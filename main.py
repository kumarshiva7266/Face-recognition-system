from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import os
import customtkinter as ctk
import time
import sys

try:
    # Set the appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
except Exception as e:
    print(f"Error setting appearance mode: {e}")
    sys.exit(1)

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
            gif = Image.open(self.gif_path)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize(self.size, Image.Resampling.LANCZOS)
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

class ImageButton(ctk.CTkFrame):
    def __init__(self, master, image_path, text, command, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color="transparent")
        self.image_path = image_path
        self.text = text
        self.command = command
        
        # Create the button frame with transparent background
        self.button_frame = ctk.CTkFrame(
            self, 
            fg_color="transparent",
            corner_radius=15,
            border_width=2,
            border_color="#1f538d"
        )
        self.button_frame.pack(fill="both", expand=True)
        
        # Load and resize image
        try:
            img = Image.open(image_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)
            self.photo = ctk.CTkImage(light_image=img, size=(180, 180))
            
            # Create image label with transparent background
            self.image_label = ctk.CTkLabel(
                self.button_frame,
                image=self.photo,
                text="",
                fg_color="transparent"
            )
            self.image_label.pack(pady=15)
            
            # Create text label with transparent background
            self.text_label = ctk.CTkLabel(
                self.button_frame,
                text=text,
                font=("Arial", 16, "bold"),
                text_color="white",
                fg_color="transparent"
            )
            self.text_label.pack(pady=10)
            
            # Bind events
            self.button_frame.bind("<Enter>", self.on_enter)
            self.button_frame.bind("<Leave>", self.on_leave)
            self.button_frame.bind("<Button-1>", self.on_click)
            self.image_label.bind("<Button-1>", self.on_click)
            self.text_label.bind("<Button-1>", self.on_click)
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
    
    def on_enter(self, event):
        self.button_frame.configure(border_color="#2b2b2b")
        self.text_label.configure(text_color="#1f538d")
    
    def on_leave(self, event):
        self.button_frame.configure(border_color="#1f538d")
        self.text_label.configure(text_color="white")
    
    def on_click(self, event):
        self.command()

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1530x790+0+0")
        self.root.config(bg="white")

        # Title
        title = Label(root, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Arial", 28, "bold"), bg="white", fg="red")
        title.pack(side=TOP, fill=X)

        # Background with GIF support
        try:
            bg_label = Label(self.root)
            bg_label.place(x=0, y=40, width=1950, height=1250)
            self.bg_animation = AnimatedGIF(bg_label, "image/nbg.gif", (1950, 1200))
            self.bg_animation.animate()
        except Exception as e:
            print(f"Error loading background: {e}")

        # Button images with GIF support
        self.button_images = {
            "Student Details": "image/detail.gif",
            "Face Recognition": "image/original.gif",
            "Attendance": "image/attendance.gif",
            "Help Desk": "image/help.gif",
            "Train Data": "image/trainData.gif",
            "Photos": "image/bee.gif",
            "Developer": "image/dev.gif",
            "Exit": "image/exit.gif"
        }

        # Create buttons with increased size and spacing
        button_width = 320  # Increased from 270
        button_height = 300  # Increased from 250
        horizontal_spacing = 400  # Increased from 350
        vertical_spacing = 400  # Increased from 350

        # First row
        self.create_tile_button("Student Details", self.student_details, 200, 200, button_width, button_height)
        self.create_tile_button("Face Recognition", self.face_recognition, 200 + horizontal_spacing, 200, button_width, button_height)
        self.create_tile_button("Attendance", self.attendance, 200 + horizontal_spacing * 2, 200, button_width, button_height)
        self.create_tile_button("Help Desk", self.help_desk, 200 + horizontal_spacing * 3, 200, button_width, button_height)

        # Second row
        self.create_tile_button("Train Data", self.train_data, 200, 200 + vertical_spacing, button_width, button_height)
        self.create_tile_button("Photos", self.photos, 200 + horizontal_spacing, 200 + vertical_spacing, button_width, button_height)
        self.create_tile_button("Developer", self.developer_info, 200 + horizontal_spacing * 2, 200 + vertical_spacing, button_width, button_height)
        self.create_tile_button("Exit", self.exit_app, 200 + horizontal_spacing * 3, 200 + vertical_spacing, button_width, button_height)

    def create_tile_button(self, text, command, x, y, width, height):
        # Create main frame
        tile_frame = Frame(
            self.root, 
            bg="white", 
            highlightthickness=2, 
            highlightbackground="blue",
            bd=0
        )
        tile_frame.place(x=x, y=y, width=width, height=height)

        # Create image label that fills the frame
        img_label = Label(tile_frame, bg="white")
        img_label.place(relx=0, rely=0, relwidth=1, relheight=0.85)  # 85% height for image

        # Create text label at bottom
        text_label = Label(
            tile_frame, 
            text=text.upper(), 
            font=("Arial", 14, "bold"),  # Increased font size
            bg="blue", 
            fg="white",
            padx=10,
            pady=5
        )
        text_label.place(relx=0, rely=0.85, relwidth=1, relheight=0.15)  # 15% height for text

        # Load and animate image if it's a GIF
        try:
            img_path = self.button_images[text]
            img = Image.open(img_path)
            
            if img.format == 'GIF':
                # For GIF images, create animation
                animation = AnimatedGIF(img_label, img_path, (width, int(height * 0.85)))
                animation.animate()
            else:
                # For static images, resize to fill the space
                img = img.resize((width, int(height * 0.85)), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_label.configure(image=photo)
                img_label.image = photo
        except Exception as e:
            print(f"Error loading image for {text}: {e}")

        # Hover and click events
        def on_enter(e):
            tile_frame.config(bg="lightblue")
            text_label.config(bg="darkblue")
        
        def on_leave(e):
            tile_frame.config(bg="white")
            text_label.config(bg="blue")

        for widget in [tile_frame, img_label, text_label]:
            widget.bind("<Button-1>", lambda e: command())
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    # ---- Functionality for Each Button ----
    def student_details(self):
        try:
            os.system("python student_details.py")
        except Exception as e:
            print(f"❌ Error opening student_details.py: {e}")

    def face_recognition(self):
        try:
            os.system("python face_recognition_module.py")
        except Exception as e:
            print(f"❌ Error opening face_recognition_module.py: {e}")

    def attendance(self):
        try:
            os.system("python attendance.py")
        except Exception as e:
            print(f"❌ Error opening attendance.py: {e}")

    def help_desk(self):
        try:
            os.system("python help.py")
        except Exception as e:
            print(f"❌ Error opening help.py: {e}")

    def train_data(self):
        try:
            os.system("python train.py")
        except Exception as e:
            print(f"❌ Error opening train.py: {e}")

    def photos(self):
        photo_dir = r"F:\face_recognition_system\captured_faces"
        if os.path.exists(photo_dir):
            os.startfile(photo_dir)
            print("✅ Captured Faces folder opened.")
        else:
            print(f"❌ Error: {photo_dir} not found!")

    def developer_info(self):
        try:
            os.system("python developer.py")
        except Exception as e:
            print(f"❌ Error opening developer.py: {e}")

    def exit_app(self):
        self.root.quit()

# Run the app
if __name__ == "__main__":
    try:
        root = ctk.CTk()
        app = FaceRecognitionApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
