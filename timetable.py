from datetime import datetime, time
from zoneinfo import ZoneInfo

# ---------------- IST SETUP ----------------
IST = ZoneInfo("Asia/Kolkata")
# -------------------------------------------

# ---------------- TIMETABLE ----------------
timetable = [
    {"subject": "Math", "start": time(0, 0), "end": time(4, 0)},
    {"subject": "Physics", "start": time(4, 0), "end": time(10, 0)},
    {"subject": "Test", "start": time(10, 0), "end": time(16, 0)},   # Testing
    {"subject": "Chemistry", "start": time(16, 0), "end": time(21, 0)},
    {"subject": "Computer", "start": time(21, 0), "end": time(23, 59)},
]
# -------------------------------------------

def get_current_subject():
    """
    Returns the subject based on CURRENT IST time.
    Called by app.py, entry.py, exit.py
    """
    now = datetime.now(IST).time()

    for slot in timetable:
        if slot["start"] <= now <= slot["end"]:
            return slot["subject"]

    return None


def get_current_subject_time():
    """
    Returns the lecture START time (IST) for late‑entry logic.
    Used in entry.py
    """
    now = datetime.now(IST).time()

    for slot in timetable:
        if slot["start"] <= now <= slot["end"]:
            return slot["start"]

    return None
