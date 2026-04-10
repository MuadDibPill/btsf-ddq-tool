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

## Conditional blocks

The following question blocks are activated only if relevant evidence
is found in the data room:

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
