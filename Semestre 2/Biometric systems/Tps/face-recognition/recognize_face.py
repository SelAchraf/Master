import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Load face detection model and initialize recognizer
facedetect = cv2.CascadeClassifier('/home/achraf/Documents/face-recognition/haarcascade_frontalcatface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Dataset path
dataset_path = "faces_dataset"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Global state
running = True
UNKNOWN_THRESHOLD = 70  # Confidence threshold to reject unknown faces

# GUI setup
root = tk.Tk()
root.title("Face Authentication System")
root.geometry("400x250")

name_var = tk.StringVar()

def collect_faces():
    name = name_var.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return

    person_path = os.path.join(dataset_path, name)
    if not os.path.exists(person_path):
        os.makedirs(person_path)

    def _collect():
        global running
        cap = cv2.VideoCapture(0)
        count = 0
        while count < 30 and running:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                file_path = os.path.join(person_path, f"{count}.jpg")
                cv2.imwrite(file_path, face)
                count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Saving {count}/50", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Collecting Faces", frame)
            if cv2.waitKey(1) == ord('q'):
                running = False
                break
        cap.release()
        cv2.destroyAllWindows()
        if running:
            messagebox.showinfo("Done", f"Collected {count} images for {name}")

    Thread(target=_collect).start()

def train_model():
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_path):
            continue
        label_map[label_id] = person_name
        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(label_id)
        label_id += 1

    if faces:
        recognizer.train(faces, np.array(labels))
        return label_map
    else:
        return None

def recognize_face():
    label_map = train_model()
    if label_map is None:
        messagebox.showerror("Error", "No faces found. Please collect first.")
        return

    def _recognize():
        global running
        cap = cv2.VideoCapture(0)
        while running:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                label, confidence = recognizer.predict(face)

                if confidence < UNKNOWN_THRESHOLD:
                    name = label_map.get(label, "Unknown")
                    color = (0, 255, 0)
                    display_text = f"{name} ({round(confidence, 2)})"
                else:
                    name = "Unknown"
                    color = (0, 0, 255)
                    display_text = "Unknown"

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, display_text, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) == ord('q'):
                running = False
                break

        cap.release()
        cv2.destroyAllWindows()

    Thread(target=_recognize).start()

def on_exit():
    global running
    running = False
    cv2.destroyAllWindows()
    root.destroy()

# GUI elements
tk.Label(root, text="Enter Name:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=name_var, font=("Arial", 12), width=30).pack()

tk.Button(root, text="Collect Faces", command=collect_faces, width=25, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Recognize Faces", command=recognize_face, width=25, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="Exit", command=on_exit, width=25, bg="#f44336", fg="white").pack(pady=5)

# Handle window close (X button)
root.protocol("WM_DELETE_WINDOW", on_exit)

root.mainloop()

