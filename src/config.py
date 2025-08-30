import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/auto")

ASR_MODEL_SIZE = os.getenv("ASR_MODEL_SIZE", "base")  # tiny/base/small/medium/large-v3
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "gtts")      # only 'gtts' implemented in this prototype

SAMPLE_RATE = 16000
CHANNELS = 1
MAX_RECORD_SECONDS = 8      # simple PTT-style recording window
LANG_HINT = "hi"            # Hindi
