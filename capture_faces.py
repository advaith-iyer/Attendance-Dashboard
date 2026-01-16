import cv2
import os
import students  # 👈 import existing students.py

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

# 🔽 Student details input
student_id = input("Enter Student ID (eg: student_1): ")
name = input("Enter Name: ")
roll_no = input("Enter Roll No: ")
division = input("Enter Division: ")

# 🔽 Create dataset folder
path = f"dataset/{student_id}"
os.makedirs(path, exist_ok=True)

# 🔽 Update student_info dictionary
students.student_info[student_id] = {
    "name": name,
    "roll_no": roll_no,
    "division": division
}

# 🔽 WRITE BACK TO students.py
with open("students.py", "w") as f:
    f.write("student_info = ")
    f.write(repr(students.student_info))

print("Student data saved to students.py")

count = 0

while count < 30:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))
        cv2.imwrite(f"{path}/{count}.jpg", face)
        count += 1
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Capture Faces", frame)
    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
print("Face images captured successfully")
