"""
Màn hình chương trình đào tạo - UC15
Hiển thị khung chương trình với trạng thái Hoàn thành/Chưa hoàn thành.
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView, COLORS, FONTS


class TrainingProgramView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Training Program")
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
        tk.Label(navbar, text="View Training Program", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Tải thông tin sinh viên và chương trình
        from models.student import Student
        student = Student.find_by_id(self._account.username)
        if not student:
            tk.Label(self.root, text="Student record not found.",
                     font=FONTS["body"], fg=COLORS["error"],
                     bg=COLORS["bg"]).pack(pady=50)
            return

        program = student.viewTrainingProgram()
        if not program:
            tk.Label(self.root, text="No training program assigned.",
                     font=FONTS["body"], fg=COLORS["text_light"],
                     bg=COLORS["bg"]).pack(pady=50)
            return

        # Thông tin chương trình
        info = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        info.pack(fill="x", padx=20, pady=(15, 10))
        tk.Label(info, text=f"Program: {program.programName}  ({program.programID})",
                 font=FONTS["heading"], fg=COLORS["primary"],
                 bg=COLORS["card"]).pack(padx=15, pady=10)

        # Bảng môn học
        table_frame = tk.Frame(self.root, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        columns = ("code", "name", "credits", "prerequisites", "status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                             selectmode="browse")

        style = ttk.Style()
        style.configure("Treeview", font=FONTS["body"], rowheight=28)
        style.configure("Treeview.Heading", font=FONTS["body_bold"])

        tree.heading("code", text="Course Code")
        tree.heading("name", text="Course Name")
        tree.heading("credits", text="Credits")
        tree.heading("prerequisites", text="Prerequisites")
        tree.heading("status", text="Status")

        tree.column("code", width=100)
        tree.column("name", width=250)
        tree.column("credits", width=70, anchor="center")
        tree.column("prerequisites", width=150)
        tree.column("status", width=100, anchor="center")

        tree.tag_configure("completed", background="#D5F5E3", foreground="#27AE60")
        tree.tag_configure("incomplete", background="#FADBD8", foreground="#C0392B")

        courses = program.get_course_list()
        for course in courses:
            status = program.getCourseStatus(course.courseCode, student.studentID)
            tag = "completed" if status == "Completed" else "incomplete"
            tree.insert("", "end", values=(
                course.courseCode, course.courseName,
                course.credits, course.prerequisites, status
            ), tags=(tag,))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

