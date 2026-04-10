"""
DDQ Automation — Question Registry
Defines the minimum question set and all conditional blocks.
Maps directly to the BTSF DDQ Template.
"""

from typing import List, Dict, Optional


class Question:
    def __init__(self,
                 qid: str,
                 section: str,
                 text: str,
                 keywords: List[str],
                 conditional: Optional[str] = None):
        self.qid         = qid          # e.g. "Q1", "G.1", "H.2"
        self.section     = section      # section heading
        self.text        = text         # full question text
        self.keywords    = keywords     # retrieval keywords
        self.conditional = conditional  # signal key that unlocks this, or None = always asked


# ── SECTION 1 — CORPORATE (always asked) ─────────────────────────────────────

S1 = [
    Question("Q1", "Corporate",
        "Please provide a brief company history — legal name, jurisdiction, date of formation, and key milestones.",
        ["company history", "formation", "incorporated", "founded", "milestones", "entity"]),
    Question("Q2", "Corporate",
        "Please provide a full legal entity org chart including all entities affiliated or associated with the borrower.",
        ["org chart", "corporate structure", "holding company", "subsidiary", "ownership chain"]),
    Question("Q3", "Corporate",
        "Which entity will be the borrower?",
        ["borrower", "borrowing entity", "SPV", "LLC", "operating entity"]),
    Question("Q4", "Corporate",
        "Please provide a cap table for the borrowing entity.",
        ["cap table", "ownership", "equity split", "shareholders", "members", "percentage"]),
    Question("Q5", "Corporate",
        "What other cash flows flow to that entity? Do you have other ancillary revenue streams?",
        ["revenue", "cash flow", "income", "ancillary", "hosting revenue", "demand response"]),
    Question("Q6", "Corporate",
        "Do you have any other indebtedness at the site or corporate level? "
        "Please provide IRS CP575 notices, bank statements, and financial statements for all entities linked to the land/data center/project.",
        ["indebtedness", "debt", "loan", "covenant", "IRS CP575", "bank statement", "liabilities"]),
    Question("Q7", "Corporate",
        "Please provide historical financials for the last two years "
        "(income statement, balance sheet, cash flow statement).",
        ["financial statements", "income statement", "balance sheet", "cash flow", "financials", "P&L"]),
    Question("Q8", "Corporate",
        "What is the breakdown of liquid assets vs. illiquid assets?",
        ["liquid assets", "illiquid", "assets", "collateral", "BTC treasury", "equipment value"]),
    Question("Q9", "Corporate",
        "How have you financed the company to date?",
        ["financed", "funding", "capital raised", "equity", "prior investment", "seed"]),
    Question("Q10", "Corporate",
        "Please provide the names of your management team and a short bio on each member.",
        ["management", "CEO", "team", "biography", "principals", "founders"]),
    Question("Q11", "Corporate",
        "Please provide a view on your competitive edge.",
        ["competitive edge", "advantage", "differentiation", "moat", "unique"]),
    Question("Q12", "Corporate",
        "Please provide a view of your growth strategy.",
        ["growth", "expansion", "strategy", "roadmap", "phases", "future"]),
    Question("Q13", "Corporate",
        "What will capital funds be used for?",
        ["use of proceeds", "capex", "capital funds", "spending", "budget", "deployment"]),
]


# ── SECTION 2 — EQUIPMENT / INFRASTRUCTURE (always asked) ────────────────────

S2 = [
    Question("Q14", "Equipment / Infrastructure",
        "What is the breakdown of the assets/equipment "
        "(manufacturer, model, quantity, power draw, hashrate, efficiency)?",
        ["ASIC", "miner", "Antminer", "S21", "manufacturer", "model", "power draw", "TH/s", "J/TH", "containers"]),
    Question("Q15", "Equipment / Infrastructure",
        "What is the term of the manufacturer's warranty on the stated equipment?",
        ["warranty", "manufacturer warranty", "180 days", "guarantee"]),
    Question("Q16", "Equipment / Infrastructure",
        "Is there any other supporting infrastructure that will need to be purchased? "
        "(PDUs, cabling, cooling, civil works, fiber, networking)",
        ["infrastructure", "PDU", "cabling", "cooling", "civil works", "fiber", "networking",
         "switchgear", "transformer maintenance", "arc flash"]),
]


