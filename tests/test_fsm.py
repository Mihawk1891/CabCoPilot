import pytest
from src.conversation_fsm import VoiceBotFSM, State

def test_nominal_flow():
    fsm = VoiceBotFSM()
    # INIT -> ASK_REG
    t = fsm.next("मैं 2 घंटे से ऑनलाइन हूँ पर कोई राइड नहीं मिल रही", "complaint")
    assert t.state == State.ASK_REG
    # ASK_REG -> CHECKING (yes)
    t = fsm.next("हाँ", "confirm_yes")
    assert t.state == State.CHECKING
    # CHECKING -> SUGGEST
    t = fsm.next("", "unknown")
    assert t.state == State.SUGGEST
    # SUGGEST -> GOODBYE
    t = fsm.next("ठीक है", "unknown")
    assert t.state == State.GOODBYE
    # GOODBYE -> END
    t = fsm.next("", "unknown")
    assert fsm.done()

def test_unexpected_then_recover():
    fsm = VoiceBotFSM()
    # INIT -> ASK_REG
    t = fsm.next("कुछ भी", "unknown")
    assert t.state == State.ASK_REG
    # Unexpected reply -> clarify
    t = fsm.next("समझ नहीं आया", "unknown")
    assert t.state == State.ASK_REG and "रजिस्टर्ड" in t.bot_text
    # Then yes -> checking
    t = fsm.next("जी हाँ", "confirm_yes")
    assert t.state == State.CHECKING
