import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_config import db
from students import student_info

# ---------------- IST UTILITY ----------------
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)
# --------------------------------------------

def create_csv():
    # 1️⃣ Use IST date
    date = ist_now().strftime("%Y-%m-%d")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    file_name = f"attendance_full_{date}.csv"
    file_path = os.path.join(reports_dir, file_name)

    # 2️⃣ Reference attendance for IST date
    day_ref = db.collection("attendance").document(date)

    # Get all subject sub‑collections
    subject_collections = day_ref.collections()

    all_student_ids = list(student_info.keys())

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Subject",
            "Student ID",
            "Name",
            "Roll No",
            "Division",
            "In Time (IST)",
            "Out Time (IST)",
            "Status"
        ])

        found_any_data = False

        for sub in subject_collections:
            found_any_data = True
            subject_name = sub.id

            # Fetch present students for this subject
            present_docs = {
                doc.id: doc.to_dict()
                for doc in sub.stream()
            }

            for s_id in all_student_ids:
                info = student_info.get(s_id, {})
                actual_name = info.get("name", s_id)

                if s_id in present_docs:
                    d = present_docs[s_id]
                    writer.writerow([
                        subject_name,
                        s_id,
                        actual_name,
                        info.get("roll_no", "N/A"),
                        info.get("division", "N/A"),
                        d.get("in_time", "N/A"),
                        d.get("out_time", "---"),
                        d.get("status", "Present"),
                    ])
                else:
                    # Absent for this subject
                    writer.writerow([
                        subject_name,
                        s_id,
                        actual_name,
                        info.get("roll_no", "N/A"),
                        info.get("division", "N/A"),
                        "---",
                        "---",
                        "Absent",
                    ])

    if not found_any_data:
        print(f"⚠️ No attendance data found for IST date: {date}")
    else:
        print(f"✅ IST attendance report generated: {file_path}")

    return file_path


if __name__ == "__main__":
    create_csv()
