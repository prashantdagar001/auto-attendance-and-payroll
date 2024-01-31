import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
class Employee:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position

employees = [
    Employee(0, "John Doe", "Manager"),
    Employee(1, "Jane Smith", "Developer"),
    Employee(2, "Prashant Dagar","CEO")
    # Add more sample employees as needed
]

def add_employee():
    id = int(entry_id.get())
    name = entry_name.get()
    position = entry_position.get()
    
    new_employee = Employee(id, name, position)
    employees.append(new_employee)
    
    update_employee_list()

def edit_employee():
    selected_employee = tree.selection()
    
    if selected_employee:
        selected_employee_id = int(tree.item(selected_employee)['text'])
        updated_name = entry_name.get()
        updated_position = entry_position.get()

        for employee in employees:
            if employee.id == selected_employee_id:
                employee.name = updated_name
                employee.position = updated_position
        
        update_employee_list()

def delete_employee():
    selected_employee = tree.selection()
    
    if selected_employee:
        selected_employee_id = int(tree.item(selected_employee)['text'])
        
        employees[:] = [employee for employee in employees if employee.id != selected_employee_id]
        
        update_employee_list()

def toggle_attendance_mode():
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
    #cv2.imshow('test_photo',reference_image0)
    #reference_image1 = cv2.resize(reference_image1, common_size)
    #cv2.imshow('test_photo',reference_image1)
    #reference_image2 = cv2.resize(reference_image2, common_size)
    #cv2.imshow('test_photo',reference_image2)

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


def update_employee_list():
    # Clear existing items in the tree
    for item in tree.get_children():
        tree.delete(item)

    # Populate the tree with updated employee data
    for employee in employees:
        tree.insert("", "end", text=employee.id, values=(employee.name, employee.position))

# Create the main window
root = tk.Tk()
root.title("Admin Mode")

# Create and set a custom style for the labels, entries, and button
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12, "bold"))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"))

# Create labels, entry widgets, and buttons
label_id = ttk.Label(root, text="Employee ID:")
label_name = ttk.Label(root, text="Employee Name:")
label_position = ttk.Label(root, text="Employee Position:")

entry_id = ttk.Entry(root)
entry_name = ttk.Entry(root)
entry_position = ttk.Entry(root)

button_add_employee = ttk.Button(root, text="Add Employee", command=add_employee)
button_edit_employee = ttk.Button(root, text="Edit Employee", command=edit_employee)
button_delete_employee = ttk.Button(root, text="Delete Employee", command=delete_employee)
button_toggle_attendance = ttk.Button(root, text="Toggle Attendance Mode", command=toggle_attendance_mode)

# Create a Treeview to display employee data
tree = ttk.Treeview(root, columns=("Name", "Position"))
tree.heading("#0", text="ID")
tree.heading("Name", text="Name")
tree.heading("Position", text="Position")

# Place labels, entry widgets, and buttons in the window
label_id.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_id.grid(row=0, column=1, padx=10, pady=10, sticky="w")
label_name.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_name.grid(row=1, column=1, padx=10, pady=10, sticky="w")
label_position.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_position.grid(row=2, column=1, padx=10, pady=10, sticky="w")

button_add_employee.grid(row=3, column=0, columnspan=2, pady=10)
button_edit_employee.grid(row=4, column=0, columnspan=2, pady=10)
button_delete_employee.grid(row=5, column=0, columnspan=2, pady=10)
button_toggle_attendance.grid(row=6, column=0, columnspan=2, pady=10)

tree.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky="nsew")

# Configure row and column weights to make the Treeview expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run the application
update_employee_list()
root.mainloop()
