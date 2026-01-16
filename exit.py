import cv2
import os
import numpy as np
import tensorflow as tf
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_config import db
from timetable import get_current_subject

# ---------------- IST UTILITY ----------------
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    return datetime.now(IST)
# --------------------------------------------

# ---------------- CONFIG ----------------
CONFIDENCE_THRESHOLD = 0.75  # 0.0–1.0 scale
# ----------------------------------------

# 🔹 Load trained model
model = tf.keras.models.load_model("model/face_model.h5")
labels = sorted(os.listdir("dataset"))

# 🔹 Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

print("Starting Exit System... Press 'ESC' to exit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # 1️⃣ Get current subject
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
        cv2.imshow("Exit System", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y : y + h, x : x + w]
        face = cv2.resize(face, (100, 100)) / 255.0
        face = np.expand_dims(face, axis=0)

        preds = model.predict(face, verbose=0)
        confidence = np.max(preds)
        label_index = np.argmax(preds)

        # ❌ Unknown face
        if confidence < CONFIDENCE_THRESHOLD:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            continue

        # ✅ Identified student
        student_id = labels[label_index]

        # 🔹 IST time
        now = ist_now()
        date_str = now.strftime("%Y-%m-%d")
        out_time = now.strftime("%H:%M:%S")

        # 🔹 Reference to today's subject record
        ref = (
            db.collection("attendance")
            .document(date_str)
            .collection(subject)
            .document(student_id)
        )

        doc = ref.get()
        if not doc.exists:
            cv2.putText(
                frame,
                "NO ENTRY RECORD",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )
            continue

        # 🔹 Update exit details only
        ref.update(
            {
                "out_time": out_time,
                "exit_status": "Exited",
            }
        )

        print(f"✅ Exit marked for {student_id} in {subject} (IST)")

        # 🔹 Visual feedback
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(
            frame,
            f"{student_id} OUT",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2,
        )

    cv2.imshow("Exit System", frame)

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
