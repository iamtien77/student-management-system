"""
Màn hình xem điểm - hiển thị bảng điểm và GPA của sinh viên.
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, COLORS, FONTS
from models.student import Student
from models.class_section import ClassSection
from models.course import Course

class ViewGradesView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - View Grades")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(900, 600)
        self._build_ui()

    def _build_ui(self):
        # Thanh điều hướng
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="View Grades & GPA", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        student = Student.find_by_id(self._account.username)
        if not student:
            tk.Label(self.root, text="Student record not found.",
                     font=FONTS["body"], fg=COLORS["error"],
                     bg=COLORS["bg"]).pack(pady=50)
            return

        # Tính GPA trước khi hiển thị
        sem_gpa = student.calculateSemesterGPA()
        cum_gpa = student.calculateCumulativeGPA()

        info = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        info.pack(fill="x", padx=20, pady=(15, 10))
        
        tk.Label(info, text="Academic Performance", font=FONTS["heading"], 
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(10, 5))
        
        gpa_frame = tk.Frame(info, bg=COLORS["card"])
        gpa_frame.pack(pady=(0, 10))
        
        tk.Label(gpa_frame, text=f"Semester GPA (Finalized only): {sem_gpa}", 
                 font=FONTS["body_bold"], bg=COLORS["card"]).grid(row=0, column=0, padx=20)
        tk.Label(gpa_frame, text=f"Cumulative GPA (Finalized only): {cum_gpa}", 
                 font=FONTS["body_bold"], bg=COLORS["card"]).grid(row=0, column=1, padx=20)

        # Bảng điểm học tập
        table_frame = tk.Frame(self.root, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        columns = ("class", "course", "credits", "midterm", "assign", "attend", "final", "summary", "letter", "status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        style = ttk.Style()
        style.configure("Treeview", font=FONTS["body"], rowheight=28)
        style.configure("Treeview.Heading", font=FONTS["body_bold"])

        headings = [
            ("class", "Class", 80),
            ("course", "Course Name", 150),
            ("credits", "Cr", 40),
            ("midterm", "Mid", 50),
            ("assign", "Assn", 50),
            ("attend", "Att", 50),
            ("final", "Fin", 50),
            ("summary", "Total", 50),
            ("letter", "Ltr", 50),
            ("status", "Status", 80)
        ]

        for col_id, title, width in headings:
            tree.heading(col_id, text=title)
            tree.column(col_id, width=width, anchor="center" if col_id != "course" else "w")

        tree.tag_configure("finalized", background="#D5F5E3")
        tree.tag_configure("draft", background="#F2F3F4")

        grades = student.viewGrades()
        for g in grades:
            # Lấy tên môn học và số tín chỉ
            course_name = "Unknown"
            credits = 0
            cs = ClassSection.find_by_code(g.classCode)
            if cs:
                course = Course.find_by_code(cs.courseCode)
                if course:
                    course_name = course.courseName
                    credits = course.credits

            tag = "finalized" if g.status == "Finalized" else "draft"
            tree.insert("", "end", values=(
                g.classCode,
                course_name,
                credits,
                g.midtermGrade,
                g.assignmentGrade,
                g.attendanceGrade,
                g.finalExamGrade,
                g.finalSummaryGrade,
                g.letterGrade,
                g.status
            ), tags=(tag,))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

