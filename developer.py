import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
import webbrowser
from datetime import datetime
import os

class AnimatedGIF:
    def __init__(self, label, path, size):
        self.label = label
        self.path = path
        self.size = size
        self.frames = []
        self.current_frame = 0
        self.load_frames()
        self.animate()
        
    def load_frames(self):
        try:
            gif = Image.open(self.path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                frame_image = gif.copy()
                frame_image = frame_image.resize(self.size, Image.Resampling.LANCZOS)
                self.frames.append(ctk.CTkImage(light_image=frame_image, size=self.size))
        except Exception as e:
            print(f"Error loading GIF: {e}")
            
    def animate(self):
        if self.frames:
            self.label.configure(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.label.after(100, self.animate)

class Developer:
    def __init__(self, root):
        self.root = root
        self.root.title("Meet The Developers")
        self.root.geometry("1650x850+0+0")
        self.root.resizable(True, True)
        
        # Set appearance mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Background Image
        bg_image = Image.open("F:\\face_recognition_system\\image\\developer1.JPG")
        bg_image = bg_image.resize((1650, 850), Image.Resampling.LANCZOS)
        self.bg_photo = ctk.CTkImage(light_image=bg_image, size=(1650, 850))
        
        # Background Label
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_photo, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Add animated GIF in the background
        gif_label = ctk.CTkLabel(self.root, text="")
        gif_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.animated_gif = AnimatedGIF(gif_label, "F:\\face_recognition_system\\image\\detail.gif", (1650, 850))
        
        # Main container with semi-transparent background
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title Frame
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a")
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(title_frame,
                                  text="MEET THE DEVELOPERS",
                                  font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
                                  text_color="#ffffff")
        title_label.pack(pady=20)
        
        # Back Button
        back_btn = ctk.CTkButton(title_frame,
                                text="← Back",
                                width=100,
                                height=35,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                corner_radius=10,
                                fg_color="#FF5722",
                                hover_color="#E64A19",
                                command=self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Developer Cards Frame
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a")
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Developer Data
        developers = [
            {
                "name": "Shiv Prasad",
                "email": "shiva.cloudray0303@gmail.com",
                "role": "Lead Developer",
                "image": "F:\\face_recognition_system\\image\\shiva.JPG",
                "linkedin": "www.linkedin.com/in/shiv-prasad-99a524346",
                "color": "#4CAF50"
            },
            {
                "name": "Rohith Kumar",
                "email": "proffessorrohithkumar@gmail.com",
                "role": "Backend Developer",
                "image": "F:\\face_recognition_system\\image\\rohith.PNG",
                "linkedin": "www.linkedin.com/in/rohith-kumar-0643061b4",
                "color": "#2196F3"
            },
            {
                "name": "Monish Goud",
                "email": "gandumonish@example.com",
                "role": "Frontend Developer",
                "image": "F:\\face_recognition_system\\image\\monish.PNG",
                "linkedin": "#",
                "color": "#FF9800"
            }
        ]
        
        # Create developer cards
        for idx, dev in enumerate(developers):
            # Card container
            card = ctk.CTkFrame(cards_frame, fg_color="#2a2a2a")
            card.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
            
            # Developer Image
            try:
                dev_img = Image.open(dev["image"]).resize((300, 300), Image.Resampling.LANCZOS)
                dev_photo = ctk.CTkImage(light_image=dev_img, size=(300, 300))
                
                img_label = ctk.CTkLabel(card, image=dev_photo, text="")
                img_label.pack(pady=20)
            except Exception as e:
                print(f"Error loading image: {e}")
                img_label = ctk.CTkLabel(card, text="Image not available", font=ctk.CTkFont(size=16))
                img_label.pack(pady=20)
            
            # Developer Info
            info_frame = ctk.CTkFrame(card, fg_color="#333333")
            info_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Name
            name_label = ctk.CTkLabel(info_frame,
                                    text=dev["name"],
                                    font=ctk.CTkFont(size=24, weight="bold"),
                                    text_color=dev["color"])
            name_label.pack(pady=5)
            
            # Role
            role_label = ctk.CTkLabel(info_frame,
                                    text=dev["role"],
                                    font=ctk.CTkFont(size=18),
                                    text_color="#ffffff")
            role_label.pack(pady=5)
            
            # Email
            email_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            email_frame.pack(fill=tk.X, padx=20, pady=5)
            
            email_label = ctk.CTkLabel(email_frame,
                                     text="📧",
                                     font=ctk.CTkFont(size=16))
            email_label.pack(side=tk.LEFT, padx=5)
            
            email_text = ctk.CTkLabel(email_frame,
                                    text=dev["email"],
                                    font=ctk.CTkFont(size=14))
            email_text.pack(side=tk.LEFT, padx=5)
            
            # LinkedIn Button
            linkedin_btn = ctk.CTkButton(card,
                                       text="LinkedIn Profile",
                                       width=200,
                                       height=35,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       corner_radius=10,
                                       fg_color=dev["color"],
                                       hover_color=self.darken_color(dev["color"]),
                                       command=lambda url=dev["linkedin"]: self.open_linkedin(url))
            linkedin_btn.pack(pady=20)
        
        # Footer
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a")
        footer_frame.pack(fill=tk.X, padx=20, pady=20)
        
        footer_label = ctk.CTkLabel(footer_frame,
                                   text="We design and develop with passion! 💻",
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="#ffffff")
        footer_label.pack(pady=20)
        
    def darken_color(self, color):
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Darken by 20%
        r = max(0, r - 40)
        g = max(0, g - 40)
        b = max(0, b - 40)
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def go_back(self):
        self.root.destroy()
        
    def open_linkedin(self, url):
        if url != "#":
            webbrowser.open(f"https://{url}")

if __name__ == "__main__":
    root = ctk.CTk()
    obj = Developer(root)
    root.mainloop()
