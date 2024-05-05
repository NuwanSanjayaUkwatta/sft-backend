import cv2
import numpy as np
import os
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump
import pickle
from scipy import ndimage

# Function to preprocess image and adjust color
def preprocess_image(img):
    img = cv2.resize(img, (640, 480))
    img_array = img_to_array(img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Function to create embeddings and apply data augmentation
def create_face_embeddings(dataset_path):
    embeddings = []
    labels = []
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for class_dir in os.listdir(dataset_path):
        if not class_dir.startswith('.'):
            class_path = os.path.join(dataset_path, class_dir)
            for img_path in os.listdir(class_path):
                img = cv2.imread(os.path.join(class_path, img_path))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    face_img = img[y:y+h, x:x+w]
                    processed_img = preprocess_image(face_img)
                    embeddings.append(processed_img.flatten())
                    labels.append(class_dir)
                    # Data augmentation by rotating the face image
                    for angle in [90, 180, 270]:
                        rotated_img = ndimage.rotate(face_img, angle)
                        processed_rotated_img = preprocess_image(rotated_img)
                        embeddings.append(processed_rotated_img.flatten())
                        labels.append(class_dir)
    return embeddings, labels

# Function to train the SVM model
def train_model(X_train, y_train):
    model = SVC(C=1.0, kernel='linear', probability=True)
    model.fit(X_train, y_train)
    return model



def run():
    dataset_path = 'ai_model/dataset'
    embeddings, labels = create_face_embeddings(dataset_path)

    # Split the data into training, validation, and testing sets
    X_train, X_temp, y_train, y_temp = train_test_split(embeddings, labels, test_size=0.2, random_state=42)
    X_validation, X_test, y_validation, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Encode labels
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_validation_encoded = le.transform(y_validation)
    y_test_encoded = le.transform(y_test)

    # Train the model using the training set
    model = train_model(X_train, y_train_encoded)

    # Evaluate on validation data
    validation_predictions = model.predict(X_validation)
    print("Validation Metrics:")
    print(classification_report(y_validation_encoded, validation_predictions))
    print("Validation Confusion Matrix:")
    print(confusion_matrix(y_validation_encoded, validation_predictions))

    # Finally, evaluate the model on the test data
    test_predictions = model.predict(X_test)
    print("Test Metrics:")
    print(classification_report(y_test_encoded, test_predictions))
    print("Test Confusion Matrix:")
    print(confusion_matrix(y_test_encoded, test_predictions))

    # Save the model and encoder
    dump(model, 'ai_model/face_recognition_model.joblib')
    with open('ai_model/label_encoder.pickle', 'wb') as f:
        pickle.dump(le, f)