# ── SECTION 3 — OPERATION / SITE DETAILS ─────────────────────────────────────

S3_ALWAYS = [
    Question("Q17", "Operation / Site Details",
        "What are your total megawatts (MW) under management? What of this do you own vs. manage?",
        ["MW", "megawatt", "capacity", "owned", "managed", "hashrate"]),
    Question("Q18", "Operation / Site Details",
        "Do you plan on expanding your sites? If so, please provide plans.",
        ["expansion", "Phase 2", "Phase 3", "grid upgrade", "additional MW", "growth"]),
    Question("Q19", "Operation / Site Details",
        "Do the sites have access to water?",
        ["water", "cooling water", "municipal water", "GCA", "Gulf Coast Authority", "gallons"]),
    Question("Q20", "Operation / Site Details",
        "Please provide the address of all sites and site details "
        "(housing type, cooling method).",
        ["address", "site details", "housing", "container", "cooling", "location"]),
    Question("Q21", "Operation / Site Details",
        "How did you come into possession of / agreement with the said sites?",
        ["lease", "acquisition", "agreement", "MIPA", "purchase", "possession"]),
    Question("Q22", "Operation / Site Details",
        "Please provide proof of site/land ownership or associated leases.",
        ["lease agreement", "ownership", "FEA", "ground lease", "title", "deed"]),
    Question("Q24", "Operation / Site Details",
        "Do the sites consist of hosting or proprietary hashrate? "
        "Please state the PH and MW split.",
        ["hosting", "proprietary", "prop", "hashrate", "PH", "MW split"]),
    Question("Q26", "Operation / Site Details",
        "What is the brand/model of the machines? Please provide a fleet breakdown.",
        ["fleet", "machines", "brand", "model", "Antminer", "ASIC", "containers"]),
    Question("Q27", "Operation / Site Details",
        "Are all the stated assets/infrastructure/equipment unencumbered?",
        ["unencumbered", "lien", "security interest", "encumbrance", "UCC", "free and clear"]),
    Question("Q28", "Operation / Site Details",
        "What machine/models is the site able to house? Any rack or tank limitations?",
        ["rack", "tank", "container", "immersion", "air cooled", "hydro", "limitations"]),
    Question("Q30", "Operation / Site Details",
        "Does the site have fiber connectivity?",
        ["fiber", "fibre", "connectivity", "internet", "bandwidth", "GlobLink", "FiberLight"]),
    Question("Q33", "Operation / Site Details",
        "What is the average monthly spend or projected operating expenses?",
        ["OpEx", "operating expenses", "monthly spend", "cost", "budget"]),
    Question("Q34", "Operation / Site Details",
        "Does the site have 24/7 security personnel or plan to have them?",
        ["security", "24/7", "guard", "surveillance", "fencing", "cameras"]),
    Question("Q35", "Operation / Site Details",
        "What power redundancies are in place, if any?",
        ["redundancy", "BESS", "battery", "generator", "backup power", "UPS"]),
    Question("Q36", "Operation / Site Details",
        "Are the sites located in a Qualified Opportunity Zone (QOZ)?",
        ["QOZ", "opportunity zone", "qualified opportunity", "tax zone"]),
    Question("Q37", "Operation / Site Details",
        "Could you please provide all if any ALTA/NSPS surveys?",
        ["ALTA", "NSPS", "survey", "land survey", "acreage"]),
    Question("Q38", "Operation / Site Details",
        "Does the site have a Phase 1 ESA?",
        ["Phase 1 ESA", "ESA", "environmental site assessment", "ASTM E1527"]),
    Question("Q39", "Operation / Site Details",
        "Are there any zoning restrictions?",
        ["zoning", "industrial zone", "land use", "permit", "restrictions"]),
]

