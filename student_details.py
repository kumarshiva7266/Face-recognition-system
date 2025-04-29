import os
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Details")
        self.root.geometry("1500x800")

        # Initialize Firebase
        firebase_config_path = r"F:\face_recognition_system\firebase.json"

        # Load Firebase credentials
        cred = credentials.Certificate(firebase_config_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        # Reference to Firestore Database
        self.db = firestore.client()
        self.students_ref = self.db.collection("students")

        # Variables for storing student data
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()

        # Title Label
        title_lbl = Label(self.root, text="Student Details", font=("times new roman", 25, "bold"))
        title_lbl.pack(pady=20)

        # Main Frame
        main_frame = Frame(self.root, bd=2, relief=RIDGE)
        main_frame.place(x=10, y=70, width=1480, height=700)

        # Left Label Frame
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Details",
                                font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=730, height=680)

        # Current Course Information
        current_course_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Current Course Information",
                                          font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=150, width=720, height=120)

        # Combobox Fields
        fields = [("Department:", "var_dep", ["Select Department", "CSE","CSE(AIML)", "CSE(DS)","CSE(CS)", "IT", "Civil", "Mechanical"]),
                  ("Course:", "var_course", ["Select Course", "B.Tech", "M.Tech", "BCA", "MCA", "B.Sc", "M.Sc"]),
                  ("Year:", "var_year", ["Select Year", "First", "Second", "Third", "Fourth"]),
                  ("Semester:", "var_semester", ["Select Semester", "Semester 1", "Semester 2", "Semester 3", "Semester 4",
                                "Semester 5", "Semester 6", "Semester 7", "Semester 8"])]
        self.comboboxes = {}
        for i, (label_text, var_name, values) in enumerate(fields):
            label = Label(current_course_frame, text=label_text, font=("times new roman", 12, "bold"))
            label.grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky=W)

            combobox = ttk.Combobox(current_course_frame, textvariable=getattr(self, var_name), font=("times new roman", 12, "bold"), width=17, state="readonly")
            combobox["values"] = values
            combobox.current(0)
            combobox.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5, sticky=W)
            self.comboboxes[label_text] = combobox

        # Class Student Information
        student_info_frame = LabelFrame(left_frame, bd=2, relief=RIDGE, text="Class Student Information",
                                        font=("times new roman", 12, "bold"))
        student_info_frame.place(x=5, y=270, width=720, height=250)

        # Student Info Fields
        student_fields = [("Student ID:", "var_std_id"), ("Student Name:", "var_std_name"),
                          ("Class Division:", "var_div"), ("Roll No:", "var_roll"),
                          ("Gender:", "var_gender"), ("DOB:", "var_dob"), ("Email:", "var_email"),
                          ("Phone No:", "var_phone"), ("Address:", "var_address"), ("Teacher Name:", "var_teacher")]

        self.entries = {}
        for i, (label_text, var_name) in enumerate(student_fields):
            label = Label(student_info_frame, text=label_text, font=("times new roman", 12, "bold"))
            label.grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky=W)

            if label_text == "Gender:":
                combobox = ttk.Combobox(student_info_frame, textvariable=getattr(self, var_name), font=("times new roman", 12, "bold"), width=17, state="readonly")
                combobox["values"] = ["Select Gender", "Male", "Female", "Other"]
                combobox.current(0)
                combobox.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5, sticky=W)
                self.entries[label_text] = combobox
            else:
                entry = Entry(student_info_frame, textvariable=getattr(self, var_name), font=("times new roman", 12, "bold"), width=20)
                entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5, sticky=W)
                self.entries[label_text] = entry

        # Button Frame
        btn_frame = Frame(left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=5, y=510, width=720, height=100)

        # Buttons with oval shape
        buttons = [("Save", "green", self.save_student),
                   ("Update", "blue", self.update_student),
                   ("Delete", "red", self.delete_student),
                   ("Reset", "orange", self.reset_fields),
                   ("Take Photo Sample", "purple", self.generate_dataset),
                   ("Update Photo Sample", "darkblue", self.generate_dataset)]

        for i, (text, color, command) in enumerate(buttons):
            btn = Button(btn_frame, 
                        text=text, 
                        font=("times new roman", 12, "bold"),
                        width=17, 
                        bg=color, 
                        fg="white", 
                        command=command,
                        relief=FLAT,
                        bd=0,
                        cursor="hand2")
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            
            # Create oval shape effect
            btn.config(highlightthickness=0)
            btn.config(highlightbackground=color)
            btn.config(highlightcolor=color)
            btn.config(borderwidth=0)
            btn.config(padx=10, pady=5)
            
            # Add hover effect
            def on_enter(e, btn=btn, color=color):
                btn.config(bg=self.darken_color(color))
            
            def on_leave(e, btn=btn, color=color):
                btn.config(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Right Label Frame for Table Display
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Student Records",
                                 font=("times new roman", 12, "bold"))
        right_frame.place(x=760, y=10, width=710, height=680)

        # Search System Frame inside right_frame
        search_frame = LabelFrame(right_frame, bd=2, relief=RIDGE, text="Search System",
                                  font=("times new roman", 12, "bold"))
        search_frame.place(x=5, y=10, width=700, height=80)

        # Search Label inside the search_frame
        search_label = Label(search_frame, text="Search By:", font=("times new roman", 12, "bold"))
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Search Criteria Combobox
        self.search_combobox = ttk.Combobox(search_frame, font=("times new roman", 12, "bold"), width=17, state="readonly")
        self.search_combobox["values"] = ("Select", "student_id", "student_name", "roll_no")
        self.search_combobox.current(0)
        self.search_combobox.grid(row=0, column=1, padx=10, pady=5)

        # Search Entry Box
        self.search_entry = Entry(search_frame, font=("times new roman", 12, "bold"), width=20)
        self.search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        # Search Button with oval shape
        search_button = Button(search_frame, 
                             text="Search", 
                             font=("times new roman", 12, "bold"), 
                             bg="green", 
                             fg="white", 
                             width=15, 
                             command=self.search_student,
                             relief=FLAT,
                             bd=0,
                             cursor="hand2")
        search_button.grid(row=0, column=3, padx=10, pady=5)
        
        # Create oval shape effect for search button
        search_button.config(highlightthickness=0)
        search_button.config(highlightbackground="green")
        search_button.config(highlightcolor="green")
        search_button.config(borderwidth=0)
        search_button.config(padx=10, pady=5)
        
        # Add hover effect for search button
        def on_enter_search(e, btn=search_button):
            btn.config(bg=self.darken_color("green"))
        
        def on_leave_search(e, btn=search_button):
            btn.config(bg="green")
        
        search_button.bind("<Enter>", on_enter_search)
        search_button.bind("<Leave>", on_leave_search)

        # Table to Display Search Results
        self.result_frame = Frame(right_frame, bd=2, relief=RIDGE)
        self.result_frame.place(x=5, y=100, width=700, height=570)

        # Table to display results
        self.result_tree = ttk.Treeview(self.result_frame, columns=("ID", "Name", "Roll No", "Phone No", "Email", "Teacher"))
        self.result_tree.heading("ID", text="Student ID")
        self.result_tree.heading("Name", text="Student Name")
        self.result_tree.heading("Roll No", text="Roll No")
        self.result_tree.heading("Phone No", text="Phone No")
        self.result_tree.heading("Email", text="Email")
        self.result_tree.heading("Teacher", text="Teacher Name")

        self.result_tree["show"] = "headings"  # Hide the first column (ID)
        self.result_tree.grid(row=0, column=0, sticky='nsew')  # Use grid for better layout management

        # Add a scrollbar to the table
        scrollbar = ttk.Scrollbar(self.result_frame, orient=VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscroll=scrollbar.set)
        # If you are using grid for the parent container, change the scrollbar to grid:
        scrollbar.grid(row=0, column=1, sticky='ns')  # Adjust according to your layout

        self.fetch_data()

    def save_student(self):
        """Save student data into Firebase."""
        if not self.validate_fields():
            messagebox.showwarning("Validation Error", "Please fill in all required fields.")
            return

        try:
            # Get all values first to ensure they're not empty
            student_id = self.var_std_id.get().strip()
            student_name = self.var_std_name.get().strip()
            roll_no = self.var_roll.get().strip()
            course = self.comboboxes["Course:"].get()
            department = self.comboboxes["Department:"].get()
            year = self.comboboxes["Year:"].get()
            semester = self.comboboxes["Semester:"].get()

            # Validate required fields
            if not all([student_id, student_name, roll_no, course, department, year, semester]):
                messagebox.showwarning("Validation Error", "Please fill in all required fields.")
                return

            # Create student data with both old and new field names for compatibility
            student_data = {
                # New field names (used by face recognition)
                "id": student_id,
                "name": student_name,
                "roll_no": roll_no,
                "course": course,
                "department": department,
                "year": year,
                "semester": semester,
                
                # Old field names (for backward compatibility)
                "student_id": student_id,
                "student_name": student_name,
                
                # Additional fields
                "class_division": self.var_div.get().strip(),
                "gender": self.entries["Gender:"].get(),
                "dob": self.var_dob.get().strip(),
                "email": self.var_email.get().strip(),
                "phone_no": self.var_phone.get().strip(),
                "address": self.var_address.get().strip(),
                "teacher_name": self.var_teacher.get().strip()
            }

            # Save data to Firebase Firestore using the student ID as the document ID
            self.students_ref.document(student_id).set(student_data)

            messagebox.showinfo("Success", "Student details saved successfully.")
            self.fetch_data()
            self.reset_fields()  # Reset fields after successful save

        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")

    def update_student(self):
        """Update student data in Firebase."""
        if not self.validate_fields():
            messagebox.showwarning("Validation Error", "Please fill in all required fields.")
            return

        try:
            student_id = self.var_std_id.get()
            student_doc = self.students_ref.document(student_id)

            if student_doc.get().exists:
                student_doc.update({
                    "student_name": self.var_std_name.get(),
                    "class_division": self.var_div.get(),
                    "roll_no": self.var_roll.get(),
                    "gender": self.entries["Gender:"].get(),
                    "dob": self.var_dob.get(),
                    "email": self.var_email.get(),
                    "phone_no": self.var_phone.get(),
                    "address": self.var_address.get(),
                    "teacher_name": self.var_teacher.get(),
                    "department": self.comboboxes["Department:"].get(),
                    "course": self.comboboxes["Course:"].get(),
                    "year": self.comboboxes["Year:"].get(),
                    "semester": self.comboboxes["Semester:"].get(),
                })

                messagebox.showinfo("Success", "Student details updated successfully.")
                self.fetch_data()
            else:
                messagebox.showerror("Error", "Student ID not found.")

        except Exception as e:
            messagebox.showerror("Firebase Error", f"Error: {e}")

    def delete_student(self):
        """Delete student data from Firebase."""
        student_id = self.var_std_id.get()
        roll_no = self.var_roll.get()

        if not student_id and not roll_no:
            messagebox.showwarning("Validation Error", "Please enter a valid Student ID or Roll No.")
            return

        try:
            if student_id:
                # Delete by student ID
                student_doc = self.students_ref.document(student_id)
                if student_doc.get().exists:
                    student_doc.delete()
                    messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully.")
                    self.reset_fields()
                    self.fetch_data()
                else:
                    messagebox.showerror("Error", f"Student ID {student_id} not found.")
            elif roll_no:
                # Delete by roll number
                students = self.students_ref.where("roll_no", "==", roll_no).stream()
                deleted = False
                for student in students:
                    student.reference.delete()
                    deleted = True

                if deleted:
                    messagebox.showinfo("Success", f"Student with Roll No {roll_no} deleted successfully.")
                    self.reset_fields()
                    self.fetch_data()
                else:
                    messagebox.showerror("Error", f"No student found with Roll No {roll_no}.")

        except Exception as e:
            print(f"Error deleting student: {e}")
            messagebox.showerror("Firebase Error", f"Error deleting student: {e}")

    def reset_fields(self):
        """Reset all input fields."""
        self.var_dep.set("")
        self.var_course.set("")
        self.var_year.set("")
        self.var_semester.set("")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        # Reset comboboxes
        for combobox in self.comboboxes.values():
            combobox.set(combobox["values"][0])
        # Reset entries
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set(entry["values"][0])
            else:
                entry.delete(0, END)

    def validate_fields(self):
        """Validate student fields before saving."""
        if (self.var_std_id.get() == "" or
            self.var_std_name.get() == "" or
            self.var_div.get() == "" or
            self.var_roll.get() == "" or
            self.entries["Gender:"].get() == "Select Gender" or
            self.var_dob.get() == "" or
            self.var_email.get() == "" or
            self.var_phone.get() == "" or
            self.var_address.get() == "" or
            self.var_teacher.get() == "" or
            self.comboboxes["Department:"].get() == "Select Department" or
            self.comboboxes["Course:"].get() == "Select Course" or
            self.comboboxes["Year:"].get() == "Select Year" or
            self.comboboxes["Semester:"].get() == "Select Semester"):

            print("Validation Failed.")
            return False
        print("Validation Passed.")
        return True

    def search_student(self):
        """Search for a student in Firebase and load their details."""
        search_value = self.search_entry.get()
        search_by = self.search_combobox.get()

        if search_value and search_by != "Select":
            try:
                self.result_tree.delete(*self.result_tree.get_children())  # Clear table

                # Search in Firebase
                students = self.students_ref.where(search_by, "==", search_value).stream()
                found = False
                
                for student in students:
                    found = True
                    data = student.to_dict()
                    
                    # Insert into treeview
                    self.result_tree.insert("", "end", values=(
                        data["student_id"],
                        data["student_name"],
                        data["roll_no"],
                        data["phone_no"],
                        data["email"],
                        data["teacher_name"]
                    ))
                    
                    # Load student details into the form
                    self.var_std_id.set(data.get("student_id", ""))
                    self.var_std_name.set(data.get("student_name", ""))
                    self.var_div.set(data.get("class_division", ""))
                    self.var_roll.set(data.get("roll_no", ""))
                    self.entries["Gender:"].set(data.get("gender", "Select Gender"))
                    self.var_dob.set(data.get("dob", ""))
                    self.var_email.set(data.get("email", ""))
                    self.var_phone.set(data.get("phone_no", ""))
                    self.var_address.set(data.get("address", ""))
                    self.var_teacher.set(data.get("teacher_name", ""))
                    self.comboboxes["Department:"].set(data.get("department", "Select Department"))
                    self.comboboxes["Course:"].set(data.get("course", "Select Course"))
                    self.comboboxes["Year:"].set(data.get("year", "Select Year"))
                    self.comboboxes["Semester:"].set(data.get("semester", "Select Semester"))
                
                if not found:
                    messagebox.showinfo("Search Result", "No student found with the given criteria.")

            except Exception as e:
                messagebox.showerror("Firebase Error", f"Error: {e}")

    def fetch_data(self):
        """Fetch student data from Firebase and display it in the table."""
        try:
            # Clear the existing Treeview data
            self.result_tree.delete(*self.result_tree.get_children())

            # Fetch all student documents from Firebase
            students = self.students_ref.stream()
            for student in students:
                data = student.to_dict()

                # Verify that necessary fields exist in the document
                student_id = data.get("student_id", "N/A")
                student_name = data.get("student_name", "N/A")
                roll_no = data.get("roll_no", "N/A")
                phone_no = data.get("phone_no", "N/A")
                email = data.get("email", "N/A")
                teacher_name = data.get("teacher_name", "N/A")

                # Insert student data into the Treeview
                self.result_tree.insert("", "end", values=(
                    student_id,
                    student_name,
                    roll_no,
                    phone_no,
                    email,
                    teacher_name
                ))

        except Exception as e:
            print(f"Error fetching data: {e}")
            messagebox.showerror("Firebase Error", f"Failed to fetch student data: {e}")

    def generate_dataset(self):
        """Generates a dataset of face images for a student."""
        user_id = self.var_std_id.get()
        if not user_id:
            messagebox.showwarning("Input Error", "Please enter a valid Student ID before capturing photos.")
            return

        data_dir = f"F:/face_recognition_system/captured_faces/user_{user_id}"
        os.makedirs(data_dir, exist_ok=True)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        sample_count = 0
        max_samples = 100

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 6)

            for (x, y, w, h) in faces:
                sample_count += 1
                face_img = gray[y:y+h, x:x+w]
                cv2.imwrite(f"{data_dir}/sample_{sample_count}.jpg", face_img)  # FIXED PATH
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow("Face Capture", frame)

            if cv2.waitKey(1)==13 & 0xFF == ord('q') or sample_count >= max_samples:
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", f"Captured {sample_count} images for User ID {user_id}.")

    def darken_color(self, color):
        """Darken a color for hover effect."""
        try:
            # Handle named colors
            if color in ['blue', 'red', 'green', 'orange', 'purple', 'darkblue']:
                color_map = {
                    'blue': '#3498db',
                    'red': '#e74c3c',
                    'green': '#2ecc71',
                    'orange': '#e67e22',
                    'purple': '#9b59b6',
                    'darkblue': '#2980b9'
                }
                color = color_map.get(color, '#3498db')
            
            # Ensure color is in hex format
            if not color.startswith('#'):
                return color
                
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Darken by 20%
            r = max(0, r - 40)
            g = max(0, g - 40)
            b = max(0, b - 40)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            print(f"Error darkening color: {e}")
            return color  # Return original color if there's an error

# Driver code
if __name__ == "__main__":
    try:
        root = Tk()
        obj = Student(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")