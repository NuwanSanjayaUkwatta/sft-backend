#not use in flask 


import cv2
import os

# Create dataset folder if it doesn't exist
dataset_folder = 'dataset'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# Function to capture and save images
def capture_images(name, num_images=10):
    # Create folder for the person if it doesn't exist
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Counter for captured images
    count = 0

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Display the captured image
        cv2.imshow('Capture Image', frame)

        # Save the captured image
        image_path = os.path.join(person_folder, f'{name}_{count}.jpg')
        cv2.imwrite(image_path, frame)

        # Increment counter
        count += 1

        # Wait for 0.5 seconds before capturing the next image
        cv2.waitKey(1000)

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Main function
def main():
    # Ask for the person's name
    name = input("Enter the person's name: ")

    # Capture and save images
    capture_images(name, num_images=10)

if __name__ == "__main__":
    main()