S3_CONDITIONAL = [
    Question("Q23", "Operation / Site Details",
        "Are there any exogenous factors that lead to unanticipated downtime?",
        ["downtime", "outage", "maintenance", "curtailment", "interruption"],
        conditional="prior_operations"),
    Question("Q25", "Operation / Site Details",
        "If sites contain hosting, please provide a breakdown of all hosting contract details "
        "(rate, term, expiry, notice period, termination rights, make-whole provisions).",
        ["hosting contract", "co-location", "hosting fee", "term", "$/kWh", "clients"],
        conditional="hosting"),
    Question("Q29", "Operation / Site Details",
        "Could you please provide 12 months of 15-min/hourly hashrate data.",
        ["hashrate data", "15-minute", "hourly", "historical hashrate"],
        conditional="prior_operations"),
    Question("Q31", "Operation / Site Details",
        "Does the site have an office/admin space?",
        ["office", "admin space", "NOC", "operations center"],
        conditional="prior_operations"),
    Question("Q32", "Operation / Site Details",
        "How many full-time employees are on site?",
        ["employees", "FTE", "staff", "headcount", "on site"],
        conditional="prior_operations"),
]


# ── SECTION 4 — ENERGY ────────────────────────────────────────────────────────

S4_ALWAYS = [
    Question("Q40", "Energy",
        "What is the energy source for such sites? (Grid, BTM gas, BTM renewable, hybrid)",
        ["energy source", "grid", "ERCOT", "BTM", "natural gas", "solar", "wind"]),
    Question("Q42", "Energy",
        "What is the total access to power at the current build? "
        "Is there ability to further develop power capacity?",
        ["power capacity", "MW", "FEA", "grid upgrade", "expansion", "total capacity"]),
    Question("Q43", "Energy",
        "If grid connected, is there any outstanding interconnection requests or deadline conditions?",
        ["interconnection", "FEA", "RLO", "deadline", "ONCOR", "queue"]),
    Question("Q44", "Energy",
        "What is the all-in electricity cost ($ per MWh)? Please provide a breakdown.",
        ["electricity cost", "$/MWh", "energy cost", "all-in", "ERCOT LMP", "Waha",
         "ancillaries", "delivery charge"]),
    Question("Q51", "Energy",
        "If there is no power purchase agreement, please provide an energy price schedule "
        "and backup history data of spot settle power pricing.",
        ["price schedule", "spot price", "ERCOT LMP", "historical pricing", "price history"]),
]

S4_CONDITIONAL = [
    Question("Q41", "Energy",
        "Who is the energy counterparty?",
        ["REP", "retail electric provider", "energy counterparty", "Ammper", "power supplier"],
        conditional="existing_infrastructure"),
    Question("Q45", "Energy",
        "Who is the REP for the facility?",
        ["REP", "retail electric provider", "Ammper", "electricity supplier"],
        conditional="existing_infrastructure"),
    Question("Q46", "Energy",
        "Is there a broker for the facility?",
        ["broker", "energy broker", "power broker"],
        conditional="existing_infrastructure"),
    Question("Q47", "Energy",
        "What are the REP fees? (Retail adder, credit fees, broker fees, misc)",
        ["REP fees", "retail adder", "credit fees", "broker fees", "$/MWh fees"],
        conditional="existing_infrastructure"),
    Question("Q48", "Energy",
        "Does the REP or any other party have curtailment rights?",
        ["curtailment", "curtailment rights", "interruption", "REP curtail"],
        conditional="existing_infrastructure"),
    Question("Q49", "Energy",
        "Is there a power purchase agreement (or equivalent)?",
        ["PPA", "power purchase agreement", "fixed price", "offtake"],
        conditional="existing_infrastructure"),
    Question("Q50", "Energy",
        "Does the power purchase agreement require a security deposit, letter of credit, "
        "or similar features?",
        ["PPA deposit", "security deposit", "letter of credit", "PPA security"],
        conditional="ppa_present"),
    Question("Q52", "Energy",
        "Is there a substation on site? If so, what is the maximum capacity in MW?",
        ["substation", "POI", "transformer", "138 kV", "capacity MW"],
        conditional="existing_infrastructure"),
    Question("Q53", "Energy",
        "If no substation, how is power pulled into the site? Who owns this infrastructure?",
        ["power delivery", "no substation", "distribution line", "overhead line"],
        conditional="greenfield"),
    Question("Q54", "Energy",
        "Can you please provide historical uptime.",
        ["uptime", "historical uptime", "availability", "operational history"],
        conditional="prior_operations"),
    Question("Q55", "Energy",
        "Could you please provide 12 months of power invoices.",
        ["power invoices", "electricity bills", "monthly invoices", "12 months"],
        conditional="prior_operations"),
    Question("Q56", "Energy",
        "Could you please provide 12 months of hourly power consumption data.",
        ["hourly consumption", "power consumption data", "interval data", "15-minute data"],
        conditional="prior_operations"),
]


