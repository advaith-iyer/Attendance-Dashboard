from flask import Flask, render_template, redirect, url_for, send_file
from firebase_config import db
from timetable import get_current_lecture   # ← changed import
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import subprocess

app = Flask(__name__)

# ---------------- IST UTILITY ----------------
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)
# --------------------------------------------

# ---------------- HOME / LOGIN ----------------
@app.route("/")
def login():
    return redirect(url_for("dashboard"))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    now = ist_now()
    date_str = now.strftime("%d %B %Y")   # nicer format: 17 January 2026

    lecture = get_current_lecture()

    if lecture:
        subject = lecture["subject"]
        # Format times in 12-hour style with AM/PM (common in dashboards)
        start_time_str = lecture["start_time"].strftime("%I:%M %p")
        end_time_str   = lecture["end_time"].strftime("%I:%M %p")
    else:
        subject = "No Active Lecture"
        start_time_str = "—"
        end_time_str   = "—"

    students = []

    if lecture:  # only query if there's an active subject
        docs = (
            db.collection("attendance")
            .document(now.strftime("%Y-%m-%d"))   # use actual date
            .collection(subject)
            .stream()
        )

        for d in docs:
            data = d.to_dict()
            data["id"] = d.id
            students.append(data)

    return render_template(
        "dashboard.html",
        date=date_str,
        subject=subject,
        lecture_start_time=start_time_str,
        lecture_end_time=end_time_str,
        total=len(students),
        students=students,
    )

# ---------------- ENTRY (LOCAL ONLY) ----------------
@app.route("/start_entry")
def start_entry():
    if os.environ.get("RENDER"):
        return redirect(url_for("dashboard"))

    subprocess.Popen(["python3", "entry.py"])
    return redirect(url_for("dashboard"))

# ---------------- EXIT (LOCAL ONLY) ----------------
@app.route("/start_exit")
def start_exit():
    if os.environ.get("RENDER"):
        return redirect(url_for("dashboard"))

    subprocess.Popen(["python3", "exit.py"])
    return redirect(url_for("dashboard"))

# ---------------- REPORT DOWNLOAD ----------------
@app.route("/generate_report")
def download_report():
    import generate_report

    try:
        file_path = generate_report.create_csv()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Error generating report: {e}", 500

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)   # debug=True helpful during dev
