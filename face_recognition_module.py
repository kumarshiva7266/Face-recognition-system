import os
import cv2
import numpy as np
import threading
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from PIL import Image as PilImage, ImageTk, ImageSequence
from tkinter import *
from tkinter import messagebox, ttk

class AnimatedGIF:
    def __init__(self, label, gif_path, size):
        self.label = label
        self.gif_path = gif_path
        self.size = size
        self.frames = []
        self.current_frame = 0
        self.load_frames()
        
    def load_frames(self):
        try:
            gif = PilImage.open(self.gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize(self.size, PilImage.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(frame)
                self.frames.append(photo)
        except Exception as e:
            print(f"Error loading GIF: {e}")
            
    def animate(self):
        if not self.frames:
            return
            
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.label.configure(image=self.frames[self.current_frame])
        self.label.after(50, self.animate)

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System - Recognition Module")
        self.root.geometry("1530x790+0+0")
        self.root.configure(bg="#2c3e50")

        # Custom style for buttons
        style = ttk.Style()
        style.configure("Custom.TButton", 
                       font=("Helvetica", 14, "bold"),
                       padding=10,
                       background="#3498db",
                       foreground="white")

        # Main frame with gradient background
        main_frame = Frame(self.root, bg="#2c3e50")
        main_frame.place(x=0, y=0, width=1530, height=790)

        # Title with modern styling
        title_frame = Frame(main_frame, bg="#2c3e50")
        title_frame.place(x=0, y=0, width=1530, height=80)

        title_lbl = Label(title_frame, 
                         text="FACE RECOGNITION SYSTEM", 
                         font=("Helvetica", 30, "bold"), 
                         fg="#ecf0f1", 
                         bg="#2c3e50")
        title_lbl.pack(pady=20)

        # Status frame
        self.status_frame = Frame(main_frame, bg="#2c3e50")
        self.status_frame.place(x=0, y=680, width=1530, height=50)
        
        self.status_label = Label(self.status_frame,
                                text="Ready for face recognition...",
                                font=("Helvetica", 12),
                                fg="#ecf0f1",
                                bg="#2c3e50")
        self.status_label.pack()

        # Animated GIFs
        try:
            self.top_label = Label(main_frame, bg="#2c3e50")
            self.top_label.place(x=0, y=80, width=740, height=600)
            self.top_animation = AnimatedGIF(self.top_label, r"F:\face_recognition_system\image\aii.gif", (740, 600))
            self.top_animation.animate()
        except Exception as e:
            print(f"Error loading top image: {e}")

        try:
            self.bottom_label = Label(main_frame, bg="#2c3e50")
            self.bottom_label.place(x=750, y=80, width=750, height=600)
            self.bottom_animation = AnimatedGIF(self.bottom_label, r"F:\face_recognition_system\image\bii.gif", (750, 600))
            self.bottom_animation.animate()
        except Exception as e:
            print(f"Error loading bottom image: {e}")

        # Modern recognition button with hover effects
        self.recognition_btn = Button(main_frame, 
                                    text="Start Recognition", 
                                    font=("Helvetica", 16, "bold"), 
                                    fg="white", 
                                    bg="#3498db",
                                    activebackground="#2980b9",
                                    activeforeground="white",
                                    relief=FLAT,
                                    borderwidth=0,
                                    cursor="hand2",
                                    command=self.start_recognition)
        self.recognition_btn.place(x=600, y=730, width=300, height=50)
        
        # Add hover effects
        self.recognition_btn.bind("<Enter>", lambda e: self.recognition_btn.config(bg="#2980b9"))
        self.recognition_btn.bind("<Leave>", lambda e: self.recognition_btn.config(bg="#3498db"))

        # Modern exit button
        self.exit_btn = Button(main_frame,
                             text="X",
                             font=("Helvetica", 12, "bold"),
                             fg="white",
                             bg="#e74c3c",
                             activebackground="#c0392b",
                             activeforeground="white",
                             relief=FLAT,
                             borderwidth=0,
                             cursor="hand2",
                             command=self.root.quit)
        self.exit_btn.place(x=10, y=10, width=30, height=30)
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c0392b"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg="#e74c3c"))

        # Modern delete CSV button
        self.delete_btn = Button(main_frame,
                               text="🗑️",
                               font=("Helvetica", 12, "bold"),
                               fg="white",
                               bg="#e74c3c",
                               activebackground="#c0392b",
                               activeforeground="white",
                               relief=FLAT,
                               borderwidth=0,
                               cursor="hand2",
                               command=self.delete_csv_file)
        self.delete_btn.place(x=1400, y=10, width=30, height=30)
        self.delete_btn.bind("<Enter>", lambda e: self.delete_btn.config(bg="#c0392b"))
        self.delete_btn.bind("<Leave>", lambda e: self.delete_btn.config(bg="#e74c3c"))

        # Initialize Firebase
        cred = credentials.Certificate(r"F:\face_recognition_system\firebase.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.students_ref = self.db.collection("students")

        # Load the classifier if it exists
        if os.path.exists("F:/face_recognition_system/classifier.xml"):
            self.clf = cv2.face.LBPHFaceRecognizer_create()
            self.clf.read("F:/face_recognition_system/classifier.xml")
            print("Loaded existing classifier.")
        else:
            print("No existing classifier found. Please train a new classifier.")

    def start_recognition(self):
        self.recognition_btn.config(state=DISABLED, bg="#95a5a6")
        self.status_label.config(text="Starting face recognition...")
        threading.Thread(target=self.face_recog, daemon=True).start()

    def delete_csv_file(self):
        """Delete the attendance CSV file."""
        filename = "attendance.csv"
        try:
            if os.path.exists(filename):
                os.remove(filename)
                self.status_label.config(text="Attendance CSV file deleted successfully!")
                messagebox.showinfo("Success", "Attendance CSV file deleted successfully!")
            else:
                self.status_label.config(text="No attendance file found.")
                messagebox.showinfo("Info", "No attendance file found.")
        except Exception as e:
            self.status_label.config(text=f"Error deleting CSV file: {e}")
            messagebox.showerror("Error", f"Error deleting CSV file: {e}")

    def face_recog(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            self.status_label.config(text="Could not open camera")
            messagebox.showerror("Error", "Could not open camera")
            self.recognition_btn.config(state=NORMAL, bg="#3498db")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Couldn't capture frame from camera.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                try:
                    id, confidence = self.clf.predict(gray[y:y + h, x:x + w])
                    confidence = int(100 * (1 - confidence / 300))

                    if confidence > 60:  # Lowered confidence threshold for better recognition
                        student_data = self.get_student_data(id)
                        if student_data:
                            # Display student details with modern styling
                            text_lines = [
                                f"ID: {student_data.get('id', 'N/A')}",
                                f"Name: {student_data.get('name', 'N/A')}",
                                f"Roll No: {student_data.get('roll_no', 'N/A')}",
                                f"Course: {student_data.get('course', 'N/A')}",
                                f"Department: {student_data.get('department', 'N/A')}",
                                f"Year: {student_data.get('year', 'N/A')}",
                                f"Semester: {student_data.get('semester', 'N/A')}",
                            ]
                            
                            # Draw text with modern styling
                            y_offset = 30
                            for i, line in enumerate(text_lines):
                                cv2.putText(
                                    frame,
                                    line,
                                    (15, 45 + y_offset * i),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (255, 255, 255),  # White text
                                    2,
                                )

                            # Check if attendance is already marked for today
                            if self.is_attendance_marked(student_data.get("id")):
                                cv2.putText(
                                    frame,
                                    "Attendance already marked for today",
                                    (10, 250),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (0, 255, 255),  # Yellow text
                                    2,
                                )
                                self.status_label.config(text="Attendance already marked for today")
                            else:
                                # Mark attendance
                                self.mark_attendance(
                                    student_data.get("id"),
                                    student_data.get("name"),
                                    student_data.get("roll_no"),
                                    student_data.get("course"),
                                    student_data.get("department"),
                                    student_data.get("year"),
                                    student_data.get("semester"),
                                )
                                cv2.putText(
                                    frame,
                                    "Attendance Marked Successfully!",
                                    (10, 250),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (0, 255, 0),  # Green text
                                    2,
                                )
                                self.status_label.config(text="Attendance marked successfully!")
                        else:
                            cv2.putText(
                                frame,
                                "Student data not found",
                                (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 0, 255),  # Red text
                                2,
                            )
                            self.status_label.config(text="Student data not found in database")
                    else:
                        cv2.putText(
                            frame,
                            "Unknown Face",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255),  # Red text
                            2,
                        )
                        self.status_label.config(text="Unknown face detected")
                except Exception as e:
                    print(f"Error in face recognition: {e}")
                    cv2.putText(
                        frame,
                        "Error in recognition",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),  # Red text
                        2,
                    )

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.recognition_btn.config(state=NORMAL, bg="#3498db")
        self.status_label.config(text="Ready for face recognition...")

    def get_student_data(self, student_id):
        try:
            # Convert student_id to string to ensure proper matching
            student_id = str(student_id)
            print(f"Looking up student with ID: {student_id}")  # Debug print
            
            # Query the students collection for the matching student_id
            student_doc = self.students_ref.document(student_id).get()
            
            if student_doc.exists:
                data = student_doc.to_dict()
                print(f"Raw student data from Firebase: {data}")  # Debug print
                
                # Create a dictionary with the required fields
                student_info = {
                    'id': data.get('id', student_id),  # Use student_id as fallback
                    'name': data.get('name', 'N/A'),
                    'roll_no': data.get('roll_no', 'N/A'),
                    'course': data.get('course', 'N/A'),
                    'department': data.get('department', 'N/A'),
                    'year': data.get('year', 'N/A'),
                    'semester': data.get('semester', 'N/A')
                }
                
                # If name is N/A, try to get it from student_name field
                if student_info['name'] == 'N/A' and 'student_name' in data:
                    student_info['name'] = data['student_name']
                
                # If id is N/A, try to get it from student_id field
                if student_info['id'] == 'N/A' and 'student_id' in data:
                    student_info['id'] = data['student_id']
                
                print(f"Processed student data: {student_info}")  # Debug print
                return student_info
            else:
                print(f"Student ID {student_id} not found in database")
                return None
            
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def is_attendance_marked(self, student_id):
        filename = "attendance.csv"
        try:
            if not os.path.exists(filename):
                return False

            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")

            with open(filename, "r") as f:
                lines = f.readlines()
                for line in lines:
                    data = line.strip().split(",")
                    if len(data) > 7 and data[0] == str(student_id) and data[8] == date_str:
                        return True
            return False
        except Exception as e:
            print(f"Error checking attendance: {e}")
            return False

    def mark_attendance(self, student_id, student_name, roll_no, course, department, year, semester):
        filename = "attendance.csv"
        try:
            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")

            if not os.path.exists(filename):
                with open(filename, "w", newline="") as f:
                    f.write("ID,Name,Roll No,Course,Department,Year,Semester,Time,Date,Status\n")

            with open(filename, "a", newline="") as f:
                f.write(f"{student_id},{student_name},{roll_no},{course},{department},{year},{semester},{time_str},{date_str},Present\n")
                print(f"Attendance marked for {student_name}")
        except Exception as e:
            print(f"Error marking attendance: {e}")

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()