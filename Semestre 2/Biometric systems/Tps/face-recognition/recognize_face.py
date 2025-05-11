import cv2                   # OpenCV for computer vision tasks.
import os                    # For file and directory handling.
import numpy as np           # For numerical operations (used in face model training).
import tkinter as tk         # GUI library.
from tkinter import messagebox  # For showing popup messages.
from threading import Thread     # To run camera operations in parallel with GUI.
import time                 # For managing time delays

# === PATHS ===
base_path = "/home/shito/Master/Semestre 2/Biometric systems/Tps/face-recognition"
cascade_path = os.path.join(base_path, "haarcascade_frontalface_default.xml")
dataset_path = os.path.join(base_path, "faces_dataset")

# === INITIALIZATIONS ===
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
os.makedirs(dataset_path, exist_ok=True)

# === GLOBAL STATE ===
running = False
mode = "idle"
thread = None

# === GUI SETUP ===
root = tk.Tk()
root.title("Face Authentication System")
root.geometry("400x250")
name_var = tk.StringVar()

# === FUNCTION: COLLECT FACES ===
def collect_faces():
    global running, mode, thread
    name = name_var.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return

    if running:
        messagebox.showinfo("Busy", "Camera is already running.")
        return

    person_path = os.path.join(dataset_path, name)
    os.makedirs(person_path, exist_ok=True)

    def _collect():
        global running, mode
        running = True
        mode = "collect"
        cap = cv2.VideoCapture(0)
        count = 0
        last_capture_time = time.time()
        delay_between_captures = 0.5  # seconds

        while count < 30 and running:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            current_time = time.time()

            for (x, y, w, h) in faces:
                if current_time - last_capture_time >= delay_between_captures:
                    face_color = frame[y:y+h, x:x+w]
                    face_color = cv2.resize(face_color, (200, 200))
                    cv2.imwrite(os.path.join(person_path, f"{count}.jpg"), face_color)
                    count += 1
                    last_capture_time = current_time

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Saving {count}/30", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Collecting Faces", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
                break

        cap.release()
        cv2.destroyAllWindows()
        running = False
        mode = "idle"

        if count > 0:
            messagebox.showinfo("Done", f"Collected {count} images for {name}")
        else:
            messagebox.showwarning("Warning", "No faces collected.")

        root.quit()  # Exit GUI after collection

    thread = Thread(target=_collect)
    thread.start()

# === FUNCTION: TRAIN MODEL ===
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
            if img is not None:
                img = cv2.equalizeHist(img)
                faces.append(img)
                labels.append(label_id)
        label_id += 1

    if faces:
        recognizer.train(faces, np.array(labels))
        return label_map
    else:
        return None

# === FUNCTION: RECOGNIZE FACES ===
def recognize_faces():
    global running, mode, thread

    if running:
        messagebox.showinfo("Busy", "Camera is already running.")
        return

    label_map = train_model()
    if label_map is None:
        messagebox.showerror("Error", "No faces found. Please collect first.")
        return

    def _recognize():
        global running, mode
        running = True
        mode = "recognize"
        cap = cv2.VideoCapture(0)

        while running:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                label, confidence = recognizer.predict(face)

                if confidence < 50:
                    name = label_map.get(label, "Unknown")
                    color = (0, 255, 0)
                    display = f"{name} ({round(confidence, 2)})"
                else:
                    name = "Unknown"
                    color = (0, 0, 255)
                    display = "Unknown"

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, display, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        running = False
        mode = "idle"

        root.quit()  # Exit GUI after recognition

    thread = Thread(target=_recognize)
    thread.start()

# === FUNCTION: EXIT ===
def on_exit():
    global running
    running = False
    if thread and thread.is_alive():
        thread.join()
    cv2.destroyAllWindows()
    root.destroy()

# === GUI WIDGETS ===
tk.Label(root, text="Enter Name:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=name_var, font=("Arial", 12), width=30).pack()

tk.Button(root, text="Collect Faces", command=collect_faces,
    width=25, bg="#4CAF50", fg="white").pack(pady=10)

tk.Button(root, text="Recognize Faces", command=recognize_faces,
    width=25, bg="#2196F3", fg="white").pack(pady=5)

tk.Button(root, text="Exit", command=on_exit,
    width=25, bg="#f44336", fg="white").pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
root.destroy()