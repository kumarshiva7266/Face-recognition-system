import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import json
import os
from datetime import datetime

class HelpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Help & Support System")
        self.root.geometry("1650x850+0+0")
        self.root.resizable(True, True)
        
        # Set appearance mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.main_frame, width=1600, height=800)
        self.tabview.pack(padx=20, pady=20)
        
        # Add tabs
        self.tab1 = self.tabview.add("Help Center")
        self.tab2 = self.tabview.add("Contact Support")
        self.tab3 = self.tabview.add("FAQ")
        
        self.setup_help_center()
        self.setup_contact_support()
        self.setup_faq()
        
    def setup_help_center(self):
        # Help Center Tab
        help_frame = ctk.CTkFrame(self.tab1, fg_color="#2a2a2a")
        help_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(help_frame, 
                                  text="Welcome to Help Center",
                                   font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
                                  text_color="#ffffff")
        title_label.pack(pady=20)
        
        # Search Section
        search_frame = ctk.CTkFrame(help_frame, fg_color="#333333", corner_radius=15)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, 
                                        placeholder_text="🔍 Search for help...",
                                        width=400,
                                        height=45,
                                        font=ctk.CTkFont(size=14),
                                        corner_radius=10)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10)
        
        search_btn = ctk.CTkButton(search_frame, 
                                  text="Search",
                                  width=100,
                                  height=45,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  corner_radius=10,
                                  fg_color="#1e90ff",
                                  hover_color="#187bcd",
                                  command=self.search_help)
        search_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Quick Links
        quick_links_frame = ctk.CTkFrame(help_frame, fg_color="#333333", corner_radius=15)
        quick_links_frame.pack(fill=tk.X, padx=20, pady=20)
        
        quick_links = [
            ("📚 Documentation", self.open_documentation, "#4CAF50"),
            ("❓ FAQ", self.open_faq, "#2196F3"),
            ("📧 Contact Support", self.open_contact, "#FF9800")
        ]
        
        for text, command, color in quick_links:
            btn = ctk.CTkButton(quick_links_frame,
                               text=text,
                               width=200,
                               height=50,
                               font=ctk.CTkFont(size=16, weight="bold"),
                               corner_radius=10,
                               fg_color=color,
                               hover_color=self.darken_color(color),
                               command=command)
            btn.pack(side=tk.LEFT, padx=10, pady=10)
            
    def setup_contact_support(self):
        # Contact Support Tab
        contact_frame = ctk.CTkFrame(self.tab2, fg_color="#2a2a2a")
        contact_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contact Form
        form_frame = ctk.CTkFrame(contact_frame, fg_color="#333333", corner_radius=15)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form Fields
        fields = [
            ("Name", "Enter your name", "#4CAF50"),
            ("Email", "Enter your email", "#2196F3"),
            ("Subject", "Enter subject", "#FF9800"),
            ("Priority", ["Low", "Medium", "High"], "#9C27B0")
        ]
        
        self.form_entries = {}
        for i, (label, placeholder, color) in enumerate(fields):
            frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            ctk.CTkLabel(frame, 
                        text=label,
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=color).pack(side=tk.LEFT, padx=10)
            
            if isinstance(placeholder, list):
                # Priority dropdown
                entry = ctk.CTkOptionMenu(frame,
                                        values=placeholder,
                                        width=200,
                                        height=35,
                                        font=ctk.CTkFont(size=14),
                                        corner_radius=10,
                                        fg_color=color,
                                        button_color=color,
                                        button_hover_color=self.darken_color(color))
            else:
                # Text entry
                entry = ctk.CTkEntry(frame,
                                   placeholder_text=placeholder,
                                   width=300,
                                   height=35,
                                   font=ctk.CTkFont(size=14),
                                   corner_radius=10,
                                   fg_color="#444444",
                                   border_color=color)
            
            entry.pack(side=tk.LEFT, padx=10)
            self.form_entries[label] = entry
            
        # Message Box
        message_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        message_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ctk.CTkLabel(message_frame,
                    text="Message",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#FF5722").pack(side=tk.LEFT, padx=10)
        
        self.message_text = ctk.CTkTextbox(message_frame,
                                         width=400,
                                         height=150,
                                         font=ctk.CTkFont(size=14),
                                         corner_radius=10,
                                         fg_color="#444444",
                                         border_color="#FF5722")
        self.message_text.pack(side=tk.LEFT, padx=10, pady=10)

        # Submit Button
        submit_btn = ctk.CTkButton(form_frame,
                                  text="Submit Ticket",
                                  width=200,
                                  height=45,
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  corner_radius=10,
                                  fg_color="#FF5722",
                                  hover_color="#E64A19",
                                  command=self.submit_ticket)
        submit_btn.pack(pady=20)
        
    def setup_faq(self):
        # FAQ Tab
        faq_frame = ctk.CTkFrame(self.tab3, fg_color="#2a2a2a")
        faq_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # FAQ Items
        faq_items = [
            ("How do I start using the system?", 
             "To start using the system, first register your face in the Student Details section. Then you can use the Face Recognition module for attendance.",
             "#4CAF50"),
            ("What should I do if face recognition fails?",
             "If face recognition fails, ensure you are in a well-lit area and your face is clearly visible. You can also try re-registering your face.",
             "#2196F3"),
            ("How can I view my attendance?",
             "You can view your attendance in the Attendance Report section. The system provides detailed reports of your attendance history.",
             "#FF9800"),
            ("Is my data secure?",
             "Yes, all your data is securely stored and encrypted. We follow strict security protocols to protect your information.",
             "#9C27B0")
        ]
        
        for question, answer, color in faq_items:
            faq_item = ctk.CTkFrame(faq_frame, fg_color="#333333", corner_radius=15)
            faq_item.pack(fill=tk.X, padx=20, pady=10)
            
            question_label = ctk.CTkLabel(faq_item,
                                        text=question,
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color=color)
            question_label.pack(padx=20, pady=10)
            
            answer_label = ctk.CTkLabel(faq_item,
                                      text=answer,
                                      font=ctk.CTkFont(size=14))
            answer_label.pack(padx=20, pady=(0, 10))
            
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
        
    def search_help(self):
        query = self.search_entry.get()
        if query:
            # Implement search functionality
            messagebox.showinfo("Search", f"Searching for: {query}")
            
    def submit_ticket(self):
        # Validate form
        if not all(entry.get() for entry in self.form_entries.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        # Get form data
        ticket_data = {
            "name": self.form_entries["Name"].get(),
            "email": self.form_entries["Email"].get(),
            "subject": self.form_entries["Subject"].get(),
            "priority": self.form_entries["Priority"].get(),
            "message": self.message_text.get("1.0", tk.END).strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save ticket
        self.save_ticket(ticket_data)
        
        messagebox.showinfo("Success", "Your ticket has been submitted successfully!")
        self.clear_form()
        
    def save_ticket(self, ticket_data):
        tickets_file = "support_tickets.json"
        tickets = []
        
        if os.path.exists(tickets_file):
            with open(tickets_file, "r") as f:
                tickets = json.load(f)
                
        tickets.append(ticket_data)
        
        with open(tickets_file, "w") as f:
            json.dump(tickets, f, indent=4)
            
    def clear_form(self):
        for entry in self.form_entries.values():
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ctk.CTkOptionMenu):
                entry.set("Low")
        self.message_text.delete("1.0", tk.END)
        
    def open_documentation(self):
        webbrowser.open("www.linkedin.com/in/shiv-prasad-99a524346")
        
    def open_faq(self):
        self.tabview.set("FAQ")
        
    def open_contact(self):
        self.tabview.set("Contact Support")

if __name__ == "__main__":
    root = ctk.CTk()
    app = HelpApp(root)
    root.mainloop()
