import os
from flask import jsonify, request
from ai_model.model_train import run
from ai_model.model_train import preprocess_image
from joblib import load
import pickle
import cv2
import numpy as np
from PIL import Image
import uuid

UPLOAD_FOLDER = 'ai_model/dataset'
MODEL_PATH = 'ai_model/face_recognition_model.joblib'
ENCODER_PATH = 'ai_model/label_encoder.pickle'
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


def image_upload(employee_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if not file or file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Ensure the folder exists or create it
        employee_folder = os.path.join(UPLOAD_FOLDER, str(employee_id))
        os.makedirs(employee_folder, exist_ok=True)

        # Check the number of files in the folder
        files = os.listdir(employee_folder)
        if len(files) >= 10:
            # If 10 or more files exist, remove them
            for f in files:
                os.remove(os.path.join(employee_folder, f))

        # Generate a unique filename using UUID
        unique_filename = f"{uuid.uuid4()}.jpg"  # Generates a unique identifier and appends .jpg

        # Assume the file is an image and save it directly as JPEG
        image = Image.open(file.stream)  # Open the image file
        save_path = os.path.join(employee_folder, unique_filename)  # Save with unique filename
        image.save(save_path, format='JPEG')  # Save as JPEG

        return jsonify({"message": "File uploaded successfully", "filename": unique_filename}), 201
    except Exception as e:
        return jsonify({"error": "Could not process the uploaded file: " + str(e)}), 500

def train():
    try:
        run()
        return jsonify({"message": "Model trained successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def load_model_and_encoder():
    model = None
    encoder = None
    try:
        # Load model
        model = load(MODEL_PATH)
        # Load encoder
        with open(ENCODER_PATH, 'rb') as f:
            encoder = pickle.load(f)
    except Exception as e:
        print(f"Error loading model or encoder: {e}")
    return model, encoder

def predict():
    try:
        # Load model and encoder
        model, encoder = load_model_and_encoder()

        if not model or not encoder:
            return jsonify({"error": "Model or encoder not found"}), 500

        # Load image from request
        file = request.files['file']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Detect faces in the image
        face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Make predictions for each detected face
        persons = []
        for (x, y, w, h) in faces:
            face_img = img[y:y+h, x:x+w]
            processed_img = preprocess_image(face_img)
            prediction = model.predict(processed_img.flatten().reshape(1, -1))
            person = encoder.inverse_transform(prediction)[0]
            persons.append(person)

        return jsonify({"persons": persons}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
