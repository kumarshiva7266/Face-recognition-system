import os
import cv2
import numpy as np
import re
import threading
from PIL import Image as PilImage, ImageTk, ImageSequence
from tkinter import *
from tkinter import messagebox, ttk
import time

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

class Train:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition System - Training Module")
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
                         text="TRAIN DATA SET", 
                         font=("Helvetica", 30, "bold"), 
                         fg="#ecf0f1", 
                         bg="#2c3e50")
        title_lbl.pack(pady=20)

        # Progress bar frame
        self.progress_frame = Frame(main_frame, bg="#2c3e50")
        self.progress_frame.place(x=0, y=400, width=1530, height=50)
        
        self.progress = ttk.Progressbar(self.progress_frame, 
                                      orient=HORIZONTAL, 
                                      length=1530, 
                                      mode='determinate',
                                      style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = Label(self.progress_frame,
                                text="Ready to train...",
                                font=("Helvetica", 12),
                                fg="#ecf0f1",
                                bg="#2c3e50")
        self.status_label.pack()

        # Animated GIFs
        try:
            self.top_label = Label(main_frame, bg="#2c3e50")
            self.top_label.place(x=0, y=80, width=1550, height=300)
            self.top_animation = AnimatedGIF(self.top_label, r"F:\face_recognition_system\image\noo.gif", (1550, 300))
            self.top_animation.animate()
        except Exception as e:
            print(f"Error loading top image: {e}")

        try:
            self.bottom_label = Label(main_frame, bg="#2c3e50")
            self.bottom_label.place(x=0, y=480, width=1530, height=300)
            self.bottom_animation = AnimatedGIF(self.bottom_label, r"F:\face_recognition_system\image\jii.gif", (1530, 300))
            self.bottom_animation.animate()
        except Exception as e:
            print(f"Error loading bottom image: {e}")

        # Modern train button with hover effects
        self.train_btn = Button(main_frame, 
                              text="Start Training", 
                              font=("Helvetica", 16, "bold"), 
                              fg="white", 
                              bg="#3498db",
                              activebackground="#2980b9",
                              activeforeground="white",
                              relief=FLAT,
                              borderwidth=0,
                              cursor="hand2",
                              command=self.start_training)
        self.train_btn.place(x=600, y=350, width=300, height=50)
        
        # Add hover effects
        self.train_btn.bind("<Enter>", lambda e: self.train_btn.config(bg="#2980b9"))
        self.train_btn.bind("<Leave>", lambda e: self.train_btn.config(bg="#3498db"))

    def start_training(self):
        self.train_btn.config(state=DISABLED, bg="#95a5a6")
        self.status_label.config(text="Training in progress...")
        threading.Thread(target=self.train_classifier, daemon=True).start()

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def train_classifier(self):
        data_dir = r"F:\face_recognition_system\captured_faces"
        faces, ids = [], []
        total_files = sum([len(files) for _, _, files in os.walk(data_dir)])
        processed_files = 0

        print("🔍 Scanning images in all subfolders...")

        for root, dirs, files in os.walk(data_dir):
            folder_name = os.path.basename(root)
            match = re.search(r'_(\d+)$', folder_name)
            if not match:
                print(f"⚠️ Skipping {root}: No numeric User ID found")
                continue
            
            user_id = int(match.group(1))

            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(root, file)
                    try:
                        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                        if img is None or img.size == 0:
                            raise ValueError("Corrupted image")

                        image_np = np.array(img, 'uint8')
                        faces.append(image_np)
                        ids.append(user_id)

                        processed_files += 1
                        progress = (processed_files / total_files) * 100
                        self.update_progress(progress)
                        self.status_label.config(text=f"Processing image {processed_files} of {total_files}")

                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")

        if len(ids) == 0:
            messagebox.showerror("Error", "No valid images found for training!")
            self.train_btn.config(state=NORMAL, bg="#3498db")
            self.status_label.config(text="Training failed: No valid images found")
            return

        try:
            self.status_label.config(text="Training model...")
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            recognizer.write("F:/face_recognition_system/classifier.xml")
            self.update_progress(100)
            self.status_label.config(text="Training completed successfully!")
            messagebox.showinfo("Success", "✅ Training Completed Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ Training Error: {e}")
            self.status_label.config(text=f"Training failed: {str(e)}")
        finally:
            self.train_btn.config(state=NORMAL, bg="#3498db")

if __name__ == "__main__":
    root = Tk()
    Train(root)
    root.mainloop()