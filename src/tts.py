# Text-to-speech for Hindi using gTTS (Google TTS). Requires internet & ffmpeg (for MP3->WAV via pydub).
# We keep it simple: generate MP3 then convert to WAV for consistent playback.

from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from .utils.logger import logger

def synthesize_hi_to_wav(text: str, out_wav: Path) -> Path:
    try:
        mp3_path = out_wav.with_suffix('.mp3')
        tts = gTTS(text=text, lang='hi')
        tts.save(mp3_path)
        # Convert MP3 to WAV for playback via sounddevice
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(out_wav, format='wav')
        logger.info(f"TTS synthesized -> {out_wav.name}")
        try:
            mp3_path.unlink(missing_ok=True)
        except Exception:
            pass
        return out_wav
    except Exception as e:
        logger.error(f"TTS failed: {e}")
        raise
