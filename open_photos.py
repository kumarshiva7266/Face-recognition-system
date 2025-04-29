import os
import subprocess
import time
from tkinter import messagebox
import threading
from PIL import Image, ImageTk
import cv2
import numpy as np

class PhotoManager:
    def __init__(self, root=None):
        self.root = root
        self.photo_dir = r"F:\face_recognition_system\captured_faces"
        self.is_loading = False
        self.thumbnail_size = (150, 150)
        self.thumbnails = []
        
    def open_photos(self):
        """Open the photos directory with smooth loading and error handling"""
        try:
            if not os.path.exists(self.photo_dir):
                raise FileNotFoundError(f"Directory not found: {self.photo_dir}")
                
            # Start loading animation if root window exists
            if self.root:
                self.start_loading_animation()
                
            # Open directory in a separate thread to prevent UI freezing
            threading.Thread(target=self._open_directory, daemon=True).start()
            
        except Exception as e:
            self.handle_error(e)
            
    def _open_directory(self):
        """Open directory with smooth transition"""
        try:
            # Use subprocess for better control
            subprocess.Popen(['explorer', self.photo_dir])
            
            # Update status if root window exists
            if self.root:
                self.root.after(100, self.stop_loading_animation)
                self.root.after(200, lambda: messagebox.showinfo("Success", "Photos folder opened successfully!"))
                
        except Exception as e:
            self.handle_error(e)
            
    def start_loading_animation(self):
        """Start loading animation"""
        self.is_loading = True
        # Add loading animation logic here if needed
        
    def stop_loading_animation(self):
        """Stop loading animation"""
        self.is_loading = False
        # Add stop animation logic here if needed
        
    def handle_error(self, error):
        """Handle errors with user-friendly messages"""
        error_message = f"❌ Error: {str(error)}"
        print(error_message)
        if self.root:
            messagebox.showerror("Error", error_message)
            
    def get_photo_count(self):
        """Get total number of photos in directory"""
        try:
            count = sum([len(files) for _, _, files in os.walk(self.photo_dir)])
            return count
        except Exception as e:
            self.handle_error(e)
            return 0
            
    def generate_thumbnails(self, max_thumbnails=12):
        """Generate thumbnails for preview"""
        try:
            self.thumbnails = []
            count = 0
            
            for root, _, files in os.walk(self.photo_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        try:
                            # Load and resize image
                            img_path = os.path.join(root, file)
                            img = cv2.imread(img_path)
                            if img is not None:
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                img = Image.fromarray(img)
                                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
                                self.thumbnails.append(img)
                                count += 1
                                
                                if count >= max_thumbnails:
                                    break
                        except Exception as e:
                            print(f"Error processing thumbnail: {e}")
                            
            return self.thumbnails
            
        except Exception as e:
            self.handle_error(e)
            return []
            
    def get_directory_info(self):
        """Get detailed information about the photos directory"""
        try:
            info = {
                "total_photos": self.get_photo_count(),
                "directory_size": self.get_directory_size(),
                "last_modified": self.get_last_modified(),
                "subfolders": self.get_subfolder_count()
            }
            return info
        except Exception as e:
            self.handle_error(e)
            return {}
            
    def get_directory_size(self):
        """Calculate total size of the photos directory"""
        try:
            total_size = 0
            for dirpath, _, filenames in os.walk(self.photo_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            return self.format_size(total_size)
        except Exception as e:
            self.handle_error(e)
            return "Unknown"
            
    def get_last_modified(self):
        """Get last modification time of the directory"""
        try:
            return time.ctime(os.path.getmtime(self.photo_dir))
        except Exception as e:
            self.handle_error(e)
            return "Unknown"
            
    def get_subfolder_count(self):
        """Count number of subfolders"""
        try:
            return len([name for name in os.listdir(self.photo_dir) 
                       if os.path.isdir(os.path.join(self.photo_dir, name))])
        except Exception as e:
            self.handle_error(e)
            return 0
            
    @staticmethod
    def format_size(size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

# Example usage
if __name__ == "__main__":
    photo_manager = PhotoManager()
    photo_manager.open_photos()
    
    # Get directory information
    info = photo_manager.get_directory_info()
    print("Directory Information:")
    print(f"Total Photos: {info.get('total_photos', 0)}")
    print(f"Directory Size: {info.get('directory_size', 'Unknown')}")
    print(f"Last Modified: {info.get('last_modified', 'Unknown')}")
    print(f"Subfolders: {info.get('subfolders', 0)}")
