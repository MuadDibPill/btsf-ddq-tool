"""
DDQ Automation — Answer Generation
For each active question, retrieves relevant chunks and calls Claude
to generate an answer with source citation and confidence flag.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import anthropic

from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from core.ingestion import Chunk, search_chunks, chunks_to_context
from core.questions import Question


# ── Answer data structure ─────────────────────────────────────────────────────

@dataclass
class Answer:
    question:   Question
    text:       str                      # answer text
    confidence: str                      # "answered" | "partial" | "gap" | "n/a"
    sources:    List[str] = field(default_factory=list)   # list of "filename p.N"
    gap_note:   Optional[str] = None     # what is missing, if gap or partial


# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior credit analyst completing a due diligence questionnaire 
for a Bitcoin mining infrastructure financing transaction.

You will be given:
1. A DDQ question
2. Relevant excerpts from the data room documents

Your task is to:
- Answer the question as fully as possible using only the provided document excerpts
- If the documents fully answer the question, give a complete, concise answer
- If the documents partially answer the question, give what you know and clearly state what is missing
- If the documents do not answer the question at all, state that clearly
- Always cite your sources (filename and page number)
- Never invent information not found in the documents
- Be concise and professional — this is a credit document

Response format (JSON only, no markdown fences):
{
  "answer": "Your answer text here. Be specific and cite sources inline.",
  "confidence": "answered|partial|gap",
  "sources": ["filename.pdf p.1", "other_doc.docx p.3"],
  "gap_note": "Description of what is missing (only if confidence is partial or gap, else null)"
}
"""


def _build_prompt(question: Question, context: str) -> str:
    return f"""QUESTION [{question.qid}]: {question.text}

RELEVANT DOCUMENT EXCERPTS:
{context if context.strip() else "[No relevant documents found in data room]"}

Answer the question based solely on the document excerpts above.
Return JSON only."""


# ── Public API ────────────────────────────────────────────────────────────────

def generate_answers(questions: List[Question],
                     chunks: List[Chunk],
                     max_chunks_per_q: int = 12,
                     verbose: bool = True) -> List[Answer]:
    """
    For each question, retrieve relevant chunks and call Claude to generate an answer.
    Returns a list of Answer objects.
    """
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    answers: List[Answer] = []

    total = len(questions)
    for i, q in enumerate(questions, 1):
        if verbose:
            print(f"  [{i}/{total}] {q.qid}: {q.text[:60]}...")

        # Retrieve relevant chunks
        relevant = search_chunks(chunks, q.keywords, max_results=max_chunks_per_q)
        context  = chunks_to_context(relevant, max_chars=8000)

        prompt = _build_prompt(q, context)

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.content[0].text.strip()

            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            import json
            data = json.loads(raw)

            answer = Answer(
                question   = q,
                text       = data.get("answer", ""),
                confidence = data.get("confidence", "gap"),
                sources    = data.get("sources", []),
                gap_note   = data.get("gap_note"),
            )

        except Exception as e:
            print(f"    [WARN] API error for {q.qid}: {e}")
            answer = Answer(
                question   = q,
                text       = "Error generating answer — please complete manually.",
                confidence = "gap",
                gap_note   = f"API error: {str(e)}"
            )

        answers.append(answer)
        if verbose:
            icon = {"answered": "✓", "partial": "~", "gap": "✗"}.get(answer.confidence, "?")
            print(f"    {icon} [{answer.confidence}]")

    return answers
