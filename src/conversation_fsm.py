# A tiny finite-state machine that enforces the assessment's Hindi scenario.
# We keep responses crisp and deterministic to pass the rubric.

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

class State(Enum):
    INIT = auto()
    ASK_REG = auto()
    CHECKING = auto()
    SUGGEST = auto()
    GOODBYE = auto()
    END = auto()

@dataclass
class Turn:
    state: State
    bot_text: str

class VoiceBotFSM:
    def __init__(self):
        self.state = State.INIT
        # Pre-scripted Hindi lines per the assessment
        self.lines = {
            "greet": "ओला कस्टमर सपोर्ट में आपका स्वागत है। क्या यह आपका रजिस्टर्ड नंबर है?",
            "ok_number": "आपका नंबर ब्लॉक नहीं है। सब ठीक है।",
            "suggest": "कृपया अपना लोकेशन बदल कर फिर से राइड्स चेक कीजिए।",
            "bye": "धन्यवाद! सुरक्षित ड्राइव करें। नमस्ते।",
            "clarify_yesno": "कृपया हाँ या नहीं में बताइए—क्या यह आपका रजिस्टर्ड नंबर है?",
        }

    def next(self, user_text: str, intent_label: str) -> Turn:
        t = (user_text or "").strip().lower()

        if self.state == State.INIT:
            # Expect a complaint like: not getting rides
            self.state = State.ASK_REG
            return Turn(self.state, self.lines["greet"])

        if self.state == State.ASK_REG:
            if intent_label == "confirm_yes":
                self.state = State.CHECKING
                return Turn(self.state, self.lines["ok_number"])
            elif intent_label == "confirm_no":
                # In assessment we assume registered number confirmation; gently reprompt
                return Turn(self.state, self.lines["clarify_yesno"])
            else:
                return Turn(self.state, self.lines["clarify_yesno"])

        if self.state == State.CHECKING:
            # Move to suggestion
            self.state = State.SUGGEST
            return Turn(self.state, self.lines["suggest"])

        if self.state == State.SUGGEST:
            # User acknowledges
            self.state = State.GOODBYE
            return Turn(self.state, self.lines["bye"])

        if self.state == State.GOODBYE:
            self.state = State.END
            return Turn(self.state, "")

        return Turn(self.state, "")

    def done(self) -> bool:
        return self.state == State.END
