"""
Màn hình nhập điểm - UC17
Giảng viên nhập điểm thành phần + điểm thi cuối kỳ, lưu ở trạng thái Nháp.
Hệ thống tự tính điểm tổng kết và điểm chữ.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView, COLORS, FONTS


class EnterGradesView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Enter Grades")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1100, 700)
        self._build_ui()

    def _build_ui(self):
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="Enter Grades", font=FONTS["nav"], fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Chọn lớp học phần
        from models.lecturer import Lecturer
        lecturer = Lecturer.find_by_id(self._account.username)
        classes = lecturer.get_assigned_classes() if lecturer else []

        select = tk.Frame(self.root, bg=COLORS["bg"])
        select.pack(fill="x", padx=20, pady=10)

        tk.Label(select, text="Select Class:", font=FONTS["body_bold"],
                 bg=COLORS["bg"]).pack(side="left")
        class_codes = [cs.classCode for cs in classes]
        self._class_var = tk.StringVar()
        combo = ttk.Combobox(select, textvariable=self._class_var,
                              values=class_codes, state="readonly", font=FONTS["body"])
        combo.pack(side="left", padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: self._load_grades())

        # Bảng điểm
        table_frame = tk.Frame(self.root, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 5))

        columns = ("student_id", "name", "midterm", "assignment",
                   "attendance", "final_exam", "summary", "letter", "status")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

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

        # Biểu mẫu chỉnh sửa
        form = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        form.pack(fill="x", padx=20, pady=5)

        tk.Label(form, text="Student ID:", font=FONTS["body"], bg=COLORS["card"]).grid(
            row=0, column=0, padx=5, pady=5, sticky="e")
        self._sid_entry = tk.Entry(form, font=FONTS["body"], width=15)
        self._sid_entry.grid(row=0, column=1, padx=5, pady=5)

        fields = [("Midterm:", "_mid_entry"), ("Assignment:", "_asn_entry"),
                  ("Attendance:", "_att_entry"), ("Final Exam:", "_fin_entry")]
        for i, (label, attr) in enumerate(fields):
            tk.Label(form, text=label, font=FONTS["body"], bg=COLORS["card"]).grid(
                row=0, column=2 + i * 2, padx=5, pady=5, sticky="e")
            entry = tk.Entry(form, font=FONTS["body"], width=8)
            entry.grid(row=0, column=3 + i * 2, padx=5, pady=5)
            setattr(self, attr, entry)

        tk.Button(form, text="Save Grade", font=FONTS["body_bold"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=15, pady=4,
                  cursor="hand2", command=self._save_grade).grid(
            row=0, column=10, padx=10, pady=5)

        # Tự điền từ dòng được chọn trong bảng
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

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

    def _on_select(self, event):
        sel = self._tree.selection()
        if not sel:
            return
        vals = self._tree.item(sel[0], "values")
        self._sid_entry.delete(0, "end")
        self._sid_entry.insert(0, vals[0])
        self._mid_entry.delete(0, "end")
        self._mid_entry.insert(0, vals[2])
        self._asn_entry.delete(0, "end")
        self._asn_entry.insert(0, vals[3])
        self._att_entry.delete(0, "end")
        self._att_entry.insert(0, vals[4])
        self._fin_entry.delete(0, "end")
        self._fin_entry.insert(0, vals[5])

    def _save_grade(self):
        class_code = self._class_var.get()
        sid = self._sid_entry.get().strip()
        if not class_code or not sid:
            messagebox.showwarning("Warning", "Select a class and enter Student ID.")
            return

        try:
            mid = float(self._mid_entry.get() or 0)
            asn = float(self._asn_entry.get() or 0)
            att = float(self._att_entry.get() or 0)
            fin = float(self._fin_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Grades must be numbers (0-10).")
            return

        for val in [mid, asn, att, fin]:
            if val < 0 or val > 10:
                messagebox.showerror("Error", "Grades must be between 0 and 10.")
                return

        from models.lecturer import Lecturer
        lecturer = Lecturer.find_by_id(self._account.username)
        if lecturer:
            success, msg = lecturer.inputComponentGrades(class_code, sid, mid, asn, att)
            if success and fin > 0:
                success2, msg2 = lecturer.inputFinalExamGrade(class_code, sid, fin)
                if not success2:
                    messagebox.showerror("Error", msg2)
                    return
            if success:
                self._load_grades()
                messagebox.showinfo("Success", "Grade saved as Draft.")
            else:
                messagebox.showerror("Error", msg)

