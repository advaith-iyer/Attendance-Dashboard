import cv2
import os
import tensorflow as tf
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from firebase_config import db
from students import student_info
from timetable import get_current_subject, get_current_subject_time

# ---------------- IST UTILITY ----------------
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)
# --------------------------------------------

# ---------------- CONFIG ----------------
CONFIDENCE_THRESHOLD = 0.75  # 0.0–1.0 scale
LECTURE_START = get_current_subject_time()  # returns time object
GRACE_MINUTES = 10
# ----------------------------------------

# 🔹 Load trained model
model = tf.keras.models.load_model("model/face_model.h5")

# 🔹 Recreate label order
labels = sorted(os.listdir("dataset"))

# 🔹 Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- STATUS LOGIC ----------------
def get_status(entry_time):
    """
    entry_time: datetime.time (IST)
    """
    # Convert lecture start + grace minutes
    late_limit = (
        datetime.combine(datetime.today(), LECTURE_START)
        + timedelta(minutes=GRACE_MINUTES)
    ).time()

    if entry_time <= late_limit:
        return "Present"
    else:
        return "Late"
# ----------------------------------------------

cam = cv2.VideoCapture(0)

print("Starting Entry System... Press 'ESC' to exit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # 1️⃣ Check timetable
    subject = get_current_subject()
    if subject is None:
        cv2.putText(
            frame,
            "NO ACTIVE LECTURE",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )
        cv2.imshow("Entry System", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # 🔹 Preprocess face
        face = frame[y : y + h, x : x + w]
        face = cv2.resize(face, (100, 100)) / 255.0
        face = np.expand_dims(face, axis=0)

        # 🔹 Predict
        preds = model.predict(face, verbose=0)
        confidence = np.max(preds)
        label_index = np.argmax(preds)

        # ❌ Unknown face
        if confidence < CONFIDENCE_THRESHOLD:
            os.makedirs("unknown_faces", exist_ok=True)
            timestamp = ist_now().strftime("%H%M%S")
            cv2.imwrite(f"unknown_faces/unknown_{timestamp}.jpg", frame)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                frame,
                "Unknown",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )
            continue

        # ✅ Identified student
        student_id = labels[label_index]
        info = student_info.get(student_id, {})

        # 🔹 IST time
        now = ist_now()
        date_str = now.strftime("%Y-%m-%d")
        in_time = now.strftime("%H:%M:%S")
        status = get_status(now.time())

        doc_ref = (
            db.collection("attendance")
            .document(date_str)
            .collection(subject)
            .document(student_id)
        )

        # 🔹 Write only once per subject/day
        if not doc_ref.get().exists:
            doc_ref.set(
                {
                    "name": info.get("name", "Unknown"),
                    "roll_no": info.get("roll_no", "N/A"),
                    "division": info.get("division", "N/A"),
                    "in_time": in_time,
                    "status": status,
                },
                merge=True,
            )
            print(f"✅ Marked {status}: {student_id} for {subject} (IST)")

        # 🔹 Visual feedback
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{student_id} ({status})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Entry System", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
