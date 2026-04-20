# BTSF DDQ Automation Tool

Automatically fills a Bitcoin mining credit due diligence questionnaire
from a folder of data room documents using the Claude API.

## How it works

1. **Ingest** — reads all PDF, DOCX, XLSX, TXT files from a local folder
2. **Signal detection** — calls Claude to detect deal-type flags
   (greenfield, brownfield, hosting, existing debt, etc.)
3. **Question assembly** — builds the active question set:
   minimum questions always asked + conditional blocks unlocked by signals
4. **Answer generation** — for each question, retrieves relevant chunks
   and calls Claude to generate an answer with source citation and confidence flag
5. **Word export** — outputs a formatted .docx DDQ with colour-coded answers

## Setup

```bash
# Install dependencies
pip install anthropic pdfplumber docx2txt python-docx openpyxl

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Usage

```bash
cd ddq_app

# Basic usage
python main.py --folder /path/to/data_room --deal "Project Broadstone"

# With site details
python main.py \
  --folder /path/to/data_room \
  --deal "Project Broadstone" \
  --site "2501 S. Grandview Ave, Odessa TX" \
  --mw "65 MW"

# Quiet mode (suppress per-question progress)
python main.py --folder /path/to/data_room --deal "Project XXX" --quiet
```

## Output

The tool generates a Word document in `ddq_app/output/` named:
`DDQ_<deal_name>_<timestamp>.docx`

Each answer is colour-coded:
- **Green** — Answered, sourced from data room (with citation)
- **Amber** — Partial answer, specific gap noted
- **Red** — Not found in data room, must be provided manually

## Standard template

The question set is mapped **1:1 to the BTSF Mining Finance DDQ v1.1 PDF**
(18 sections, Q1–Q128). Sections 1–9, 11–14 and 16–18 are always asked;
sections 10 (Hosting) and 15 (Distressed / special situations) are gated
by signals so they only appear when relevant.

| # | Section | Questions | Gating |
|---|---------|----------:|--------|
| 1 | General information and deal overview | Q1–Q7 | always |
| 2 | Corporate and ownership | Q8–Q16 | always |
| 3 | Management, organization, and operations team | Q17–Q22 | always |
| 4 | Historical and projected financials | Q23–Q30 | always |
| 5 | Capital structure and existing indebtedness | Q31–Q35 | always |
| 6 | ASIC fleet and equipment | Q36–Q44 | always |
| 7 | Sites and infrastructure | Q45–Q54 | always |
| 8 | Energy | Q55–Q68 | core always; PPA/hedging/prior-ops items gated |
| 9 | Mining operations, pool, and revenue management | Q69–Q75 | always |
| 10 | Hosting and third-party arrangements | Q76–Q79 | `hosting` signal |
| 11 | Bitcoin treasury and custody | Q80–Q85 | always |
| 12 | Risk management and insurance | Q86–Q91 | always |
| 13 | Legal, tax, and regulatory | Q92–Q100 | always |
| 14 | ESG | Q101–Q104 | always |
| 15 | Distressed and special-situations | Q105–Q118 | `distressed` signal |
| 16 | Proposed collateral and credit structure | Q119–Q125 | always |
| 17 | References | Q126–Q127 | always |
| 18 | Other | Q128 | always |

## Deep-dive blocks

In addition to the standard template, the tool can layer in deal-type
deep-dive blocks when the corresponding signals are detected. These expand
on topics not fully covered by the standard template:

| Signal | Block activated |
|--------|----------------|
| Greenfield site | G.1–G.6: Interconnection, EPC, geotechnical |
| Brownfield site | B.1–B.4: ESA, indemnitor, easements |
| Existing infrastructure | EI.1–EI.3: Health assessment, arc flash, maintenance |
| BTM gas generation | BTM.1–BTM.8: Pipeline, pricing, supply agreement |
| BTM renewable | BTM.4, BTM.6: Solar/wind profile, grid backup |
| Hosting operations | H.1–H.7: Contracts, concentration, churn |
| Existing debt | DC.1–DC.5: Schedule, covenants, COC provisions |

## File structure

```
ddq_app/
├── main.py          # Entry point
├── config.py        # API keys, colours, constants
├── core/
│   ├── ingestion.py # Document reading and chunking
│   ├── signals.py   # Deal-type signal detection
│   ├── questions.py # Full question registry
│   ├── generator.py # Claude answer generation
│   └── writer.py    # Word document export
└── output/          # Generated DDQ documents
```

## Supported file types

PDF, DOCX, DOC, XLSX, XLS, TXT, MD, CSV

## API cost estimate

A typical 20-document data room with 60–80 active questions costs
approximately $0.50–1.50 in Claude API calls and runs in 3–6 minutes.
