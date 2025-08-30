# Entry point. Wires together Audio I/O, STT, FSM, TTS. Hindi-only flow per assessment.
# Tested as a local prototype (push-to-talk).

from src.audio_io import record_push_to_talk, play_wav
from src.stt import transcribe_wav
from src.tts import synthesize_hi_to_wav
from src.conversation_fsm import VoiceBotFSM
from src.llm import classify_intent_hi
import logging
import sys
from pathlib import Path


#import sys
#from pathlib import Path
#from .audio_io import record_push_to_talk, play_wav
#from .stt import transcribe_wav
#from .tts import synthesize_hi_to_wav
#from .conversation_fsm import VoiceBotFSM
#from .llm import classify_intent_hi
#from .utils.logger import logger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voicebot")

ASSET_OUT = Path("/tmp/voicebot_out")
ASSET_OUT.mkdir(parents=True, exist_ok=True)

def say(text: str):
    if not text:
        return
    out = ASSET_OUT / "tts_out.wav"
    wav = synthesize_hi_to_wav(text, out)
    play_wav(wav)

def run():
    logger.info("\n🚀 Hindi Voice Bot (Local Prototype) — PTT mode\n"
                "नोट: बोलने के लिए Enter दबाएँ, ऐप स्वतः 8 सेकंड तक सुनेगा।\n"
                "बातचीत पूरी तरह हिंदी में रखें।\n")

    fsm = VoiceBotFSM()

    # Bot starts after hearing first user line
    # 1) User: complaint
    # 2) Bot: greet+ask reg
    # ... etc per FSM

    # Listen to first user utterance
    user_wav = record_push_to_talk(ASSET_OUT / "user_1.wav")
    user_text, _ = transcribe_wav(user_wav)
    intent = classify_intent_hi(user_text)
    turn = fsm.next(user_text, intent)
    say(turn.bot_text)

    # Loop until END
    step = 2
    while not fsm.done():
        user_wav = record_push_to_talk(ASSET_OUT / f"user_{step}.wav")
        user_text, _ = transcribe_wav(user_wav)
        intent = classify_intent_hi(user_text)
        turn = fsm.next(user_text, intent)
        if turn.bot_text:
            say(turn.bot_text)
        step += 1

    logger.info("\n✅ परिदृश्य पूर्ण हुआ. धन्यवाद!\n")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nबंद किया गया।")
        sys.exit(0)
