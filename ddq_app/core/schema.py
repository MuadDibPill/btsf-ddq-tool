"""
DDQ Automation — Structured JSON Schema Output
Extracts key deal metrics from answers into a structured JSON record.
This feeds the Excel underwriting model downstream.
"""

import json
import re
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, OUTPUT_DIR
from core.generator import Answer
from core.ingestion import Chunk, chunks_to_context, search_chunks


# ── Schema definition ─────────────────────────────────────────────────────────
# Each field: (key, description, type_hint, unit)

SCHEMA_FIELDS = {
    # Site
    "deal_name":          ("Deal / project name",                          "str",   ""),
    "site_address":       ("Full site address",                            "str",   ""),
    "state":              ("US state",                                     "str",   ""),
    "county":             ("County",                                       "str",   ""),
    "land_area_acres":    ("Land area under control",                      "float", "acres"),
    "site_type":          ("greenfield | brownfield | hybrid",             "str",   ""),
    "lease_term_years":   ("Lease or ownership term",                      "int",   "years"),

    # Power
    "capacity_mw_phase1": ("Phase 1 approved grid capacity",               "float", "MW"),
    "capacity_mw_total":  ("Total potential capacity incl. expansion",     "float", "MW"),
    "energy_source":      ("grid | btm_gas | btm_solar | btm_wind | hybrid","str",  ""),
    "utility_tdsp":       ("Transmission & Distribution Service Provider", "str",   ""),
    "rep_name":           ("Retail Electric Provider name",                "str",   ""),
    "energy_cost_mwh":    ("All-in energy cost estimate",                  "float", "$/MWh"),
    "ppa_present":        ("Fixed PPA in place (true/false)",              "bool",  ""),
    "fea_rlo_deadline":   ("ONCOR/utility RLO or energisation deadline",   "str",   "YYYY-MM-DD"),
    "substation_mva":     ("On-site substation rated capacity",            "float", "MVA"),

    # Equipment
    "asic_model":         ("Primary ASIC miner model",                     "str",   ""),
    "asic_quantity":      ("Number of ASIC units",                         "int",   "units"),
    "hashrate_total_ph":  ("Total fleet hashrate",                         "float", "PH/s"),
    "efficiency_jth":     ("Fleet efficiency",                              "float", "J/TH"),
    "container_type":     ("Container/housing type",                       "str",   ""),

    # Financial
    "acquisition_cost_usd":   ("Site/company acquisition cost",            "float", "USD"),
    "total_capex_usd":        ("Total estimated capex Phase 1",            "float", "USD"),
    "facility_size_usd":      ("Proposed debt facility size",              "float", "USD"),
    "facility_tenor_months":  ("Facility tenor",                           "int",   "months"),
    "target_irr_pct":         ("Target BTC yield / IRR",                   "float", "%"),
    "dscr_base_case":         ("Projected DSCR at base case",              "float", "x"),
    "btc_breakeven_usd":      ("BTC price at which FCF turns positive",    "float", "USD"),
    "monthly_opex_usd":       ("Estimated monthly operating expenses",     "float", "USD"),
    "energy_cost_annual_usd": ("Estimated annual energy cost",             "float", "USD"),

    # Operations
    "prop_hashrate_mw":   ("Proprietary hashrate capacity",                "float", "MW"),
    "hosted_mw":          ("Hosted / co-location capacity",                "float", "MW"),
    "hosting_clients":    ("Number of hosting clients",                    "int",   ""),
    "fte_onsite":         ("Full-time employees on site",                  "int",   "FTE"),

    # Legal / environmental
    "phase1_esa_complete":   ("Phase 1 ESA completed (true/false)",        "bool",  ""),
    "alta_survey_complete":  ("ALTA/NSPS survey current (true/false)",     "bool",  ""),
    "permits_filed":         ("Permits filed (true/false/partial)",        "str",   ""),
    "env_indemnitor":        ("Environmental indemnitor name",             "str",   ""),
    "existing_debt":         ("Existing debt at any entity level (true/false)","bool",""),

    # Corporate
    "borrowing_entity":      ("Legal name of borrowing entity",            "str",   ""),
    "jurisdiction":          ("State of formation of borrowing entity",    "str",   ""),
    "principals":            ("Key principals / management names",         "str",   ""),
}


