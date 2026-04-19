"""
Màn hình chốt điểm - UC18
Quản trị viên chọn lớp â†’ chốt điểm nháp â†’ khóa vĩnh viễn â†’ tính GPA.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView, COLORS, FONTS


class FinalizeGradesView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Finalize Grades")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1000, 650)
        self._build_ui()

    def _build_ui(self):
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="Finalize Grades", font=FONTS["nav"], fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Chọn lớp học phần
        from models.class_section import ClassSection
        all_classes = ClassSection.get_all()

        select = tk.Frame(self.root, bg=COLORS["bg"])
        select.pack(fill="x", padx=20, pady=10)

        tk.Label(select, text="Select Class:", font=FONTS["body_bold"],
                 bg=COLORS["bg"]).pack(side="left")
        class_codes = [cs.classCode for cs in all_classes]
        self._class_var = tk.StringVar()
        combo = ttk.Combobox(select, textvariable=self._class_var,
                              values=class_codes, state="readonly", font=FONTS["body"])
        combo.pack(side="left", padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: self._load_grades())

        tk.Button(select, text="Finalize Selected Class", font=FONTS["button"],
                  bg=COLORS["error"], fg="white", bd=0, padx=20, pady=5,
                  cursor="hand2", command=self._finalize).pack(side="right")

        # Bảng điểm
        table_frame = tk.Frame(self.root, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        columns = ("student_id", "name", "midterm", "assignment",
                   "attendance", "final_exam", "summary", "letter", "status")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col, heading, w in [
            ("student_id", "Student ID", 100), ("name", "Name", 150),
            ("midterm", "Midterm", 70), ("assignment", "Assignment", 80),
            ("attendance", "Attendance", 80), ("final_exam", "Final Exam", 80),
            ("summary", "Summary", 70), ("letter", "Letter", 60),
            ("status", "Status", 80)
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w, anchor="center" if col not in ("student_id", "name") else "w")

        self._tree.tag_configure("draft", background="#FFF9C4")
        self._tree.tag_configure("finalized", background="#D5F5E3")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_grades(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        class_code = self._class_var.get()
        if not class_code:
            return

        from models.grade import Grade
        from models.student import Student
        grades = Grade.find_by_class(class_code)
        for g in grades:
            student = Student.find_by_id(g.studentID)
            name = student.fullName if student else g.studentID
            tag = "finalized" if g.status == "Finalized" else "draft"
            self._tree.insert("", "end", values=(
                g.studentID, name, g.midtermGrade, g.assignmentGrade,
                g.attendanceGrade, g.finalExamGrade,
                g.finalSummaryGrade, g.letterGrade, g.status
            ), tags=(tag,))

    def _finalize(self):
        class_code = self._class_var.get()
        if not class_code:
            messagebox.showwarning("Warning", "Please select a class.")
            return

        if not messagebox.askyesno("Confirm Finalization",
                                    f"Finalize grades for class '{class_code}'?\n\n"
                                    "WARNING: This action is PERMANENT.\n"
                                    "Grades cannot be altered after finalization."):
            return

        from models.admin import Admin
        admin = Admin(self._account.username)
        success, msg = admin.finalizeGrades(class_code)
        if success:
            self._load_grades()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

