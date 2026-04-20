"""
DDQ Automation — Question Registry
Maps 1:1 to the BTSF Mining Finance DDQ v1.1 PDF template (18 sections, Q1–Q128).

Architecture:
    - Minimum set   : questions always asked  (sections 1–9, 11–14, 16–18)
    - Conditional Q : questions whose relevance depends on a detected signal
                      (e.g. hosting, existing_debt, btm_gas, ppa_present, distressed)
    - Blocks        : existing deep-dive blocks (Greenfield, Brownfield, Existing
                      Infrastructure, BTM Gas, BTM Renewable, Hosting, Existing Debt)
                      kept as complements that expand on the standard template when
                      the corresponding signal is detected.

Question IDs follow the PDF numbering (Q1…Q128). Block IDs keep their short codes
(G.x, B.x, EI.x, BTM.x, H.x, DC.x) for backward compatibility with writer / schema.
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


# =============================================================================
# STANDARD TEMPLATE — BTSF Mining Finance DDQ v1.1
# =============================================================================

# ── SECTION 1 — GENERAL INFORMATION AND DEAL OVERVIEW (always asked) ──────────

S1 = [
    Question("Q1", "1. General information and deal overview",
        "Contact person for this due diligence (name, title, email, direct line). "
        "Please also nominate a back-up contact.",
        ["contact", "point of contact", "name", "email", "phone", "back-up contact"]),
    Question("Q2", "1. General information and deal overview",
        "Brief description (one to two pages) of the Borrower, the business, and "
        "the transaction being proposed.",
        ["business description", "borrower description", "transaction overview",
         "executive summary", "company overview"]),
    Question("Q3", "1. General information and deal overview",
        "Use of proceeds: please provide a detailed source-and-uses table covering "
        "the full capital stack contemplated for this transaction.",
        ["use of proceeds", "sources and uses", "capital stack", "deployment",
         "funding use", "S&U table"]),
    Question("Q4", "1. General information and deal overview",
        "Requested facility terms as you understand them (size, tenor, currency of "
        "denomination, amortization profile, expected drawdown schedule, intended "
        "collateral package).",
        ["facility size", "tenor", "amortization", "drawdown", "collateral package",
         "term sheet", "requested terms"]),
    Question("Q5", "1. General information and deal overview",
        "Transaction timeline and any hard deadlines (equipment delivery, power "
        "energization, refinancing maturity, closing conditions).",
        ["timeline", "deadline", "closing", "energization", "delivery date",
         "refinancing maturity", "milestones"]),
    Question("Q6", "1. General information and deal overview",
        "Please list all parties materially involved in the transaction (co-lenders, "
        "equity co-investors, sponsors, brokers, advisors) and attach any term sheets, "
        "mandate letters, or commitment documents already in place.",
        ["co-lender", "co-investor", "sponsor", "broker", "advisor", "mandate letter",
         "term sheet", "commitment letter"]),
    Question("Q7", "1. General information and deal overview",
        "Please list all other lenders or capital providers that have reviewed this "
        "transaction and state the outcome of each process (declined / in progress / "
        "committed / withdrawn), including the stated reasons for any decline.",
        ["other lenders", "prior review", "declined", "committed", "withdrawn",
         "capital providers", "lender list"]),
]


# ── SECTION 2 — CORPORATE AND OWNERSHIP (always asked) ────────────────────────

S2 = [
    Question("Q8", "2. Corporate and ownership",
        "Please provide a brief company history covering material milestones, "
        "fundraising rounds, pivots, and any previous workouts or restructurings.",
        ["company history", "milestones", "fundraising", "restructuring", "pivots",
         "workout history"]),
    Question("Q9", "2. Corporate and ownership",
        "Please provide a full legal entity organization chart covering the Borrower "
        "and every affiliated or associated entity. Highlight the proposed Borrower "
        "and the entity or entities that will own the pledged collateral.",
        ["org chart", "organization chart", "legal entity", "affiliates", "subsidiary",
         "collateral owning entity"]),
    Question("Q10", "2. Corporate and ownership",
        "Which entity will be the Borrower? Please provide its certificate of "
        "incorporation / formation, current good-standing certificate, and governing "
        "documents (articles, bylaws, operating agreement, shareholders' agreement).",
        ["borrower entity", "certificate of incorporation", "good standing",
         "articles", "bylaws", "operating agreement", "shareholders agreement"]),
    Question("Q11", "2. Corporate and ownership",
        "Please provide a complete, up-to-date capitalization table for the Borrower, "
        "showing all classes of equity, options, warrants, SAFEs, convertibles, and "
        "any shareholder loans. Identify all ultimate beneficial owners (UBOs) with "
        "a 10% or greater economic or voting interest.",
        ["cap table", "capitalization", "equity classes", "warrants", "SAFE",
         "convertible", "shareholder loan", "UBO", "beneficial owner"]),
    Question("Q12", "2. Corporate and ownership",
        "Please identify all directors, officers, and authorized signatories of the "
        "Borrower, including any independent or sponsor-appointed directors, and "
        "provide copies of the relevant resolutions or delegations of authority.",
        ["directors", "officers", "authorized signatories", "independent director",
         "board resolution", "delegation of authority"]),
    Question("Q13", "2. Corporate and ownership",
        "Are there any affiliate, related-party, or intercompany arrangements "
        "material to the Borrower (management services agreements, IP licenses, "
        "shared services, intercompany loans, cost allocations)? Please describe "
        "and provide copies.",
        ["related party", "affiliate agreement", "intercompany loan", "shared services",
         "IP license", "management services agreement", "cost allocation"]),
    Question("Q14", "2. Corporate and ownership",
        "Please list and describe any other cash-generating activities of the "
        "Borrower or its affiliates (ancillary revenue streams, hosting, services, "
        "royalties, software licensing, AI / HPC, energy arbitrage, etc.).",
        ["ancillary revenue", "cash generating", "hosting revenue", "royalties",
         "AI HPC", "energy arbitrage", "other revenue"]),
    Question("Q15", "2. Corporate and ownership",
        "Please describe any recent or proposed mergers, acquisitions, divestitures, "
        "spin-offs, or reorganizations involving the Borrower or its affiliates.",
        ["merger", "acquisition", "divestiture", "spin-off", "reorganization", "M&A"]),
    Question("Q16", "2. Corporate and ownership",
        "Please describe any governance arrangements, shareholder veto rights, or "
        "consent thresholds that could restrict the Borrower's ability to borrow, "
        "grant security, or make distributions.",
        ["governance", "veto rights", "consent threshold", "borrowing restriction",
         "distribution restriction", "shareholder approval"]),
]


# ── SECTION 3 — MANAGEMENT, ORGANIZATION, AND OPERATIONS TEAM (always asked) ──

S3 = [
    Question("Q17", "3. Management, organization, and operations team",
        "Please provide bios (including LinkedIn URLs) for each member of the "
        "executive and operations teams (CEO, CFO, COO, CMO / head of mining, "
        "head of energy, head of sites, head of infrastructure).",
        ["bios", "CEO", "CFO", "COO", "head of mining", "head of energy",
         "LinkedIn", "executive team", "management bios"]),
    Question("Q18", "3. Management, organization, and operations team",
        "Please provide an organizational chart showing full-time employees by "
        "function (mining operations, data center engineering, electrical / "
        "infrastructure, site security, finance, admin), separating head-office "
        "staff from on-site staff.",
        ["org chart", "FTE", "full-time employees", "headcount", "mining operations",
         "data center engineering", "on-site staff"]),
    Question("Q19", "3. Management, organization, and operations team",
        "Please describe the Borrower's view on its competitive edge, with "
        "particular reference to (i) cost of power, (ii) operational uptime, "
        "(iii) fleet quality, (iv) access to capital, and (v) partnerships.",
        ["competitive edge", "advantage", "cost of power", "uptime",
         "fleet quality", "access to capital", "partnerships"]),
    Question("Q20", "3. Management, organization, and operations team",
        "Please describe the Borrower's growth strategy and any constraints "
        "(capital, power, equipment, land, permits) to executing it.",
        ["growth strategy", "expansion", "constraints", "capital constraint",
         "power constraint", "land constraint"]),
    Question("Q21", "3. Management, organization, and operations team",
        "Please describe any material turnover in the management team, senior "
        "operations, or board over the last twenty-four (24) months, and the "
        "reasons for such changes.",
        ["management turnover", "departure", "resignation", "board changes",
         "executive changes", "24 months"]),
    Question("Q22", "3. Management, organization, and operations team",
        "Please describe any third-party operators, maintenance providers, or "
        "hosting partners used across the fleet, and attach the corresponding "
        "master services, hosting, and maintenance agreements.",
        ["third-party operator", "maintenance provider", "hosting partner",
         "master services agreement", "MSA", "outsourced operations"]),
]


# ── SECTION 4 — HISTORICAL AND PROJECTED FINANCIALS (always asked) ────────────

S4 = [
    Question("Q23", "4. Historical and projected financials",
        "Please provide historical financial statements for the last three (3) "
        "years and year-to-date (income statement, balance sheet, cash flow "
        "statement), audited where available. If audited accounts are not "
        "available, please explain why and state the plan to achieve auditability.",
        ["financial statements", "income statement", "balance sheet", "cash flow",
         "audited", "YTD", "three years", "P&L"]),
    Question("Q24", "4. Historical and projected financials",
        "Identity and qualifications of the current auditor or, where unaudited, "
        "the accounting firm assisting with management accounts. Please note any "
        "auditor changes in the last three (3) years and the reasons.",
        ["auditor", "accounting firm", "auditor change", "management accounts",
         "big 4", "qualifications"]),
    Question("Q25", "4. Historical and projected financials",
        "Please describe the Bitcoin accounting policy applied (cost, fair value, "
        "digital-asset standard) and the treatment of mining rewards, pool fees, "
        "hosting revenue, and impairment.",
        ["Bitcoin accounting", "fair value", "digital asset", "mining rewards",
         "pool fees", "impairment", "accounting policy", "ASU 2023-08"]),
    Question("Q26", "4. Historical and projected financials",
        "Please provide the current fiscal-year budget and the Borrower's base-case "
        "financial model (monthly, at least 36 months forward), with full workings. "
        "The model should be delivered as an unlocked Excel file and should include: "
        "hashrate build-out schedule (PH/s by machine type); Bitcoin production "
        "forecast (BTC/month) with difficulty, block subsidy, transaction fees, pool "
        "fees; energy consumption and cost (kWh, $/MWh); hosting / ancillary revenue; "
        "operating expenses by category; capital expenditure by tranche; debt schedule "
        "including proposed facility; Bitcoin treasury policy and assumed realization "
        "prices.",
        ["financial model", "budget", "base case", "36 months", "hashrate build-out",
         "BTC production", "difficulty", "block subsidy", "OpEx", "capex",
         "debt schedule", "treasury policy"]),
    Question("Q27", "4. Historical and projected financials",
        "Please provide sensitivity analysis around Bitcoin price (minimum: $40k / "
        "$60k / $100k / $150k), network hashrate (+/- 30%), power cost (+/- 25%), "
        "and machine efficiency. Please state what the model implies for debt-service "
        "coverage and liquidity under each scenario.",
        ["sensitivity", "BTC price sensitivity", "hashrate sensitivity",
         "power cost sensitivity", "DSCR", "liquidity scenario", "stress test"]),
    Question("Q28", "4. Historical and projected financials",
        "Please provide the breakdown of liquid vs illiquid assets at the latest "
        "period end (cash, cash equivalents, BTC held, receivables, inventory, "
        "ASIC fleet at book and fair value, infrastructure, other).",
        ["liquid assets", "illiquid assets", "cash", "BTC holdings", "receivables",
         "inventory", "ASIC book value", "fair value"]),
    Question("Q29", "4. Historical and projected financials",
        "Please describe the Borrower's liquidity-management framework, including "
        "minimum cash balance policy, BTC treasury buffer, working-capital lines, "
        "and any committed but undrawn facilities.",
        ["liquidity management", "minimum cash", "BTC buffer", "working capital",
         "undrawn facility", "committed facility"]),
    Question("Q30", "4. Historical and projected financials",
        "Please describe all off-balance-sheet arrangements, contingent liabilities, "
        "guarantees, letters of credit, surety bonds, and performance bonds.",
        ["off-balance-sheet", "contingent liability", "guarantee", "letter of credit",
         "LoC", "surety bond", "performance bond"]),
]


# ── SECTION 5 — CAPITAL STRUCTURE AND EXISTING INDEBTEDNESS ───────────────────
# Q31 always asked (universal disclosure); Q32–Q35 also always asked.

S5 = [
    Question("Q31", "5. Capital structure and existing indebtedness",
        "Please list every item of indebtedness, financial lease, or equipment "
        "finance arrangement currently outstanding at the Borrower and at any "
        "site-level or SPV entity, including: lender / counterparty; principal "
        "outstanding and commitment size; coupon, fee structure, and effective "
        "cost; maturity and amortization profile; security granted (collateral, "
        "guarantees, intercreditor status); key financial and operational "
        "covenants; any existing defaults, waivers, forbearances, or amendments "
        "in the last twenty-four (24) months. Please attach the underlying credit "
        "agreements, security documents, and intercreditor agreements.",
        ["indebtedness", "debt schedule", "loan agreement", "equipment finance",
         "credit agreement", "covenant", "intercreditor", "security document",
         "default", "waiver", "forbearance"]),
    Question("Q32", "5. Capital structure and existing indebtedness",
        "Please list any equity commitments, shareholder loans, or convertible "
        "instruments outstanding, with the same level of detail.",
        ["equity commitment", "shareholder loan", "convertible", "preferred equity",
         "SAFE", "note"]),
    Question("Q33", "5. Capital structure and existing indebtedness",
        "Please describe the Borrower's historical financing strategy (debt, "
        "equity, strategic / JV), including amounts raised, investors, and uses "
        "of proceeds.",
        ["financing history", "capital raised", "investors", "prior rounds",
         "JV financing", "use of proceeds history"]),
    Question("Q34", "5. Capital structure and existing indebtedness",
        "Please identify any outstanding make-whole, prepayment premium, or "
        "exit-fee obligations, and any restrictions on refinancing that could "
        "affect this transaction.",
        ["make-whole", "prepayment premium", "exit fee", "refinancing restriction",
         "call protection"]),
    Question("Q35", "5. Capital structure and existing indebtedness",
        "Please identify any existing liens or security interests across the "
        "Borrower and its affiliates (UCC-1 filings, pledges over shares or bank "
        "accounts, mortgages, ASIC chattel pledges) and provide copies.",
        ["lien", "security interest", "UCC-1", "share pledge", "bank account pledge",
         "mortgage", "chattel pledge"]),
]


# ── SECTION 6 — ASIC FLEET AND EQUIPMENT (always asked) ───────────────────────

S6 = [
    Question("Q36", "6. ASIC fleet and equipment",
        "Please provide a full fleet inventory, categorized by site, including for "
        "each machine type: manufacturer, model, quantity, nominal hashrate (TH/s), "
        "rated power (W), efficiency (J/TH), vintage (manufacture / purchase date), "
        "warranty status, and ownership status (owned, leased, hosted, financed).",
        ["fleet inventory", "ASIC", "Antminer", "Whatsminer", "manufacturer",
         "model", "TH/s", "J/TH", "vintage", "warranty", "ownership status"]),
    Question("Q37", "6. ASIC fleet and equipment",
        "Please state the total fleet nameplate hashrate (PH/s) and realized "
        "hashrate (trailing 3-month average), with any material gap explained.",
        ["nameplate hashrate", "realized hashrate", "PH/s", "EH/s",
         "3-month average", "hashrate gap"]),
    Question("Q38", "6. ASIC fleet and equipment",
        "Please describe the Borrower's ASIC procurement strategy, including "
        "relationships with Bitmain, MicroBT, Canaan, and any secondary-market "
        "channels, and describe any outstanding purchase orders, deposits, or "
        "delivery schedules.",
        ["procurement strategy", "Bitmain", "MicroBT", "Canaan", "secondary market",
         "purchase order", "deposit", "delivery schedule"]),
    Question("Q39", "6. ASIC fleet and equipment",
        "Please provide the manufacturer warranty terms, remaining coverage period, "
        "and RMA history (failure rates, repair turnaround) for each machine type.",
        ["warranty terms", "coverage period", "RMA", "failure rate", "repair turnaround"]),
    Question("Q40", "6. ASIC fleet and equipment",
        "Please describe the Borrower's firmware and overclocking strategy (stock "
        "firmware, Braiins OS, LuxOS, custom firmware), the rationale, and the "
        "resulting efficiency gains or stability trade-offs.",
        ["firmware", "overclocking", "Braiins OS", "LuxOS", "custom firmware",
         "underclock", "efficiency gain"]),
    Question("Q41", "6. ASIC fleet and equipment",
        "Please describe any supporting infrastructure that is part of the "
        "collateral package or required to operate the fleet (PDUs, switchgear, "
        "transformers, cooling skids, controllers, immersion tanks, network equipment).",
        ["supporting infrastructure", "PDU", "switchgear", "transformer",
         "cooling skid", "immersion tank", "network equipment"]),
    Question("Q42", "6. ASIC fleet and equipment",
        "Are any of the stated assets, infrastructure, or equipment currently "
        "encumbered, subject to a purchase-money security interest, or under a "
        "retention-of-title clause? If yes, please provide the financing documents "
        "and the path to release.",
        ["encumbered", "purchase-money security", "PMSI", "retention of title",
         "release path", "free and clear"]),
    Question("Q43", "6. ASIC fleet and equipment",
        "Please provide ASIC depreciation schedules and the Borrower's policy for "
        "technology refresh / fleet replacement.",
        ["depreciation", "tech refresh", "fleet replacement", "useful life",
         "residual value"]),
    Question("Q44", "6. ASIC fleet and equipment",
        "Please describe the Borrower's maintenance framework (spare-parts inventory, "
        "in-house repair capability, on-site technicians, third-party repair centers, "
        "warranty claims process). Please provide the last twelve (12) months of "
        "maintenance and downtime logs.",
        ["maintenance framework", "spare parts", "repair capability", "technician",
         "maintenance log", "downtime log"]),
]


# ── SECTION 7 — SITES AND INFRASTRUCTURE ──────────────────────────────────────
# Q45-Q54 always asked (core site disclosure).

S7 = [
    Question("Q45", "7. Sites and infrastructure",
        "Please list every site included in the transaction perimeter, with the "
        "following detail for each: address and GPS coordinates; total nameplate "
        "capacity (MW) and currently energized capacity (MW); proprietary hashrate "
        "MW vs hosting MW; housing type (purpose-built, modular containers, retrofit); "
        "cooling technology (air, immersion, hydro / direct-to-chip); machine / rack / "
        "tank compatibility constraints; current utilization (percent); trailing "
        "12-month uptime; number of on-site full-time employees and 24/7 security "
        "coverage; fiber connectivity (provider, redundancy, bandwidth); office / "
        "admin and warehouse facilities on-site.",
        ["site list", "address", "GPS", "nameplate capacity", "energized capacity",
         "proprietary", "hosting MW", "container", "cooling", "immersion", "air cooled",
         "hydro", "uptime", "fiber", "on-site FTE", "security coverage"]),
    Question("Q46", "7. Sites and infrastructure",
        "For each site, please describe how the Borrower acquired possession or "
        "use rights (freehold, long-term lease, sublease, joint venture, usage right) "
        "and provide proof of ownership or the underlying lease and any addenda.",
        ["site control", "freehold", "lease", "sublease", "joint venture",
         "proof of ownership", "deed", "title"]),
    Question("Q47", "7. Sites and infrastructure",
        "Where lease-based, please state remaining term, renewal options, rent "
        "escalation mechanics, landlord consent requirements for security interests, "
        "and any change-of-control or assignment restrictions.",
        ["lease term", "renewal option", "rent escalation", "landlord consent",
         "change of control", "assignment restriction"]),
    Question("Q48", "7. Sites and infrastructure",
        "Please provide any ALTA / NSPS surveys, Phase I environmental site "
        "assessments, and geotechnical reports.",
        ["ALTA", "NSPS", "survey", "Phase I ESA", "environmental site assessment",
         "geotechnical report", "ASTM E1527"]),
    Question("Q49", "7. Sites and infrastructure",
        "Please describe the permitting and zoning status of each site (land-use "
        "designation, special-use permits, local approvals, any open violations "
        "or notices of violation).",
        ["permit", "zoning", "land use", "special use permit", "local approval",
         "violation", "notice of violation"]),
    Question("Q50", "7. Sites and infrastructure",
        "Please identify any known exogenous factors that cause or could cause "
        "unanticipated downtime (weather, grid instability, wildlife, civil unrest, "
        "water supply, cooling-water rights).",
        ["exogenous factor", "weather", "grid instability", "wildlife",
         "water supply", "water rights", "downtime risk"]),
    Question("Q51", "7. Sites and infrastructure",
        "Please describe planned expansions, build-outs, or consolidations across "
        "the site portfolio, including capacity (MW), expected energization dates, "
        "CAPEX, and the source of funding.",
        ["expansion", "build-out", "Phase 2", "Phase 3", "energization date",
         "expansion capex", "funding source"]),
    Question("Q52", "7. Sites and infrastructure",
        "Please describe the material near-term operational problems that must be "
        "solved (six to twelve months) and the Borrower's plan for each.",
        ["near-term problem", "operational issue", "6-12 months", "remediation plan",
         "action plan"]),
    Question("Q53", "7. Sites and infrastructure",
        "Please describe power and network redundancies in place (N+1, N+2, "
        "generator backup, dual-feed substation, secondary fiber).",
        ["redundancy", "N+1", "N+2", "generator backup", "dual feed", "secondary fiber",
         "UPS", "BESS"]),
    Question("Q54", "7. Sites and infrastructure",
        "Please indicate whether any site is located in a Qualified Opportunity Zone "
        "(QOZ), a Foreign Trade Zone, or any other tax-advantaged district, and the "
        "expected duration of such benefits.",
        ["QOZ", "qualified opportunity zone", "foreign trade zone", "FTZ",
         "tax advantaged", "enterprise zone"]),
]


# ── SECTION 8 — ENERGY ────────────────────────────────────────────────────────
# Core questions always asked; hedging/PPA-specific gated by signals.

S8_ALWAYS = [
    Question("Q55", "8. Energy",
        "For each site, please describe the energy source (grid, co-location, "
        "behind-the-meter natural gas, flared gas, hydro, solar, wind, nuclear, "
        "hybrid) and the energy counterparty (utility, IPP, REP, landlord, "
        "owner-operator).",
        ["energy source", "grid", "BTM", "natural gas", "flared gas", "hydro",
         "solar", "wind", "nuclear", "counterparty", "REP", "utility"]),
    Question("Q56", "8. Energy",
        "Please provide the total contracted power capacity at current build, "
        "including any reserved capacity for expansion, and describe the pathway "
        "to any additional MW.",
        ["contracted power", "capacity", "reserved capacity", "expansion MW",
         "pathway to MW"]),
    Question("Q57", "8. Energy",
        "For each source, please state the all-in delivered energy cost ($/MWh), "
        "including a breakdown of wholesale / node price, transmission, distribution, "
        "retail adder, ancillary services, capacity charges, credit / collateral fees, "
        "broker fees, and taxes. Please provide the last twelve (12) months of invoices.",
        ["all-in cost", "$/MWh", "wholesale", "node price", "transmission",
         "distribution", "retail adder", "ancillary", "capacity charge", "broker fee",
         "12 months invoices"]),
    Question("Q58", "8. Energy",
        "Please identify the retail energy provider (REP) and any brokers involved, "
        "and describe their respective roles and fees.",
        ["REP", "retail electric provider", "broker", "energy broker", "fees"]),
    Question("Q59", "8. Energy",
        "Please describe the curtailment regime: who has the right to curtail, on "
        "what terms, with what notice, and what has been the realized curtailment "
        "(hours, MWh) over the last twelve (12) months.",
        ["curtailment", "curtailment rights", "curtailment hours", "curtailment MWh",
         "notice period"]),
    Question("Q63", "8. Energy",
        "Is there a substation on site? If yes, please state the maximum capacity "
        "(MW) and ownership (Borrower-owned, utility-owned, leased).",
        ["substation", "on-site substation", "MVA", "substation ownership",
         "utility owned"]),
    Question("Q64", "8. Energy",
        "If no on-site substation, please describe how power is delivered to site, "
        "the owner of the interconnection and delivery infrastructure, and any "
        "ongoing obligations attached to it.",
        ["power delivery", "interconnection", "delivery infrastructure",
         "no substation", "distribution line"]),
    Question("Q66", "8. Energy",
        "Please describe any outstanding interconnection requests, study queue "
        "positions, upgrade obligations, or system-impact studies for capacity expansion.",
        ["interconnection request", "queue position", "system impact study",
         "upgrade obligation", "FEA", "RLO"]),
    Question("Q67", "8. Energy",
        "Please describe the Borrower's participation in any demand-response, "
        "ancillary-services, or grid-balancing programs, and the revenue / credits "
        "generated from each over the last twelve (12) months.",
        ["demand response", "ancillary services", "grid balancing", "ERS", "RRS",
         "4CP", "program revenue"]),
    Question("Q68", "8. Energy",
        "Please describe any anticipated changes in the relevant electricity market "
        "(regulation, tariff design, capacity market, renewable procurement obligations) "
        "that could affect the site economics.",
        ["market change", "regulation", "tariff", "capacity market", "PCM",
         "renewable procurement"]),
]

S8_CONDITIONAL = [
    Question("Q60", "8. Energy",
        "Please provide the latest executed power purchase agreement, energy-services "
        "agreement, or co-location agreement and describe: counterparty and site; "
        "contracted MW, start date, remaining term, renewal options; pricing formula "
        "(fixed, indexed, heat-rate, floor / cap); collateral or security-deposit "
        "requirements; curtailment and make-whole mechanics; termination rights, "
        "including for convenience, and any change-of-control or assignment restrictions.",
        ["PPA", "power purchase agreement", "ESA", "co-location agreement",
         "pricing formula", "heat rate", "floor cap", "security deposit",
         "termination right"],
        conditional="ppa_present"),
    Question("Q61", "8. Energy",
        "If no PPA is in place, please provide an energy-price schedule and at least "
        "twelve (12) months of hourly spot-settled power pricing data, plus the "
        "Borrower's view on forward pricing and hedging.",
        ["price schedule", "spot price", "hourly pricing", "forward pricing",
         "hedging view", "ERCOT LMP"]),
    Question("Q62", "8. Energy",
        "Please describe any active hedging program covering power (financial or "
        "physical), its tenor, notional, and the counterparty.",
        ["hedging program", "power hedge", "financial hedge", "physical hedge",
         "tenor", "notional"]),
    Question("Q65", "8. Energy",
        "Please provide at least twelve (12) months of (i) hourly power consumption "
        "data and (ii) hourly realized hashrate data at site level, and historical "
        "site-level uptime.",
        ["hourly consumption", "hourly hashrate", "15-minute data", "interval data",
         "uptime history"],
        conditional="prior_operations"),
]


# ── SECTION 9 — MINING OPERATIONS, POOL, AND REVENUE MANAGEMENT ───────────────
# All always-asked: pool/routing disclosures are critical to collateral package.

S9 = [
    Question("Q69", "9. Mining operations, pool, and revenue management",
        "Please describe the Borrower's mining pool strategy, including the pool(s) "
        "used, payout scheme (FPPS, PPS, PPLNS, PPLNS+, solo), pool fees, and any "
        "minimum commitment or exclusivity terms. Please attach the pool agreement(s).",
        ["mining pool", "FPPS", "PPS", "PPLNS", "pool fee", "pool agreement",
         "Foundry", "Antpool", "ViaBTC", "Luxor", "Braiins"]),
    Question("Q70", "9. Mining operations, pool, and revenue management",
        "Please describe the process by which hashrate can be redirected to another "
        "pool (technical mechanism, minimum switching interval, operational constraints, "
        "counterparty consents required). BTSF will typically require that pool-routing "
        "rights be pledged or assigned as part of the collateral package.",
        ["hashrate redirection", "pool switching", "routing rights",
         "pool switching interval", "pledge routing"]),
    Question("Q71", "9. Mining operations, pool, and revenue management",
        "Please describe the payout flow: from pool to which wallet(s), on what "
        "cadence, through which intermediaries, and subject to which internal controls.",
        ["payout flow", "wallet", "pool payout", "cadence", "internal control",
         "wallet architecture"]),
    Question("Q72", "9. Mining operations, pool, and revenue management",
        "Please provide the last twelve (12) months of mining production data, "
        "including BTC earned per site, pool fees paid, average realized revenue "
        "per PH/day, and reconciliation to reported revenue.",
        ["BTC earned", "mining production", "pool fees paid", "revenue per PH",
         "reconciliation"]),
    Question("Q73", "9. Mining operations, pool, and revenue management",
        "Please describe any variable operating strategies used to manage margin "
        "(uptime curtailment, seasonal ramp, firmware tuning, dynamic frequency / "
        "voltage scaling, peak-hour avoidance).",
        ["variable operating", "dynamic frequency", "voltage scaling",
         "peak-hour avoidance", "seasonal ramp", "firmware tuning"]),
    Question("Q74", "9. Mining operations, pool, and revenue management",
        "Please describe the Borrower's AI / HPC strategy, if any, and whether any "
        "power or infrastructure is currently allocated or contemplated for "
        "non-Bitcoin workloads.",
        ["AI", "HPC", "non-Bitcoin workload", "GPU", "high performance computing",
         "AI allocation"]),
    Question("Q75", "9. Mining operations, pool, and revenue management",
        "Please describe any revenue-sharing, joint venture, or profit-share "
        "arrangements with strategic partners or hosting clients, and attach the "
        "underlying agreements.",
        ["revenue share", "profit share", "joint venture", "strategic partner",
         "hosting client JV"]),
]


# ── SECTION 10 — HOSTING AND THIRD-PARTY ARRANGEMENTS (conditional) ───────────
# Entire section gated by hosting signal.

S10 = [
    Question("Q76", "10. Hosting and third-party arrangements",
        "If the Borrower operates a hosting business or hosts third-party equipment, "
        "please provide a schedule of all hosting contracts with the following "
        "detail: client name, contracted MW / machine count, pricing (per kWh, fixed "
        "fee, profit-share), term, renewal, security deposits, make-whole clauses, "
        "security interests in client machines, and any exclusivity.",
        ["hosting contract", "client name", "contracted MW", "$/kWh", "profit share",
         "security deposit", "make-whole", "exclusivity"],
        conditional="hosting"),
    Question("Q77", "10. Hosting and third-party arrangements",
        "Please describe any hosting client concentration (top three by MW and "
        "revenue) and any known client credit issues, past-due balances, or disputes.",
        ["client concentration", "top three clients", "credit issues",
         "past-due balance", "dispute"],
        conditional="hosting"),
    Question("Q78", "10. Hosting and third-party arrangements",
        "Please describe the Borrower's rights with respect to hosted machines in "
        "a client default (lien, possessory security, self-help, ability to operate "
        "for own account).",
        ["client default", "possessory security", "self-help", "operate for own account",
         "hosted machine lien"],
        conditional="hosting"),
    Question("Q79", "10. Hosting and third-party arrangements",
        "If the Borrower is itself a hosted customer at any site, please provide "
        "the same detail from the reverse perspective (hosting provider, pricing, "
        "term, remedies available to the Borrower).",
        ["hosted customer", "hosting provider", "reverse hosting", "remedies",
         "hosted as client"],
        conditional="hosting"),
]


# ── SECTION 11 — BITCOIN TREASURY AND CUSTODY (always asked) ──────────────────

S11 = [
    Question("Q80", "11. Bitcoin treasury and custody",
        "Please state the current Bitcoin treasury balance (BTC), its location "
        "(custodian, wallet, cold / hot split), and the historical inflow-outflow "
        "over the last twelve (12) months.",
        ["BTC balance", "treasury balance", "custodian", "cold wallet", "hot wallet",
         "inflow outflow", "BTC holdings"]),
    Question("Q81", "11. Bitcoin treasury and custody",
        "Please describe the Bitcoin treasury policy (HODL, sell-to-cover OpEx, "
        "partial monetization, yield strategy) and the governance around deviations "
        "from policy.",
        ["treasury policy", "HODL", "sell-to-cover", "monetization", "yield strategy",
         "policy deviation"]),
    Question("Q82", "11. Bitcoin treasury and custody",
        "Please identify all custody counterparties used (qualified custodian, "
        "self-custody, multisig providers) and attach the master custody agreements. "
        "BTSF will expect any pledged BTC to be held by a qualified institutional "
        "custodian acceptable to BTSF (e.g., Anchorage Digital) or under a "
        "control-account / multisig arrangement with BTSF participation.",
        ["custody counterparty", "qualified custodian", "self custody", "multisig",
         "Anchorage", "BitGo", "Coinbase Custody", "Fireblocks", "custody agreement"]),
    Question("Q83", "11. Bitcoin treasury and custody",
        "Please describe the wallet architecture, signing policies, and key-management "
        "procedures (number and identity of signers, M-of-N, cold-storage handling, "
        "HSM usage, disaster-recovery protocols).",
        ["wallet architecture", "signing policy", "key management", "M-of-N",
         "cold storage", "HSM", "disaster recovery"]),
    Question("Q84", "11. Bitcoin treasury and custody",
        "Please describe the Borrower's approach to any Bitcoin-denominated yield "
        "activity (lending, staking-equivalent, options, structured products) and "
        "related counterparty exposure.",
        ["BTC yield", "BTC lending", "options", "structured product",
         "counterparty exposure", "rehypothecation"]),
    Question("Q85", "11. Bitcoin treasury and custody",
        "Please provide evidence of on-chain balances (verifiable addresses, "
        "custodian attestations, or third-party proof-of-reserves) as of the most "
        "recent month end.",
        ["on-chain balance", "verifiable address", "custodian attestation",
         "proof of reserves", "PoR"]),
]


# ── SECTION 12 — RISK MANAGEMENT AND INSURANCE (always asked) ─────────────────

S12 = [
    Question("Q86", "12. Risk management and insurance",
        "Please provide an overview of the Borrower's risk-management framework, "
        "including risk register, key risk indicators, escalation procedures, and "
        "board-level oversight.",
        ["risk management", "risk register", "KRI", "key risk indicator",
         "escalation", "board oversight"]),
    Question("Q87", "12. Risk management and insurance",
        "Please describe any enterprise risk committee, treasury committee, or "
        "investment committee, including membership and meeting cadence.",
        ["risk committee", "treasury committee", "investment committee",
         "committee membership", "meeting cadence"]),
    Question("Q88", "12. Risk management and insurance",
        "Please provide copies of all insurance policies (property, equipment, "
        "business interruption, general liability, cyber, D&O, crime / digital-asset, "
        "environmental), with insurer, broker, limits, deductibles, and annual "
        "premium. Please highlight any material exclusions.",
        ["insurance", "property insurance", "business interruption", "D&O",
         "cyber insurance", "digital asset insurance", "PLL", "pollution liability",
         "exclusion", "deductible"]),
    Question("Q89", "12. Risk management and insurance",
        "Please describe the claims history over the last five (5) years.",
        ["claims history", "insurance claim", "5 years", "loss history"]),
    Question("Q90", "12. Risk management and insurance",
        "Please describe cybersecurity controls (network segmentation, MFA, "
        "privileged-access management, endpoint detection, penetration testing, "
        "incident-response plan, SOC / SIEM usage) and any incidents in the last "
        "36 months.",
        ["cybersecurity", "network segmentation", "MFA", "PAM", "endpoint detection",
         "pen test", "incident response", "SOC", "SIEM", "cyber incident"]),
    Question("Q91", "12. Risk management and insurance",
        "Please provide the Borrower's business continuity and disaster recovery "
        "plan (documented, tested, last test date).",
        ["business continuity", "BCP", "disaster recovery", "DR plan", "last test",
         "BC test"]),
]


# ── SECTION 13 — LEGAL, TAX, AND REGULATORY (always asked) ────────────────────

S13 = [
    Question("Q92", "13. Legal, tax, and regulatory",
        "Please confirm there is no material outstanding litigation, arbitration, "
        "or regulatory action pending or threatened against the Borrower or any "
        "affiliate. Please list any matter with potential exposure above $100,000.",
        ["litigation", "arbitration", "regulatory action", "pending dispute",
         "threatened", "PACER", "$100,000 exposure"]),
    Question("Q93", "13. Legal, tax, and regulatory",
        "Please list all governmental, regulatory, or tax authority inquiries, "
        "audits, or investigations in the last three (3) years, open or closed.",
        ["regulatory inquiry", "tax audit", "investigation", "government inquiry",
         "3 years"]),
    Question("Q94", "13. Legal, tax, and regulatory",
        "Please describe the regulatory status of the Borrower's activities in each "
        "operating jurisdiction (licenses required, licenses held, registration "
        "status, any sanctions / trade-control considerations).",
        ["regulatory status", "license", "registration", "sanctions",
         "trade control", "OFAC"]),
    Question("Q95", "13. Legal, tax, and regulatory",
        "Please describe the Borrower's AML / KYC framework (customer / counterparty "
        "onboarding, sanctions screening, transaction monitoring, suspicious-activity "
        "reporting) and any audit findings or regulatory feedback.",
        ["AML", "KYC", "onboarding", "sanctions screening", "transaction monitoring",
         "SAR", "suspicious activity"]),
    Question("Q96", "13. Legal, tax, and regulatory",
        "Please describe the tax residence, primary tax regimes applicable (income "
        "tax, VAT / sales tax, withholding, customs / import duty on ASICs), and "
        "any tax rulings or concessions the Borrower relies on.",
        ["tax residence", "income tax", "VAT", "sales tax", "withholding",
         "import duty", "ASIC duty", "tax ruling"]),
    Question("Q97", "13. Legal, tax, and regulatory",
        "Please describe the current effective tax rate, any net operating losses "
        "or tax credits carried forward, any transfer-pricing arrangements, and any "
        "material uncertain tax positions.",
        ["effective tax rate", "NOL", "net operating loss", "tax credit",
         "transfer pricing", "uncertain tax position"]),
    Question("Q98", "13. Legal, tax, and regulatory",
        "Please describe any tax exemptions, holidays, or special-zone benefits "
        "(QOZ, FTZ, enterprise zone, renewable-energy credits) that apply to the "
        "Borrower or its sites, and the remaining term of each.",
        ["tax exemption", "tax holiday", "QOZ", "FTZ", "enterprise zone",
         "renewable energy credit", "PTC", "ITC"]),
    Question("Q99", "13. Legal, tax, and regulatory",
        "Please list all material permits, licenses, and authorizations (power, "
        "environmental, construction, telecom, mining / data-center license) with "
        "issuer, validity period, and renewal cadence.",
        ["permit", "license", "authorization", "power permit", "environmental permit",
         "construction permit", "data center license"]),
    Question("Q100", "13. Legal, tax, and regulatory",
        "Please identify BTSF-facing regulatory or approval requirements for the "
        "transaction (for example, foreign-investment review, energy-regulator "
        "consent, landlord consent, existing-lender consent, public-utility "
        "commission filings).",
        ["foreign investment review", "CFIUS", "energy regulator consent",
         "landlord consent", "existing lender consent", "PUC filing"]),
]


# ── SECTION 14 — ENVIRONMENTAL, SOCIAL, AND GOVERNANCE (ESG) (always asked) ───

S14 = [
    Question("Q101", "14. Environmental, social, and governance (ESG)",
        "Please describe the energy mix (renewable / low-carbon / fossil) powering "
        "the fleet, and the Borrower's position on carbon accounting and any "
        "voluntary offsets or certificates purchased.",
        ["energy mix", "renewable", "low carbon", "fossil", "carbon accounting",
         "offset", "REC", "certificate"]),
    Question("Q102", "14. Environmental, social, and governance (ESG)",
        "Please describe any environmental impact assessments, community "
        "consultations, or benefit agreements associated with the sites.",
        ["environmental impact", "EIA", "community consultation",
         "community benefit agreement", "stakeholder"]),
    Question("Q103", "14. Environmental, social, and governance (ESG)",
        "Please describe any social, community, or local-employment initiatives "
        "that the Borrower considers material to maintaining its social license "
        "to operate.",
        ["community initiative", "local employment", "social license",
         "community engagement"]),
    Question("Q104", "14. Environmental, social, and governance (ESG)",
        "Please describe any ESG-related commitments made to lenders, investors, "
        "or regulators, and any ongoing reporting obligations.",
        ["ESG commitment", "reporting obligation", "sustainability reporting",
         "investor commitment"]),
]


# ── SECTION 15 — DISTRESSED AND SPECIAL-SITUATIONS (conditional) ──────────────
# Entire section gated by `distressed` signal.

S15 = [
    Question("Q105", "15. Distressed and special-situations",
        "Please provide a narrative description of the events leading to the current "
        "stress (operational, commercial, financial, legal, regulatory), with dates "
        "and order of magnitude.",
        ["distress narrative", "stress event", "operational stress", "financial stress",
         "chronology"],
        conditional="distressed"),
    Question("Q106", "15. Distressed and special-situations",
        "Please provide the current capital stack, including for each instrument: "
        "holder(s), principal, accrued interest / dividends, maturity, security, "
        "ranking, and any cross-default or cross-acceleration links.",
        ["capital stack distressed", "accrued interest", "ranking",
         "cross-default", "cross-acceleration"],
        conditional="distressed"),
    Question("Q107", "15. Distressed and special-situations",
        "Please provide a schedule of all past-due and accrued obligations (interest, "
        "principal, trade payables, taxes, rent, power invoices, payroll), with aging.",
        ["past due", "accrued obligation", "aging", "trade payable", "payroll due",
         "rent arrears"],
        conditional="distressed"),
    Question("Q108", "15. Distressed and special-situations",
        "Please list all events of default, covenant breaches, notices, and "
        "reservation-of-rights letters received in the last twenty-four (24) months, "
        "and the current status of each.",
        ["event of default", "covenant breach", "reservation of rights",
         "default notice", "EoD"],
        conditional="distressed"),
    Question("Q109", "15. Distressed and special-situations",
        "Please list all forbearance agreements, standstills, amendments, or waivers "
        "in effect and attach the executed documents.",
        ["forbearance", "standstill", "amendment", "waiver", "executed document"],
        conditional="distressed"),
    Question("Q110", "15. Distressed and special-situations",
        "Please describe any active creditor negotiations, ad-hoc groups, or "
        "steering committees, and the Borrower's current engagement with each.",
        ["creditor negotiation", "ad-hoc group", "steering committee",
         "creditor group"],
        conditional="distressed"),
    Question("Q111", "15. Distressed and special-situations",
        "Please disclose any pending or threatened insolvency, receivership, "
        "chapter 11, administration, or foreign equivalent process, and any "
        "strategy to avoid or accelerate it.",
        ["insolvency", "receivership", "chapter 11", "administration",
         "bankruptcy filing"],
        conditional="distressed"),
    Question("Q112", "15. Distressed and special-situations",
        "Please list all pledges, liens, and security interests granted across the "
        "corporate group (UCC-1 filings, PPSA, mortgages, share pledges, account "
        "controls, ASIC chattel pledges, energy-contract collateral), with ranking "
        "and outstanding balances. Please state explicitly any assets that are "
        "currently unencumbered.",
        ["pledge list", "lien schedule", "UCC-1", "PPSA", "chattel pledge",
         "unencumbered asset", "ranking", "account control"],
        conditional="distressed"),
    Question("Q113", "15. Distressed and special-situations",
        "Please describe any \"surviving obligations\" from earlier transactions "
        "(residual guarantees, indemnities, earn-outs, contingent consideration, "
        "environmental liabilities).",
        ["surviving obligation", "residual guarantee", "indemnity", "earn-out",
         "contingent consideration", "environmental liability"],
        conditional="distressed"),
    Question("Q114", "15. Distressed and special-situations",
        "Please describe the turnaround plan (operational, financial, strategic), "
        "including the specific interventions contemplated, the cash-flow bridge, "
        "and the milestones.",
        ["turnaround plan", "intervention", "cash flow bridge", "milestone",
         "operational turnaround"],
        conditional="distressed"),
    Question("Q115", "15. Distressed and special-situations",
        "Please identify the advisors engaged (financial advisor, restructuring "
        "counsel, independent director, CRO) and their roles.",
        ["financial advisor", "restructuring counsel", "CRO",
         "chief restructuring officer", "independent director"],
        conditional="distressed"),
    Question("Q116", "15. Distressed and special-situations",
        "Please provide the 13-week cash-flow forecast and the assumptions, "
        "including minimum-cash waterfall and any already-identified gaps.",
        ["13-week", "cash flow forecast", "TWCF", "minimum cash waterfall",
         "funding gap"],
        conditional="distressed"),
    Question("Q117", "15. Distressed and special-situations",
        "Please describe the Borrower's prior restructuring or workout history "
        "(if any) and the outcomes.",
        ["prior restructuring", "workout history", "prior workout", "outcome"],
        conditional="distressed"),
    Question("Q118", "15. Distressed and special-situations",
        "Please describe, at a high level, the exit scenarios the Borrower is "
        "considering (refinance, sale, partial asset sale, merger, equitization, "
        "liquidation) and the preferred path.",
        ["exit scenario", "refinance", "asset sale", "equitization", "liquidation",
         "preferred path"],
        conditional="distressed"),
]


# ── SECTION 16 — PROPOSED COLLATERAL AND CREDIT STRUCTURE (always asked) ──────

S16 = [
    Question("Q119", "16. Proposed collateral and credit structure",
        "Please describe the proposed collateral package: assets to be pledged, "
        "form of security (pledge, mortgage, chattel, control agreement, account "
        "control, lien on pool routing rights), and perfection steps by jurisdiction.",
        ["collateral package", "pledge", "chattel", "control agreement",
         "account control", "pool routing rights", "perfection"]),
    Question("Q120", "16. Proposed collateral and credit structure",
        "Please describe any known impediments to granting a first-ranking lien on "
        "the contemplated collateral (existing liens, landlord waivers needed, "
        "regulatory consents, change-of-control notices).",
        ["first-ranking lien", "impediment", "landlord waiver", "regulatory consent",
         "COC notice", "prior lien"]),
    Question("Q121", "16. Proposed collateral and credit structure",
        "Please confirm the Borrower's willingness to grant BTSF: (i) a control "
        "account for mining revenue, with the ability to route pool payouts directly "
        "to a BTSF-controlled wallet or segregated custody account; (ii) a pledge "
        "and/or assignment of mining-pool routing rights and the related API access; "
        "(iii) appropriate reps and covenants around pool selection, custody changes, "
        "and wallet architecture; (iv) information and inspection rights, including "
        "site access and real-time monitoring of hashrate, uptime, and energy "
        "consumption.",
        ["control account", "BTSF-controlled wallet", "pool routing pledge",
         "API access", "inspection right", "real-time monitoring"]),
    Question("Q122", "16. Proposed collateral and credit structure",
        "Please describe any commercial or operational reasons why the Borrower "
        "could not, or would prefer not to, accept a BTSF-controlled wallet as the "
        "immediate recipient of pool payouts, and any alternative constructions "
        "the Borrower would propose.",
        ["BTSF wallet objection", "operational reason", "alternative construction",
         "payout wallet"]),
    Question("Q123", "16. Proposed collateral and credit structure",
        "Please identify any sponsor, parent, or affiliate willing to provide a "
        "guarantee or support commitment, and on what terms.",
        ["sponsor guarantee", "parent guarantee", "support commitment",
         "credit support"]),
    Question("Q124", "16. Proposed collateral and credit structure",
        "Please describe the Borrower's view on financial and operational covenants "
        "it expects to accept (LTV, DSCR, minimum hashrate, minimum uptime, maximum "
        "power cost, minimum liquidity, Bitcoin-denominated reserve).",
        ["covenant", "LTV", "DSCR", "minimum hashrate", "minimum uptime",
         "maximum power cost", "minimum liquidity", "BTC reserve"]),
    Question("Q125", "16. Proposed collateral and credit structure",
        "Please describe any existing intercreditor dynamics that will need to be "
        "resolved prior to, or at, closing.",
        ["intercreditor", "ICA", "existing lender", "closing condition",
         "intercreditor resolution"]),
]


# ── SECTION 17 — REFERENCES (always asked) ────────────────────────────────────

S17 = [
    Question("Q126", "17. References",
        "Please provide two or three references who can speak to the Borrower's "
        "operational track record (equipment manufacturer, energy counterparty, "
        "pool operator, existing lender, sponsor co-investor).",
        ["reference", "track record", "equipment manufacturer reference",
         "pool operator reference", "lender reference"]),
    Question("Q127", "17. References",
        "Please list all prior and other investors who have considered this "
        "opportunity, including the outcome and (to the extent you are willing "
        "to share) the reasons behind any decline.",
        ["prior investor", "prior review", "decline reason", "outcome"]),
]


# ── SECTION 18 — OTHER (always asked) ─────────────────────────────────────────

S18 = [
    Question("Q128", "18. Other",
        "Are there any other facts, matters, or circumstances that a prudent "
        "lender would wish to be aware of in evaluating this transaction? "
        "Please disclose.",
        ["other disclosure", "prudent lender", "material fact", "additional disclosure"]),
]


# =============================================================================
# DEEP-DIVE BLOCKS (signal-gated complements to the standard template)
# Kept from v1.0 — they expand on specific site-type cases not explicitly
# detailed in the PDF. Activated automatically when the signal fires.
# =============================================================================

BLOCK_GREENFIELD = [
    Question("G.1", "Deep-dive — Greenfield",
        "Interconnection application status and utility queue position.",
        ["interconnection application", "queue", "utility", "ERCOT queue", "FEA status"]),
    Question("G.2", "Deep-dive — Greenfield",
        "Site control agreement — conditions precedent to closing "
        "(site ownership, lease, option).",
        ["site control", "lease agreement", "option", "conditions precedent", "closing"]),
    Question("G.3", "Deep-dive — Greenfield",
        "Has a geotechnical study been completed?",
        ["geotechnical", "soil study", "ground conditions", "foundation"]),
    Question("G.4", "Deep-dive — Greenfield",
        "What civil works are required before electrical work can commence? "
        "(grading, access roads, foundations)",
        ["civil works", "grading", "access road", "foundation", "site preparation"]),
    Question("G.5", "Deep-dive — Greenfield",
        "What is the all-in EPC cost estimate and which contractor has been engaged?",
        ["EPC", "contractor", "cost estimate", "construction cost", "engineering"]),
    Question("G.6", "Deep-dive — Greenfield",
        "What is the expected time from NTP (Notice to Proceed) to first energisation?",
        ["NTP", "notice to proceed", "energisation", "timeline", "schedule"]),
]

BLOCK_BROWNFIELD = [
    Question("B.1", "Deep-dive — Brownfield",
        "Has a Phase 2 ESA been recommended or completed?",
        ["Phase 2 ESA", "phase 2", "environmental assessment", "soil sampling", "groundwater"]),
    Question("B.2", "Deep-dive — Brownfield",
        "Who is the environmental indemnitor and what is their financial capacity "
        "to stand behind the indemnity?",
        ["environmental indemnitor", "indemnity", "Flint Hills", "Koch Industries",
         "indemnification", "financial capacity"]),
    Question("B.3", "Deep-dive — Brownfield",
        "Are there any no-build zones or excavation restrictions that reduce the "
        "usable developable area?",
        ["no-build zone", "buffer", "RCRA buffer", "excavation restriction",
         "buildable area", "usable area"]),
    Question("B.4", "Deep-dive — Brownfield",
        "Are there any easements granted to prior owners that survive the lease?",
        ["easement", "prior owner", "Flint Hills easement", "remediation easement",
         "pipeline easement", "surviving easement"]),
]

BLOCK_EXISTING_INFRASTRUCTURE = [
    Question("EI.1", "Deep-dive — Existing Infrastructure",
        "Has an independent electrical contractor conducted a health assessment of "
        "the transformers and electrical infrastructure within the last 12 months?",
        ["health assessment", "transformer testing", "electrical inspection",
         "Colliers", "EPS", "health report"]),
    Question("EI.2", "Deep-dive — Existing Infrastructure",
        "Has an arc flash study been completed on the switchgear?",
        ["arc flash", "arc flash study", "switchgear", "electrical safety"]),
    Question("EI.3", "Deep-dive — Existing Infrastructure",
        "What pre-energisation maintenance is required, what is the estimated cost, "
        "and who bears it?",
        ["maintenance", "pre-energisation", "repair cost", "maintenance cost",
         "who pays", "responsible party"]),
]

BLOCK_BTM_GAS = [
    Question("BTM.1", "Deep-dive — BTM Gas",
        "Which natural gas pipelines serve the site and what is the confirmed "
        "deliverable capacity (Dth/day)?",
        ["pipeline", "Dth/day", "Oneok", "EverLine", "gas capacity", "deliverable"]),
    Question("BTM.2", "Deep-dive — BTM Gas",
        "What is the gas pricing basis and historical basis differential "
        "(e.g. Waha vs Henry Hub)?",
        ["Waha", "Henry Hub", "gas basis", "pricing basis", "IFERC", "WASP"]),
    Question("BTM.3", "Deep-dive — BTM Gas",
        "Has a gas supply agreement been executed? What are the take-or-pay obligations?",
        ["gas supply agreement", "take-or-pay", "gas contract", "supply agreement"]),
    Question("BTM.5", "Deep-dive — BTM Gas",
        "Is there an uptime guarantee on BTM generation?",
        ["uptime guarantee", "availability", "BTM uptime", "generator SLA"]),
    Question("BTM.7", "Deep-dive — BTM Gas",
        "What is the all-in LCOE for BTM generation vs. grid power?",
        ["LCOE", "levelised cost", "cost comparison", "BTM cost", "$/MWh BTM"]),
    Question("BTM.8", "Deep-dive — BTM Gas",
        "Pre-payment risk: has the counterparty's delivery capacity been confirmed "
        "by an independent party?",
        ["pre-payment risk", "delivery capacity", "counterparty risk", "gas delivery"]),
]

BLOCK_BTM_RENEWABLE = [
    Question("BTM.4", "Deep-dive — BTM Renewable",
        "What is the wind/solar pricing basis and historical generation profile?",
        ["solar pricing", "wind pricing", "generation profile", "capacity factor", "curtailment"]),
    Question("BTM.6", "Deep-dive — BTM Renewable",
        "Will the BTM renewable installation be backed by a grid connection to "
        "guarantee minimum uptime?",
        ["grid backup", "grid connection", "minimum uptime", "renewable backup"]),
]

BLOCK_HOSTING = [
    Question("H.1", "Deep-dive — Hosting",
        "How many hosting clients are currently contracted and what is the total "
        "contracted MW?",
        ["hosting clients", "contracted MW", "number of clients", "total hosted"]),
    Question("H.2", "Deep-dive — Hosting",
        "For the most significant contracts (≥10% of customer base): MW, rate "
        "($/kWh), term, expiry, notice period, termination rights, make-whole provisions.",
        ["hosting rate", "$/kWh", "contract term", "termination", "make-whole", "notice period"]),
    Question("H.3", "Deep-dive — Hosting",
        "What security interest does the operator hold over client machines in "
        "case of default?",
        ["security interest", "client machines", "default", "UCC-1", "lien on machines"]),
    Question("H.4", "Deep-dive — Hosting",
        "Who is responsible for client machine insurance?",
        ["machine insurance", "client insurance", "insurance responsibility"]),
    Question("H.5", "Deep-dive — Hosting",
        "Concentration risk: is any single client equal to or above 20% of total "
        "hosted MW?",
        ["concentration", "single client", "20%", "largest client", "client concentration"]),
    Question("H.6", "Deep-dive — Hosting",
        "What is the historical client churn and contract renewal rate?",
        ["churn", "renewal rate", "client retention", "turnover"]),
    Question("H.7", "Deep-dive — Hosting",
        "What is hosting revenue as a percentage of total facility revenue?",
        ["hosting revenue", "% revenue", "revenue split", "prop vs hosted revenue"]),
]

BLOCK_EXISTING_DEBT = [
    Question("DC.1", "Deep-dive — Existing Debt",
        "Full indebtedness schedule: lender name, outstanding balance, maturity "
        "date, interest rate, security granted, cross-default provisions.",
        ["lender", "balance", "maturity", "interest rate", "security", "cross-default"]),
    Question("DC.2", "Deep-dive — Existing Debt",
        "Are there any negative pledge clauses or restricted payment provisions?",
        ["negative pledge", "restricted payment", "covenant", "payment restriction"]),
    Question("DC.3", "Deep-dive — Existing Debt",
        "Does any existing lender hold a security interest over assets proposed as "
        "collateral for the new facility?",
        ["existing security interest", "prior lien", "collateral conflict", "first lien"]),
    Question("DC.4", "Deep-dive — Existing Debt",
        "Are there any change-of-control provisions that would be triggered by the "
        "proposed transaction?",
        ["change of control", "COC", "triggered by", "transfer restriction"]),
    Question("DC.5", "Deep-dive — Existing Debt",
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
    - Sections 1–9, 11–14, 16–18 of the standard template (always asked)
    - Section 10 Hosting  (gated by `hosting` signal)
    - Section 15 Distressed (gated by `distressed` signal)
    - Energy section conditional questions (gated by ppa_present / prior_operations)
    - Deep-dive blocks (G/B/EI/BTM/H/DC) — gated by corresponding signals
    """
    questions: List[Question] = []

    # ── Always-asked template sections (1–9, 11–14, 16–18) ───────────────────
    questions.extend(S1)        # 1.  General information
    questions.extend(S2)        # 2.  Corporate and ownership
    questions.extend(S3)        # 3.  Management and operations team
    questions.extend(S4)        # 4.  Historical and projected financials
    questions.extend(S5)        # 5.  Capital structure and existing indebtedness
    questions.extend(S6)        # 6.  ASIC fleet and equipment
    questions.extend(S7)        # 7.  Sites and infrastructure
    questions.extend(S8_ALWAYS) # 8.  Energy (core)
    questions.extend(S9)        # 9.  Mining operations, pool, revenue

    # ── Section 10 — Hosting (only if hosting signal is true) ────────────────
    for q in S10:
        if q.conditional is None or signals.get(q.conditional, False):
            questions.append(q)

    questions.extend(S11)       # 11. Bitcoin treasury and custody
    questions.extend(S12)       # 12. Risk management and insurance
    questions.extend(S13)       # 13. Legal, tax, regulatory
    questions.extend(S14)       # 14. ESG

    # ── Section 15 — Distressed (only if distressed signal is true) ──────────
    for q in S15:
        if q.conditional is None or signals.get(q.conditional, False):
            questions.append(q)

    questions.extend(S16)       # 16. Proposed collateral and credit structure
    questions.extend(S17)       # 17. References
    questions.extend(S18)       # 18. Other

    # ── Section 8 Energy — signal-specific follow-ups ────────────────────────
    for q in S8_CONDITIONAL:
        if q.conditional is None or signals.get(q.conditional, False):
            questions.append(q)

    # ── Deep-dive blocks (kept from v1.0) ────────────────────────────────────
    for signal_key, block in CONDITIONAL_BLOCKS.items():
        if signals.get(signal_key, False):
            questions.extend(block)

    return questions
