from datetime import datetime, time
from zoneinfo import ZoneInfo

# ---------------- IST SETUP ----------------
IST = ZoneInfo("Asia/Kolkata")
# -------------------------------------------

# ---------------- TIMETABLE ----------------
# Using 24-hour time objects (very natural in Python)
timetable = [
    {"subject": "Math",      "start": time(0, 0),   "end": time(4, 0)},
    {"subject": "Physics",   "start": time(4, 0),   "end": time(10, 0)},
    {"subject": "Biology",   "start": time(14, 49), "end": time(16, 0)},  # Testing slot
    {"subject": "Chemistry", "start": time(16, 0),  "end": time(21, 0)},
    {"subject": "Computer",  "start": time(21, 0),  "end": time(23, 59)},
]
# -------------------------------------------

def get_current_lecture():
    """
    Returns dict with current lecture info or None if no lecture is active.
    Includes subject + start/end time objects.
    """
    now = datetime.now(IST).time()

    for slot in timetable:
        if slot["start"] <= now <= slot["end"]:
            return {
                "subject": slot["subject"],
                "start_time": slot["start"],   # datetime.time object
                "end_time":   slot["end"],     # datetime.time object
            }
    return None


def get_current_subject():
    """
    Compatibility function - returns only subject name or None.
    Used by entry.py / exit.py if they only need subject.
    """
    lecture = get_current_lecture()
    return lecture["subject"] if lecture else None


def get_current_lecture_times():
    """
    Returns start & end time objects (or None).
    Can be used when you only need the times.
    """
    lecture = get_current_lecture()
    if lecture:
        return lecture["start_time"], lecture["end_time"]
    return None, None