# ── SECTION 5 — BUSINESS OPERATIONS (always asked) ───────────────────────────

S5 = [
    Question("Q57", "Business Operations",
        "Please describe the firm's liquidity management framework. "
        "Include: (1) hash rate assignment, (2) BTC treasury policy, "
        "(3) REP pre-payment, (4) debt service reserve.",
        ["liquidity", "treasury", "BTC policy", "hash rate assignment",
         "debt service reserve", "pre-payment"]),
    Question("Q58", "Business Operations",
        "What is the process for moving coin? Where is it held?",
        ["coin", "BTC custody", "custodian", "wallet", "mining pool", "Coinbase", "BitGo"]),
    Question("Q59", "Business Operations",
        "What is your current effective or pro-forma tax rate?",
        ["tax rate", "effective tax", "Section 179", "depreciation", "tax"]),
    Question("Q60", "Business Operations",
        "Are such sites subject to any tax exemptions?",
        ["tax exemption", "QOZ", "ad valorem", "abatement", "sales tax"]),
    Question("Q61", "Business Operations",
        "Do you take out any insurance policies against the mining equipment, "
        "building, or other related infrastructure?",
        ["insurance", "PLL", "pollution liability", "equipment insurance",
         "business interruption", "property insurance"]),
    Question("Q62", "Business Operations",
        "Please provide an overview of your risk management framework.",
        ["risk management", "risk framework", "BTC price risk", "energy risk",
         "environmental risk", "ONCOR deadline", "construction risk"]),
]


# ── SECTION 6 — LEGAL & REGULATORY ───────────────────────────────────────────

S6_ALWAYS = [
    Question("Q64", "Legal & Regulatory",
        "Please confirm there is no material outstanding litigation.",
        ["litigation", "lawsuit", "legal action", "court", "dispute", "PACER"]),
]

S6_CONDITIONAL = [
    Question("Q63", "Legal & Regulatory",
        "Are there any legal or regulatory approvals required for this incremental equipment? "
        "Specify county/city permits: Development Structure Permit, Drive Approach Permit, "
        "Right-of-Way Permit, Electrical Permits, Fire Code, Stormwater Compliance.",
        ["permits", "Ector County", "City of Odessa", "building permit",
         "electrical permit", "TCEQ", "ERCOT registration"],
        conditional="greenfield"),
]


# ── CONDITIONAL BLOCKS — from DDQ Template Section 6 ─────────────────────────

BLOCK_GREENFIELD = [
    Question("G.1", "Conditional — Greenfield",
        "Interconnection application status and utility queue position.",
        ["interconnection application", "queue", "utility", "ERCOT queue", "FEA status"]),
    Question("G.2", "Conditional — Greenfield",
        "Site control agreement — conditions precedent to closing "
        "(site ownership, lease, option).",
        ["site control", "lease agreement", "option", "conditions precedent", "closing"]),
    Question("G.3", "Conditional — Greenfield",
        "Has a geotechnical study been completed?",
        ["geotechnical", "soil study", "ground conditions", "foundation"]),
    Question("G.4", "Conditional — Greenfield",
        "What civil works are required before electrical work can commence? "
        "(grading, access roads, foundations)",
        ["civil works", "grading", "access road", "foundation", "site preparation"]),
    Question("G.5", "Conditional — Greenfield",
        "What is the all-in EPC cost estimate and which contractor has been engaged?",
        ["EPC", "contractor", "cost estimate", "construction cost", "engineering"]),
    Question("G.6", "Conditional — Greenfield",
        "What is the expected time from NTP (Notice to Proceed) to first energisation?",
        ["NTP", "notice to proceed", "energisation", "timeline", "schedule"]),
]

