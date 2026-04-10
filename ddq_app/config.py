"""
DDQ Automation Tool — Configuration
BTSF | Bitcoin Mining Credit Due Diligence
"""

import os

# ── API ───────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL             = "claude-sonnet-4-20250514"
MAX_TOKENS        = 4096

# ── Chunking ──────────────────────────────────────────────────────────────────
CHUNK_SIZE        = 1200   # chars per chunk sent to Claude
CHUNK_OVERLAP     = 200    # overlap between consecutive chunks
MAX_CHUNKS_PER_Q  = 12     # max chunks retrieved per question

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR        = os.path.join(os.path.dirname(__file__), "output")

# ── Confidence colours (for Word output) ─────────────────────────────────────
COLOUR_ANSWERED   = "1D6A3A"   # dark green
COLOUR_PARTIAL    = "B7770D"   # amber
COLOUR_GAP        = "C0392B"   # red
COLOUR_NA         = "5A6472"   # grey
COLOUR_NAVY       = "0D1F3C"
COLOUR_STEEL      = "2E5FA3"
COLOUR_GOLD       = "B8942A"
COLOUR_LGRAY      = "F4F5F7"
