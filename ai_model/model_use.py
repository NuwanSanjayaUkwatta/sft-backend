#not use in flask 

import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from joblib import load
import pickle
from collections import Counter

# Load the model and encoder
model = load('face_recognition_model.joblib')
with open('label_encoder.pickle', 'rb') as f:
    le = pickle.load(f)

# Load haarcascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to preprocess image and adjust color
def preprocess_image(img):
    img = cv2.resize(img, (640, 480))
    img_array = img_to_array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Function to perform face recognition using webcam
def perform_face_recognition(model, le, recognition_frames=100):
    cap = cv2.VideoCapture(0)

    recognized_faces = []

    frame_count = 0
    while frame_count < recognition_frames:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            processed_img = preprocess_image(face_img)
            prediction = model.predict(processed_img.flatten().reshape(1, -1))
            person = le.inverse_transform(prediction)[0]
            recognized_faces.append(person)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, person, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow('Face Recognition', frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Identify the most occurred face
    most_common_face = Counter(recognized_faces).most_common(1)[0][0]
    return most_common_face

# Perform face recognition using webcam for 100 frames and identify the most common face
perform_face_recognition(model, le, recognition_frames=100)