BLOCK_BROWNFIELD = [
    Question("B.1", "Conditional — Brownfield",
        "Has a Phase 2 ESA been recommended or completed?",
        ["Phase 2 ESA", "phase 2", "environmental assessment", "soil sampling", "groundwater"]),
    Question("B.2", "Conditional — Brownfield",
        "Who is the environmental indemnitor and what is their financial capacity "
        "to stand behind the indemnity?",
        ["environmental indemnitor", "indemnity", "Flint Hills", "Koch Industries",
         "indemnification", "financial capacity"]),
    Question("B.3", "Conditional — Brownfield",
        "Are there any no-build zones or excavation restrictions that reduce the "
        "usable developable area?",
        ["no-build zone", "buffer", "RCRA buffer", "excavation restriction",
         "buildable area", "usable area"]),
    Question("B.4", "Conditional — Brownfield",
        "Are there any easements granted to prior owners that survive the lease?",
        ["easement", "prior owner", "Flint Hills easement", "remediation easement",
         "pipeline easement", "surviving easement"]),
]

BLOCK_EXISTING_INFRASTRUCTURE = [
    Question("EI.1", "Conditional — Existing Infrastructure",
        "Has an independent electrical contractor conducted a health assessment of the "
        "transformers and electrical infrastructure within the last 12 months?",
        ["health assessment", "transformer testing", "electrical inspection",
         "Colliers", "EPS", "health report"]),
    Question("EI.2", "Conditional — Existing Infrastructure",
        "Has an arc flash study been completed on the switchgear?",
        ["arc flash", "arc flash study", "switchgear", "electrical safety"]),
    Question("EI.3", "Conditional — Existing Infrastructure",
        "What pre-energisation maintenance is required, what is the estimated cost, "
        "and who bears it?",
        ["maintenance", "pre-energisation", "repair cost", "maintenance cost",
         "who pays", "responsible party"]),
]

BLOCK_BTM_GAS = [
    Question("BTM.1", "Conditional — BTM Gas",
        "Which natural gas pipelines serve the site and what is the confirmed "
        "deliverable capacity (Dth/day)?",
        ["pipeline", "Dth/day", "Oneok", "EverLine", "gas capacity", "deliverable"]),
    Question("BTM.2", "Conditional — BTM Gas",
        "What is the gas pricing basis and historical basis differential "
        "(e.g. Waha vs Henry Hub)?",
        ["Waha", "Henry Hub", "gas basis", "pricing basis", "IFERC", "WASP"]),
    Question("BTM.3", "Conditional — BTM Gas",
        "Has a gas supply agreement been executed? What are the take-or-pay obligations?",
        ["gas supply agreement", "take-or-pay", "gas contract", "supply agreement"]),
    Question("BTM.5", "Conditional — BTM Gas",
        "Is there an uptime guarantee on BTM generation?",
        ["uptime guarantee", "availability", "BTM uptime", "generator SLA"]),
    Question("BTM.7", "Conditional — BTM Gas",
        "What is the all-in LCOE for BTM generation vs. grid power?",
        ["LCOE", "levelised cost", "cost comparison", "BTM cost", "$/MWh BTM"]),
    Question("BTM.8", "Conditional — BTM Gas",
        "Pre-payment risk: has the counterparty's delivery capacity been confirmed "
        "by an independent party?",
        ["pre-payment risk", "delivery capacity", "counterparty risk", "gas delivery"]),
]

BLOCK_BTM_RENEWABLE = [
    Question("BTM.4", "Conditional — BTM Renewable",
        "What is the wind/solar pricing basis and historical generation profile?",
        ["solar pricing", "wind pricing", "generation profile", "capacity factor", "curtailment"]),
    Question("BTM.6", "Conditional — BTM Renewable",
        "Will the BTM renewable installation be backed by a grid connection to "
        "guarantee minimum uptime?",
        ["grid backup", "grid connection", "minimum uptime", "renewable backup"]),
]

