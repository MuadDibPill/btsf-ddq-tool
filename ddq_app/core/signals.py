"""
DDQ Automation — Signal Detection
Analyses the full data room context and returns deal-type flags
that control which conditional DDQ blocks are activated.
"""

import json
from typing import Dict, List

import anthropic

from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from core.ingestion import Chunk, chunks_to_context


# ── Signal definitions ────────────────────────────────────────────────────────

SIGNALS = {
    "greenfield": {
        "description": "No existing substation, no prior industrial use, no interconnection executed yet",
        "keywords": ["greenfield", "interconnection application", "queue position",
                     "new site", "bare land", "no existing", "NTP", "EPC contractor",
                     "geotechnical", "grading", "access road"],
    },
    "brownfield": {
        "description": "Prior industrial use, environmental reports, RCRA/CERCLA/TCEQ references",
        "keywords": ["brownfield", "former", "remediation", "CERCLA", "RCRA", "TCEQ",
                     "contamination", "benzene", "groundwater", "corrective action",
                     "environmental indemnity", "Flint Hills", "restrictive use"],
    },
    "existing_infrastructure": {
        "description": "Existing substation, transformers, switchgear, or FEA already in place",
        "keywords": ["substation", "transformer", "switchgear", "FEA", "MVA",
                     "138 kV", "12.47 kV", "one-line diagram", "arc flash",
                     "ONCOR", "interconnection agreement", "metering"],
    },
    "btm_gas": {
        "description": "Behind-the-meter natural gas generation planned or in place",
        "keywords": ["natural gas", "pipeline", "Dth/day", "gas generator",
                     "reciprocating", "turbine", "LCOE", "Oneok", "EverLine",
                     "Caballo Loco", "Waha", "behind the meter", "BTM"],
    },
    "btm_renewable": {
        "description": "Behind-the-meter solar or wind generation",
        "keywords": ["solar", "wind", "PV", "renewable", "curtailment", "ERCOT wind",
                     "behind the meter", "BTM", "offtake solar"],
    },
    "hosting": {
        "description": "Hosting contracts or co-location agreements with third-party operators",
        "keywords": ["hosting", "co-location", "colocation", "hosting contract",
                     "hosting fee", "operator sleeve", "third-party miner",
                     "hosted hashrate", "client machines"],
    },
    "existing_debt": {
        "description": "Existing loans, credit facilities, or covenant references",
        "keywords": ["loan agreement", "credit facility", "covenant", "indebtedness",
                     "negative pledge", "cross-default", "security interest",
                     "intercreditor", "UCC", "forbearance", "maturity date"],
    },
    "permits_in_place": {
        "description": "Executed building permits, zoning certificates, or ERCOT registration",
        "keywords": ["building permit", "zoning certificate", "permit issued",
                     "permit approved", "ERCOT registration", "approved permit",
                     "certificate of occupancy"],
    },
    "equipment_purchased": {
        "description": "Mining equipment already purchased, ordered, or in transit",
        "keywords": ["purchase agreement", "invoice", "bill of lading",
                     "in transit", "warehouse", "delivery", "Antminer", "ASICs ordered",
                     "equipment purchased", "machines purchased"],
    },
    "prior_operations": {
        "description": "The site has prior operating history — hashrate data, power invoices, uptime records exist",
        "keywords": ["historical hashrate", "power invoice", "uptime", "operating history",
                     "prior operations", "existing operations", "monthly invoice",
                     "15-minute interval", "operational site"],
    },
    "ppa_present": {
        "description": "A power purchase agreement or fixed-price energy contract exists",
        "keywords": ["PPA", "power purchase agreement", "fixed price", "offtake agreement",
                     "energy contract", "fixed rate", "$/MWh fixed"],
    },
}


# ── Prompt ────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior credit analyst specialising in Bitcoin mining project finance.
Your task is to analyse a data room and detect deal-type signals that determine which 
due diligence questions should be asked.

You will be given text extracted from data room documents, then a list of signals to detect.
For each signal, return true if you find clear evidence in the documents, false if not found.

Rules:
- Be conservative: only return true if you see actual evidence, not just possibility
- If a document clearly mentions the concept, return true
- If there is no mention at all, return false
- Return ONLY valid JSON, no commentary
"""

def _build_detection_prompt(context: str, signals: Dict) -> str:
    signal_list = "\n".join(
        f'- "{key}": {info["description"]}'
        for key, info in signals.items()
    )
    return f"""Analyse the following data room documents and detect which signals are present.

SIGNALS TO DETECT:
{signal_list}

DATA ROOM DOCUMENTS:
{context}

Return a JSON object with exactly these keys, each value true or false:
{json.dumps({k: False for k in signals.keys()}, indent=2)}
"""


# ── Public API ────────────────────────────────────────────────────────────────

def detect_signals(chunks: List[Chunk]) -> Dict[str, bool]:
    """
    Run signal detection over all data room chunks.
    Returns a dict of signal_name -> bool.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Build a broad context — use all chunks up to ~14k chars
    context = chunks_to_context(chunks, max_chars=14000)

    prompt = _build_detection_prompt(context, SIGNALS)

    print("[Signal Detection] Calling Claude API...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        signals_detected = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  [WARN] Could not parse signal detection response. Using all-false defaults.")
        signals_detected = {k: False for k in SIGNALS}

    # Ensure all keys present
    for k in SIGNALS:
        if k not in signals_detected:
            signals_detected[k] = False

    print("[Signal Detection] Results:")
    for k, v in signals_detected.items():
        icon = "✓" if v else "·"
        print(f"  {icon} {k}: {v}")

    return signals_detected
