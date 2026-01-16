from flask import Flask, render_template, redirect, url_for, send_file
from firebase_config import db
from timetable import get_current_subject
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
    # Use IST date
    date = ist_now().strftime("%Y-%m-%d")

    # Get current subject from timetable
    subject = get_current_subject()

    students = []

    if subject:
        docs = (
            db.collection("attendance")
            .document(date)
            .collection(subject)
            .stream()
        )

        for d in docs:
            data = d.to_dict()
            data["id"] = d.id
            students.append(data)

    return render_template(
        "dashboard.html",
        date=date,
        subject=subject or "No Active Lecture",
        total=len(students),
        students=students,
    )

# ---------------- ENTRY (LOCAL ONLY) ----------------
@app.route("/start_entry")
def start_entry():
    """
    Entry must run ONLY on local machine.
    On Render, this should NOT attempt subprocess execution.
    """
    if os.environ.get("RENDER"):  # Render sets this env var
        return redirect(url_for("dashboard"))

    subprocess.Popen(["python", "entry.py"])
    return redirect(url_for("dashboard"))

# ---------------- EXIT (LOCAL ONLY) ----------------
@app.route("/start_exit")
def start_exit():
    """
    Exit must run ONLY on local machine.
    """
    if os.environ.get("RENDER"):
        return redirect(url_for("dashboard"))

    subprocess.Popen(["python", "exit.py"])
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
    app.run(host="0.0.0.0", port=port)