BLOCK_HOSTING = [
    Question("H.1", "Conditional — Hosting",
        "How many hosting clients are currently contracted and what is the total contracted MW?",
        ["hosting clients", "contracted MW", "number of clients", "total hosted"]),
    Question("H.2", "Conditional — Hosting",
        "For the most significant contracts (≥10% of customer base): MW, rate ($/kWh), "
        "term, expiry, notice period, termination rights, make-whole provisions.",
        ["hosting rate", "$/kWh", "contract term", "termination", "make-whole", "notice period"]),
    Question("H.3", "Conditional — Hosting",
        "What security interest does the operator hold over client machines in case of default?",
        ["security interest", "client machines", "default", "UCC-1", "lien on machines"]),
    Question("H.4", "Conditional — Hosting",
        "Who is responsible for client machine insurance?",
        ["machine insurance", "client insurance", "insurance responsibility"]),
    Question("H.5", "Conditional — Hosting",
        "Concentration risk: is any single client equal to or above 20% of total hosted MW?",
        ["concentration", "single client", "20%", "largest client", "client concentration"]),
    Question("H.6", "Conditional — Hosting",
        "What is the historical client churn and contract renewal rate?",
        ["churn", "renewal rate", "client retention", "turnover"]),
    Question("H.7", "Conditional — Hosting",
        "What is hosting revenue as a percentage of total facility revenue?",
        ["hosting revenue", "% revenue", "revenue split", "prop vs hosted revenue"]),
]

BLOCK_EXISTING_DEBT = [
    Question("DC.1", "Conditional — Existing Debt",
        "Full indebtedness schedule: lender name, outstanding balance, maturity date, "
        "interest rate, security granted, cross-default provisions.",
        ["lender", "balance", "maturity", "interest rate", "security", "cross-default"]),
    Question("DC.2", "Conditional — Existing Debt",
        "Are there any negative pledge clauses or restricted payment provisions?",
        ["negative pledge", "restricted payment", "covenant", "payment restriction"]),
    Question("DC.3", "Conditional — Existing Debt",
        "Does any existing lender hold a security interest over assets proposed as "
        "collateral for the new facility?",
        ["existing security interest", "prior lien", "collateral conflict", "first lien"]),
    Question("DC.4", "Conditional — Existing Debt",
        "Are there any change-of-control provisions that would be triggered by the "
        "proposed transaction?",
        ["change of control", "COC", "triggered by", "transfer restriction"]),
    Question("DC.5", "Conditional — Existing Debt",
        "Are there any outstanding defaults, waivers, or forbearance agreements?",
        ["default", "waiver", "forbearance", "breach", "cure period"]),
]


# ── Conditional block registry ────────────────────────────────────────────────

CONDITIONAL_BLOCKS: Dict[str, List[Question]] = {
    "greenfield":              BLOCK_GREENFIELD,
    "brownfield":              BLOCK_BROWNFIELD,
    "existing_infrastructure": BLOCK_EXISTING_INFRASTRUCTURE,
    "btm_gas":                 BLOCK_BTM_GAS,
    "btm_renewable":           BLOCK_BTM_RENEWABLE,
    "hosting":                 BLOCK_HOSTING,
    "existing_debt":           BLOCK_EXISTING_DEBT,
}


# ── Public API ────────────────────────────────────────────────────────────────

def assemble_questions(signals: Dict[str, bool]) -> List[Question]:
    """
    Given detected signals, return the full ordered list of active questions:
    - Always-asked minimum set
    - Conditional questions from main sections (unlocked by signals)
    - Conditional blocks (unlocked by signals)
    """
    questions: List[Question] = []

    # Minimum set — always asked
    questions.extend(S1)
    questions.extend(S2)
    questions.extend(S3_ALWAYS)
    questions.extend(S4_ALWAYS)
    questions.extend(S5)
    questions.extend(S6_ALWAYS)

    # Section-level conditional questions
    for q in S3_CONDITIONAL + S4_CONDITIONAL + S6_CONDITIONAL:
        if q.conditional is None or signals.get(q.conditional, False):
            questions.append(q)

    # Conditional blocks
    for signal_key, block in CONDITIONAL_BLOCKS.items():
        if signals.get(signal_key, False):
            questions.extend(block)

    return questions
