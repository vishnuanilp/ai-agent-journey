from room_extract import RULE
CANCEL = ' If the guest wants to stop or drop the booking, add "cancel": true.'
NOT = " Changing a detail is NOT cancelling."
VARIANTS = {"C1": RULE + CANCEL, "C2": RULE + CANCEL + NOT}
CASES = [
    ("forget it", True), ("actually I don't want a room anymore", True), ("stop", True),
    ("cancel the booking", True), ("no thanks, maybe later", True),
    ("2", False), ("3 nights", False), ("can I bring my dog?", False),
    ("Saturday", False), ("no, make it Sunday", False),
]