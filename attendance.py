import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from PIL import Image, ImageTk
import numpy as np


class AttendanceManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Attendance Management System")
        self.root.geometry("1650x850+0+0")
        self.root.configure(bg="#2c3e50")

        # Initialize Firebase
        firebase_config_path = r"F:\face_recognition_system\firebase.json"
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_config_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.students_ref = self.db.collection("students")

        # Variables
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_roll = StringVar()
        self.var_branch = StringVar()
        self.var_year = StringVar()
        self.var_days_present = StringVar()
        self.var_date = StringVar()
        self.var_attendance_status = StringVar()
        self.var_search = StringVar()

        # Custom style
        style = ttk.Style()
        style.configure("Custom.TButton", 
                       font=("Helvetica", 12, "bold"),
                       padding=10,
                       background="#3498db",
                       foreground="white")
        
        style.configure("Custom.TEntry",
                       font=("Helvetica", 12),
                       padding=5)

        # Main Frame
        main_frame = Frame(self.root, bg="#2c3e50")
        main_frame.place(x=0, y=0, width=1650, height=850)

        # Title Frame
        title_frame = Frame(main_frame, bg="#2c3e50")
        title_frame.place(x=0, y=0, width=1650, height=80)

        title_lbl = Label(title_frame, 
                         text="Advanced Attendance Management System", 
                         font=("Helvetica", 30, "bold"), 
                         fg="#ecf0f1", 
                         bg="#2c3e50")
        title_lbl.pack(pady=20)

        # Left Frame for Student Details
        left_frame = Frame(main_frame, bg="#34495e", bd=2, relief=GROOVE)
        left_frame.place(x=50, y=100, width=500, height=700)

        # Search Frame
        search_frame = Frame(left_frame, bg="#34495e")
        search_frame.place(x=20, y=20, width=460, height=60)

        search_entry = Entry(search_frame, 
                           textvariable=self.var_search,
                           font=("Helvetica", 12),
                           bg="#ecf0f1",
                           fg="#2c3e50",
                           relief=FLAT)
        search_entry.place(x=10, y=10, width=200, height=40)

        search_btn = Button(search_frame,
                          text="Search",
                          font=("Helvetica", 12, "bold"),
                          fg="white",
                          bg="#3498db",
                          activebackground="#2980b9",
                          activeforeground="white",
                          relief=FLAT,
                          borderwidth=0,
                          cursor="hand2",
                          command=self.search_student)
        search_btn.place(x=220, y=10, width=100, height=40)

        fetch_btn = Button(search_frame,
                         text="Fetch",
                         font=("Helvetica", 12, "bold"),
                         fg="white",
                         bg="#2ecc71",
                         activebackground="#27ae60",
                         activeforeground="white",
                         relief=FLAT,
                         borderwidth=0,
                         cursor="hand2",
                         command=self.fetch_student_details)
        fetch_btn.place(x=330, y=10, width=100, height=40)

        # Student Details Frame
        details_frame = Frame(left_frame, bg="#34495e")
        details_frame.place(x=20, y=100, width=460, height=500)

        # Student Info Fields
        student_fields = [
            ("Student ID:", "var_id"),
            ("Name:", "var_name"),
            ("Roll No:", "var_roll"),
            ("Branch:", "var_branch"),
            ("Year:", "var_year"),
            ("Days Present:", "var_days_present"),
            ("Date:", "var_date"),
            ("Status:", "var_attendance_status")
        ]

        self.entries = {}
        for i, (label_text, var_name) in enumerate(student_fields):
            label = Label(details_frame, 
                         text=label_text, 
                         font=("Helvetica", 12, "bold"),
                         fg="#ecf0f1",
                         bg="#34495e")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            
            if label_text == "Status:":
                combobox = ttk.Combobox(details_frame,
                                      textvariable=getattr(self, var_name),
                                      font=("Helvetica", 12),
                                      state="readonly",
                                      values=["Present", "Absent", "Late"])
                combobox.grid(row=i, column=1, padx=10, pady=10)
                self.entries[label_text] = combobox
            else:
                entry = Entry(details_frame,
                            textvariable=getattr(self, var_name),
                            font=("Helvetica", 12),
                            bg="#ecf0f1",
                            fg="#2c3e50",
                            relief=FLAT)
                entry.grid(row=i, column=1, padx=10, pady=10)
            self.entries[label_text] = entry

        # Buttons Frame
        buttons_frame = Frame(left_frame, bg="#34495e")
        buttons_frame.place(x=20, y=620, width=460, height=60)

        buttons = [
            ("Import CSV", "#2ecc71", self.Import_student),
            ("Update", "#3498db", self.update_attendance),
            ("Reset", "#e74c3c", self.reset_fields)
        ]

        for i, (text, color, command) in enumerate(buttons):
            btn = Button(buttons_frame,
                        text=text,
                        font=("Helvetica", 12, "bold"),
                        fg="white",
                        bg=color,
                        activebackground=color,
                        activeforeground="white",
                        relief=FLAT,
                        borderwidth=0,
                        cursor="hand2",
                        command=command)
            btn.place(x=10 + i*150, y=10, width=140, height=40)

        # Right Frame for Attendance Records and Statistics
        self.right_frame = Frame(main_frame, bg="#34495e", bd=2, relief=GROOVE)
        self.right_frame.place(x=600, y=100, width=1000, height=700)

        # Attendance Table Frame
        table_frame = Frame(self.right_frame, bg="#34495e")
        table_frame.place(x=20, y=20, width=960, height=300)

        # Create Treeview with scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        self.AttendanceReportTable = ttk.Treeview(table_frame, 
                                                 columns=("id", "name", "roll_no", "branch", "year", "date", "status"),
                                                 xscrollcommand=scroll_x.set,
                                                 yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        # Configure columns
        self.AttendanceReportTable.heading("id", text="ID")
        self.AttendanceReportTable.heading("name", text="Name")
        self.AttendanceReportTable.heading("roll_no", text="Roll No")
        self.AttendanceReportTable.heading("branch", text="Branch")
        self.AttendanceReportTable.heading("year", text="Year")
        self.AttendanceReportTable.heading("date", text="Date")
        self.AttendanceReportTable.heading("status", text="Status")

        self.AttendanceReportTable["show"] = "headings"
        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        # Statistics Frame
        stats_frame = Frame(self.right_frame, bg="#34495e")
        stats_frame.place(x=20, y=340, width=960, height=340)

        # Create matplotlib figure for statistics
        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=stats_frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # Initialize data
        self.fetch_data()
        self.update_statistics()

    def Import_student(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            data = pd.read_csv(file_path)
            expected_headers = ["ID", "Name", "Roll No", "Course", "Department", "Year", "Semester", "Time", "Date", "Status"]
            
            if list(data.columns) != expected_headers:
                raise ValueError(f"CSV file must have the following headers: {expected_headers}")

            for index, row in data.iterrows():
                student_data = {
                    "id": str(row["ID"]),
                    "name": str(row["Name"]) if pd.notna(row["Name"]) else "N/A",
                    "roll_no": str(row["Roll No"]),
                    "branch": str(row["Department"]) if pd.notna(row["Department"]) else "N/A",
                    "year": str(row["Year"]) if pd.notna(row["Year"]) else "N/A",
                    "date": str(row["Date"]),
                    "attendance_status": str(row["Status"])
                }
                self.students_ref.document(student_data["id"]).set(student_data)

            messagebox.showinfo("Success", "CSV file imported successfully!")
            self.fetch_data()
            self.update_statistics()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to import file: {str(e)}")

    def search_student(self):
        search_term = self.var_search.get().lower()
        if not search_term:
            self.fetch_data()
            return

        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        students = self.students_ref.stream()
        
        for student in students:
            data = student.to_dict()
            if (search_term in data.get("id", "").lower() or
                search_term in data.get("name", "").lower() or
                search_term in data.get("roll_no", "").lower()):
                self.AttendanceReportTable.insert("", "end", values=(
                    data.get("id", ""),
                    data.get("name", ""),
                    data.get("roll_no", ""),
                    data.get("branch", ""),
                    data.get("year", ""),
                    data.get("date", ""),
                    data.get("attendance_status", "")
                ))

    def update_attendance(self):
        try:
            student_id = self.var_id.get()
            if not student_id:
                messagebox.showwarning("Input Error", "Please enter a valid Student ID")
                return

            attendance_data = {
                "id": student_id,
                "name": self.var_name.get(),
                "roll_no": self.var_roll.get(),
                "branch": self.var_branch.get(),
                "year": self.var_year.get(),
                "date": self.var_date.get(),
                "attendance_status": self.var_attendance_status.get()
            }

            self.students_ref.document(student_id).set(attendance_data)
            messagebox.showinfo("Success", "Attendance updated successfully!")
            self.fetch_data()
            self.update_statistics()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update attendance: {str(e)}")

    def fetch_data(self):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        students = self.students_ref.stream()
        
        for student in students:
            data = student.to_dict()
            self.AttendanceReportTable.insert("", "end", values=(
                data.get("id", ""),
                data.get("name", ""),
                data.get("roll_no", ""),
                data.get("branch", ""),
                data.get("year", ""),
                data.get("date", ""),
                data.get("attendance_status", "")
            ))

    def update_statistics(self):
        try:
            self.ax.clear()
            students = self.students_ref.stream()
            
            # Count attendance status for pie chart
            status_counts = {"Present": 0, "Absent": 0, "Late": 0}
            for student in students:
                status = student.to_dict().get("attendance_status", "")
                if status in status_counts:
                    status_counts[status] += 1

            # Create pie chart
            labels = status_counts.keys()
            sizes = status_counts.values()
            colors = ['#2ecc71', '#e74c3c', '#f1c40f']
            
            self.ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                       startangle=90, shadow=True)
            self.ax.axis('equal')
            self.ax.set_title('Attendance Distribution')
            
            self.canvas.draw()

            # Create daily attendance percentage graph
            self.update_daily_attendance()

        except Exception as e:
            print(f"Error updating statistics: {e}")

    def update_daily_attendance(self):
        try:
            # Create a new figure for daily attendance
            fig2, ax2 = plt.subplots(figsize=(9, 4))
            
            # Get all attendance records
            students = self.students_ref.stream()
            
            # Dictionary to store daily attendance counts
            daily_counts = {}
            total_students = set()
            
            for student in students:
                data = student.to_dict()
                date_str = data.get("date", "")
                if date_str:
                    try:
                        # Try to parse the date in DD/MM/YYYY format
                        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                        # Convert to YYYY-MM-DD format for consistency
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                        
                        # Skip Sundays
                        if date_obj.weekday() == 6:  # 6 is Sunday
                            continue
                            
                        if formatted_date not in daily_counts:
                            daily_counts[formatted_date] = {"Present": 0, "Total": 0}
                        
                        daily_counts[formatted_date]["Total"] += 1
                        if data.get("attendance_status") == "Present":
                            daily_counts[formatted_date]["Present"] += 1
                    except ValueError:
                        # If date is already in YYYY-MM-DD format
                        try:
                            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                            if date_obj.weekday() == 6:  # 6 is Sunday
                                continue
                                
                            if date_str not in daily_counts:
                                daily_counts[date_str] = {"Present": 0, "Total": 0}
                            
                            daily_counts[date_str]["Total"] += 1
                            if data.get("attendance_status") == "Present":
                                daily_counts[date_str]["Present"] += 1
                        except ValueError:
                            print(f"Invalid date format: {date_str}")
                            continue
                
                total_students.add(data.get("id", ""))

            # Calculate percentages
            dates = sorted(daily_counts.keys())
            percentages = []
            for date in dates:
                if daily_counts[date]["Total"] > 0:
                    percentage = (daily_counts[date]["Present"] / daily_counts[date]["Total"]) * 100
                    percentages.append(percentage)
                else:
                    percentages.append(0)

            # Create bar chart
            bars = ax2.bar(dates, percentages, color='#3498db')
            
            # Add percentage labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom')

            # Customize the graph
            ax2.set_title('Daily Attendance Percentage (Excluding Sundays)')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Attendance Percentage')
            ax2.set_ylim(0, 100)  # Set y-axis from 0 to 100%
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
            # Create a new frame for the daily attendance graph
            daily_frame = Frame(self.right_frame, bg="#34495e")
            daily_frame.place(x=20, y=700, width=960, height=340)
            
            # Display the graph
            canvas2 = FigureCanvasTkAgg(fig2, master=daily_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=BOTH, expand=1)

        except Exception as e:
            print(f"Error updating daily attendance graph: {e}")

    def reset_fields(self):
        for var in [self.var_id, self.var_name, self.var_roll, self.var_branch, 
                   self.var_year, self.var_days_present, self.var_date, self.var_attendance_status]:
            var.set("")
        self.var_search.set("")
        self.fetch_data()
        self.update_statistics()

    def fetch_student_details(self):
        try:
            search_term = self.var_search.get().strip()
            if not search_term:
                messagebox.showwarning("Input Error", "Please enter ID, Name, or Roll No to fetch details")
                return

            # Search in Firestore
            students = self.students_ref.stream()
            found = False
            
            for student in students:
                data = student.to_dict()
                if (search_term == data.get("id", "") or
                    search_term.lower() == data.get("name", "").lower() or
                    search_term == data.get("roll_no", "")):
                    
                    # Fill the form with student details
                    self.var_id.set(data.get("id", ""))
                    self.var_name.set(data.get("name", ""))
                    self.var_roll.set(data.get("roll_no", ""))
                    self.var_branch.set(data.get("branch", ""))
                    self.var_year.set(data.get("year", ""))
                    self.var_days_present.set(str(self.calculate_days_present(data.get("id", ""))))
                    self.var_date.set(datetime.now().strftime("%Y-%m-%d"))
                    
                    # Set attendance status to Present by default
                    self.var_attendance_status.set("Present")
                    
                    found = True
                    messagebox.showinfo("Success", "Student details fetched successfully!")
                    break

            if not found:
                messagebox.showerror("Error", "No student found with the given details")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch student details: {str(e)}")

    def calculate_days_present(self, student_id):
        try:
            students = self.students_ref.stream()
            unique_dates = set()
            for student in students:
                data = student.to_dict()
                if data.get("id") == student_id and data.get("attendance_status") == "Present":
                    unique_dates.add(data.get("date", ""))
            return len(unique_dates)
        except Exception as e:
            print(f"Error calculating days present: {e}")
            return 0

    def __del__(self):
        try:
            # Close matplotlib figures
            plt.close('all')
            
            # Clear Firebase app if it exists
            if firebase_admin._apps:
                firebase_admin.delete_app(firebase_admin.get_app())
                
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def on_closing(self):
        try:
            # First destroy all widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Then clean up resources
            self.__del__()
            
            # Finally destroy the root window
            self.root.destroy()
            
            # Force garbage collection
            import gc
            gc.collect()
            
        except Exception as e:
            print(f"Error during window closing: {e}")

# Driver Code
if __name__ == "__main__":
    try:
        root = Tk()
        obj = AttendanceManagement(root)
        # Add window close handler
        root.protocol("WM_DELETE_WINDOW", obj.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")