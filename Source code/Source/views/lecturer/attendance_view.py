"""
Màn hình điểm danh - UC16
Giảng viên chọn lớp â†’ đánh dấu điểm danh sinh viên theo từng buổi học.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from views.base_view import BaseView, COLORS, FONTS


class AttendanceView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Take Attendance")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1000, 650)
        self._build_ui()

    def _build_ui(self):
        # Thanh điều hướng
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="Take Attendance", font=FONTS["nav"], fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Chọn lớp học phần
        from models.lecturer import Lecturer
        lecturer = Lecturer.find_by_id(self._account.username)
        classes = lecturer.get_assigned_classes() if lecturer else []

        select_frame = tk.Frame(self.root, bg=COLORS["bg"])
        select_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(select_frame, text="Select Class:", font=FONTS["body_bold"],
                 bg=COLORS["bg"], fg=COLORS["text_dark"]).pack(side="left")

        class_codes = [cs.classCode for cs in classes]
        self._class_var = tk.StringVar()
        combo = ttk.Combobox(select_frame, textvariable=self._class_var,
                              values=class_codes, state="readonly", font=FONTS["body"])
        combo.pack(side="left", padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: self._load_students())

        tk.Label(select_frame, text="Date:", font=FONTS["body_bold"],
                 bg=COLORS["bg"], fg=COLORS["text_dark"]).pack(side="left", padx=(20, 5))
        self._date_entry = tk.Entry(select_frame, font=FONTS["body"], width=12)
        self._date_entry.insert(0, datetime.date.today().strftime("%d/%m/%Y"))
        self._date_entry.pack(side="left")

        tk.Button(select_frame, text="Load", font=FONTS["body_bold"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=15, pady=3,
                  cursor="hand2", command=self._load_students).pack(side="left", padx=10)

        # Bảng điểm danh sinh viên
        self._table_frame = tk.Frame(self.root, bg=COLORS["card"])
        self._table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Nút lưu
        tk.Button(self.root, text="Save Attendance", font=FONTS["button"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=25, pady=8,
                  cursor="hand2", command=self._save).pack(pady=(0, 15))

        self._attendance_vars = {}

    def _load_students(self):
        for w in self._table_frame.winfo_children():
            w.destroy()
        self._attendance_vars.clear()

        class_code = self._class_var.get()
        if not class_code:
            return

        # Lấy toàn bộ sinh viên (thực tế nên lấy sinh viên đã đăng ký lớp)
        from models.grade import Grade
        grades = Grade.find_by_class(class_code)
        student_ids = list(set(g.studentID for g in grades))

        if not student_ids:
            # Nếu chưa có điểm, thử lấy toàn bộ sinh viên
            from models.student import Student
            all_students = Student.get_all()
            student_ids = [s.studentID for s in all_students]

        # Tải dữ liệu điểm danh sẵn có cho ngày này
        session_date = self._date_entry.get().strip()
        from models.attendance import Attendance
        existing = Attendance.get_class_session(class_code, session_date)
        existing_map = {a.studentID: a.attendanceStatus for a in existing}

        # Phần đầuer
        header = tk.Frame(self._table_frame, bg=COLORS["primary"])
        header.pack(fill="x")
        tk.Label(header, text="Student ID", font=FONTS["body_bold"], fg="white",
                 bg=COLORS["primary"], width=20, anchor="w").pack(side="left", padx=10, pady=5)
        tk.Label(header, text="Name", font=FONTS["body_bold"], fg="white",
                 bg=COLORS["primary"], width=25, anchor="w").pack(side="left", padx=5)
        tk.Label(header, text="Status", font=FONTS["body_bold"], fg="white",
                 bg=COLORS["primary"], width=15).pack(side="left", padx=5)
        tk.Label(header, text="Rate", font=FONTS["body_bold"], fg="white",
                 bg=COLORS["primary"], width=10).pack(side="left", padx=5)

        # Danh sách sinh viên có thể cuộn
        canvas = tk.Canvas(self._table_frame, bg=COLORS["card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self._table_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["card"])
        scroll_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        from models.student import Student
        for i, sid in enumerate(student_ids):
            student = Student.find_by_id(sid)
            name = student.fullName if student else sid
            bg = "#F5F7FA" if i % 2 else COLORS["card"]

            row = tk.Frame(scroll_frame, bg=bg)
            row.pack(fill="x")

            tk.Label(row, text=sid, font=FONTS["body"], bg=bg,
                     width=20, anchor="w").pack(side="left", padx=10, pady=3)
            tk.Label(row, text=name, font=FONTS["body"], bg=bg,
                     width=25, anchor="w").pack(side="left", padx=5)

            var = tk.StringVar(value=existing_map.get(sid, "Present"))
            self._attendance_vars[sid] = var

            status_frame = tk.Frame(row, bg=bg)
            status_frame.pack(side="left", padx=5)
            tk.Radiobutton(status_frame, text="Present", variable=var, value="Present",
                           font=FONTS["small"], bg=bg).pack(side="left")
            tk.Radiobutton(status_frame, text="Absent", variable=var, value="Absent",
                           font=FONTS["small"], bg=bg).pack(side="left")

            # Tỷ lệ điểm danh
            rate = Attendance(class_code, sid, "", "").calculateAttendanceRate()
            tk.Label(row, text=f"{rate}%", font=FONTS["body"], bg=bg,
                     width=10).pack(side="left", padx=5)

    def _save(self):
        class_code = self._class_var.get()
        session_date = self._date_entry.get().strip()
        if not class_code or not session_date:
            messagebox.showwarning("Warning", "Select a class and date first.")
            return

        from models.attendance import Attendance
        for sid, var in self._attendance_vars.items():
            att = Attendance(class_code, sid, session_date, var.get())
            att.markAttendance(var.get())

        messagebox.showinfo("Success", "Attendance saved successfully.")

