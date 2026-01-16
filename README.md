# Smart Attendance System Using Face Recognition
A comprehensive attendance management system that uses AI-based Face Recognition to mark attendance automatically. It integrates with Firebase Firestore for real-time data storage and features a Flask Web Dashboard for monitoring and reporting.


Key Features:

AI Face Recognition: Uses TensorFlow/Keras & OpenCV to identify students with high accuracy.

Real-Time Cloud Sync: Instantly updates attendance status (Present/Late) to Google Firebase.

Dynamic Timetable: Automatically detects the current subject based on the time of day and logs attendance in the correct subject folder.

Smart Entry/Exit Logging: * Entry: Marks "In Time" and calculates status (Present vs. Late) based on a grace period.

Exit: Updates "Out Time" for the same session without duplicating records.

Live Web Dashboard: A responsive Flask interface to view live stats, control the camera, and download reports.

Automated Reports: Generates daily CSV reports identifying Present, Late, and Absent students.


Tech Stack:

Language: Python 3.x

Computer Vision: OpenCV (cv2)

Deep Learning: TensorFlow / Keras

Database: Google Firebase Firestore

Web Framework: Flask (HTML/CSS/JS)

Data Handling: Pandas / NumPy / CSV


Project Structure:

├── dataset/                 # Folder containing student face images

├── model/

│   └── face_model.h5        # Trained AI model

├── reports/                 # Generated CSV reports saved here

├── static/

│   └── style.css            # CSS for Dashboard

├── templates/

│   └── dashboard.html       # Flask HTML Template

├── app.py                   # Main Flask Application

├── entry.py                 # Script for Entry Attendance

├── exit.py                  # Script for Exit Attendance

├── firebase_config.py       # Firebase Database Connection

├── generate_report.py       # Logic to create CSVs

├── students.py              # Dictionary of Student Info (Name, Roll No)

├── timetable.py             # Class Schedule Logic

├── requirements.txt         # Project Dependencies

└── serviceAccountKey.json   # (NOT INCLUDED) Firebase Credentials


Setup & Installation:

1. Clone the Repository

git clone https://github.com/aarushi2404/Attendance-Dashboard.git

cd Attendance-Dashboard

2. Install Dependencies

pip install -r requirements.txt

3. Firebase Configuration

Go to the Firebase Console.

Create a project and set up Firestore Database.

Go to Project Settings > Service Accounts.

Generate a New Private Key.

Rename the downloaded file to serviceAccountKey.json and place it in the project root folder.

Ensure firebase_config.py points to this file.


Configure Timetable & Students:

students.py: Add your students' names and roll numbers.

timetable.py: Update the schedule with your actual class times.


How to Run

Start the Web Dashboard:

python app.py

Open your browser and go to: http://127.0.0.1:5001


Use the Dashboard Controls:

Click "Start Entry Camera" to mark arrival.

Click "Start Exit Camera" to mark departure.

Click "Generate Report" to download the daily attendance CSV.


Usage Guide:

Status Logic:

Present: Arriving before or at the lecture start time.

Late: Arriving within the 10-minute grace period.

Absent: Automatically marked in the report if no entry is found.


Closing the Camera: Press ESC on your keyboard to close the camera window.


Contributing:

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
