# Speech-to-text using faster-whisper (ctranslate2 backend).
# Model size is configurable via env. Default: 'base' but i dont have much computation power in my current laptop so i have used 'tiny'.

from faster_whisper import WhisperModel
from pathlib import Path
from typing import Tuple
from .config import ASR_MODEL_SIZE, LANG_HINT
from .utils.logger import logger

_model_cache = {}

def _get_model(size: str) -> WhisperModel:
    # reuse across calls to avoid repeated loading cost
    if size not in _model_cache:
        logger.info(f"Loading faster-whisper model: {size}. This may take a while on first run.")
        # Forced CPU mode to avoid CUDA/cuDNN issues on Windows

        _model_cache[size] = WhisperModel(size, device="cpu", compute_type="int8")
    return _model_cache[size]

def transcribe_wav(path: Path) -> Tuple[str, float]:
    model = _get_model(ASR_MODEL_SIZE)
    segments, info = model.transcribe(str(path), language=LANG_HINT, vad_filter=True)
    text = " ".join(seg.text.strip() for seg in segments).strip()
    confidence = getattr(info, 'language_probability', 0.0) if hasattr(info, 'language_probability') else 0.0
    logger.info(f"ASR: '{text}' (conf≈{confidence:.2f})")
    return text, confidence
