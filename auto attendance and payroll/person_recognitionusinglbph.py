import cv2
import numpy as np

# Load the reference image for the person
reference_image_path0 = "test_photo2.png"
reference_image0 = cv2.imread(reference_image_path0, cv2.IMREAD_GRAYSCALE)
reference_image_path1 = "test_photo.png"
reference_image1 = cv2.imread(reference_image_path1, cv2.IMREAD_GRAYSCALE)
reference_image_path2 = "photo.png"
reference_image2 = cv2.imread(reference_image_path2, cv2.IMREAD_GRAYSCALE)

# Resize the reference image to a common size (adjust dimensions as needed)
#common_size = (100, 100)
#reference_image0 = cv2.resize(reference_image0, common_size)
cv2.imshow('test_photo',reference_image0)
#reference_image1 = cv2.resize(reference_image1, common_size)
cv2.imshow('test_photo',reference_image1)
#reference_image2 = cv2.resize(reference_image2, common_size)
cv2.imshow('test_photo',reference_image2)

# Create LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=100)

# Train the recognizer with the resized reference image
labels = np.array([0,1,2])  # You can assign labels for multiple persons
faces = [reference_image0,reference_image1,reference_image2]  # List of images for training
recognizer.train(faces, labels)

# Initialize the video capture
video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify a file path

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection using a cascade classifier (you can use a more advanced method if needed)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for face recognition
        face_roi = gray_frame[y:y + h, x:x + w]

        # Recognize the face using LBPH recognizer
        label, confidence = recognizer.predict(face_roi)

        # Draw a rectangle around the face
        color = (0, 255, 0)  # Green
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Display the recognized label and confidence level
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"Person {label} - Confidence: {confidence:.2f}"
        cv2.putText(frame, text, (x, y - 10), font, 0.5, color, 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Video Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
video_capture.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
