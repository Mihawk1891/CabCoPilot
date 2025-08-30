# Minimal audio I/O utilities. Uses sounddevice+soundfile to record WAV and playback.
# If playback fails (e.g., missing audio device), we fail gracefully and print text instead.

import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
from pathlib import Path
from .config import SAMPLE_RATE, CHANNELS, MAX_RECORD_SECONDS
from .utils.logger import logger

def record_push_to_talk(out_path: Path) -> Path:
    """Record audio for a fixed window after user hits Enter. Saves mono WAV.    Rationale: simpler than VAD for a quick prototype.

    """
    input("\n[PTT] बोलना शुरू करने के लिए Enter दबाएँ, रिकॉर्डिंग {} सेकंड तक चलेगी...".format(MAX_RECORD_SECONDS))
    duration = MAX_RECORD_SECONDS
    logger.info(f"Recording for {duration}s at {SAMPLE_RATE}Hz...")
    try:
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                        channels=CHANNELS, dtype='float32')
        sd.wait()
        data = np.squeeze(recording)
        sf.write(out_path, data, SAMPLE_RATE)
        logger.info(f"Saved recording -> {out_path}")
        return out_path
    except Exception as e:
        logger.error(f"Recording failed: {e}")
        raise

def play_wav(path: Path) -> None:
    """Naive WAV playback using soundfile+sounddevice."""
    try:
        data, sr = sf.read(path, dtype='float32', always_2d=False)
        logger.info(f"Playing TTS audio ({path.name})...")
        sd.play(data, sr)
        sd.wait()
    except Exception as e:
        logger.error(f"Playback failed: {e}")

