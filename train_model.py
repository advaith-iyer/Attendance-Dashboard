import tensorflow as tf
import numpy as np
import cv2
import os

X, y = [], []

students = sorted(os.listdir("dataset"))
label_map = {name: idx for idx, name in enumerate(students)}

for student in students:
    for img in os.listdir(f"dataset/{student}"):
        image = cv2.imread(f"dataset/{student}/{img}")
        image = cv2.resize(image, (100, 100))
        X.append(image)
        y.append(label_map[student])

X = np.array(X) / 255.0
y = np.array(y)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(100,100,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(students), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X, y, epochs=15)
model.save("model/face_model.h5")