# ── Extraction prompt ─────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a financial analyst extracting structured data from due diligence answers
for a Bitcoin mining infrastructure financing transaction.

Extract the requested fields from the provided answers. Rules:
- Extract only what is clearly stated — do not infer or estimate
- For numeric fields, return numbers only (no units, no $ signs, no commas)
- For boolean fields, return true or false (lowercase)
- For dates, use YYYY-MM-DD format
- If a field cannot be determined from the answers, return null
- Return ONLY valid JSON, no commentary, no markdown fences
"""


def _build_extraction_prompt(answers: List[Answer], schema: Dict) -> str:
    # Summarise key answers for context
    answer_text = "\n\n".join(
        f"[{a.question.qid}] {a.question.text}\n{a.text}"
        for a in answers
        if a.confidence != "gap" and len(a.text) > 20
    )
    # Truncate to avoid context limit
    if len(answer_text) > 15000:
        answer_text = answer_text[:15000] + "\n[truncated]"

    field_list = "\n".join(
        f'  "{k}": {info[1]}  // {info[0]} ({info[2]} {info[3]})'.strip()
        for k, info in schema.items()
    )

    return f"""Extract the following fields from these due diligence answers.

FIELDS TO EXTRACT:
{{
{field_list}
}}

DUE DILIGENCE ANSWERS:
{answer_text}

Return a JSON object with exactly the keys listed above.
Use null for any field that cannot be determined."""


# ── Public API ────────────────────────────────────────────────────────────────

def extract_schema(answers: List[Answer],
                   deal_name: str = "Project XXX") -> Dict[str, Any]:
    """
    Call Claude to extract structured deal metrics from DDQ answers.
    Returns a dict matching SCHEMA_FIELDS.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print("[Schema] Extracting structured data from answers...")
    prompt = _build_extraction_prompt(answers, SCHEMA_FIELDS)

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        schema = json.loads(raw)
    except json.JSONDecodeError:
        print("  [WARN] Could not parse schema extraction. Using empty schema.")
        schema = {k: None for k in SCHEMA_FIELDS}

    # Always set deal_name
    schema["deal_name"] = deal_name
    schema["_extracted_at"] = datetime.now().isoformat()

    return schema


def save_schema_json(schema: Dict[str, Any], deal_name: str) -> str:
    """Save the structured schema to a JSON file. Returns file path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    safe_name = deal_name.replace(" ", "_").replace("/", "-")
    filename  = f"Schema_{safe_name}_{timestamp}.json"
    filepath  = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"[Schema] Saved JSON: {filepath}")
    return filepath


def print_schema_summary(schema: Dict[str, Any]):
    """Print a human-readable summary of extracted values."""
    print("\n[Schema] Extracted deal metrics:")
    groups = {
        "Site":       ["deal_name","site_address","state","land_area_acres","site_type","lease_term_years"],
        "Power":      ["capacity_mw_phase1","capacity_mw_total","energy_source","energy_cost_mwh","fea_rlo_deadline","ppa_present"],
        "Financial":  ["acquisition_cost_usd","total_capex_usd","facility_size_usd","facility_tenor_months","dscr_base_case","btc_breakeven_usd"],
        "Equipment":  ["asic_model","asic_quantity","hashrate_total_ph","efficiency_jth"],
        "Operations": ["prop_hashrate_mw","hosted_mw","hosting_clients","fte_onsite"],
        "Legal":      ["phase1_esa_complete","alta_survey_complete","existing_debt","env_indemnitor"],
    }
    for group, keys in groups.items():
        print(f"\n  ── {group}")
        for k in keys:
            v = schema.get(k)
            field_info = SCHEMA_FIELDS.get(k, ("","","",""))
            unit = f" {field_info[3]}" if field_info[3] else ""
            status = "✓" if v is not None else "·"
            print(f"    {status} {k}: {v}{unit if v is not None else ''}")
