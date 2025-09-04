# Optional LLM integration via OpenRouter for intent classification / fallback NLG.
# This file is deliberately minimal; we avoid dependence unless OPENROUTER_API_KEY is set.

import requests
from .config import OPENROUTER_API_KEY, OPENROUTER_MODEL
import logging
logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def _headers():
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

def classify_intent_hi(text_hi: str) -> str:
    """Return a coarse intent label in Hindi context: one of {complaint, confirm_yes, confirm_no, unknown}."""
    if not OPENROUTER_API_KEY:
        # Lightweight heuristic fallback
        t = text_hi.strip().lower()
        if any(k in t for k in ["2 घंटे", "दो घंटे", "ride", "राइड", "नहीं मिल", "ऑनलाइन", "गाड़ी", "काम नहीं"]):
            return "complaint"
        if any(k in t for k in ["हाँ", "जी", "haan", "ha", "yes"]):
            return "confirm_yes"
        if any(k in t for k in ["नहीं", "nahin", "nai", "no"]):
            return "confirm_no"
        return "unknown"

    prompt = [
        {"role": "system", "content": "You are a function that returns only one token label from {complaint, confirm_yes, confirm_no, unknown, feedback}."},
        {"role": "user", "content": f"Classify the Hindi user message into one label:\n\n\"\"\"\n{text_hi}\n\"\"\""},
    ]

    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers=_headers(),
            json={
                "model": OPENROUTER_MODEL,
                "messages": prompt,
                "temperature": 0,
                "max_tokens": 3,
            },
            timeout=30
        )
        resp.raise_for_status()
        out = resp.json()
        choice = out.get("choices", [{}])[0].get("message", {}).get("content", "").strip().lower()

        label = "unknown"
        for c in ["complaint", "confirm_yes", "confirm_no", "unknown"]:
            if c in choice:
                label = c
                break

        logger.info(f"LLM intent => {label}")
        return label

    except Exception as e:
        logger.error(f"OpenRouter classify failed: {e}")
        return "unknown"
