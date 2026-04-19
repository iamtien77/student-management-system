"""
Màn hình phân công giảng viên - UC10
Quản trị viên chọn lớp học phần và phân công giảng viên phụ trách.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView, COLORS, FONTS


class AssignLecturerView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Assign Lecturer")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(900, 600)
        self._build_ui()

    def _build_ui(self):
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="Assign Lecturer to Class", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        content = tk.Frame(self.root, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Bảng lớp học phần
        tk.Label(content, text="Class Sections", font=FONTS["heading"],
                 bg=COLORS["bg"], fg=COLORS["primary"]).pack(anchor="w")

        table_frame = tk.Frame(content, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True, pady=(5, 10))

        columns = ("classCode", "courseCode", "semester", "capacity",
                   "day", "time", "lecturerID")
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        for col, heading, w in [
            ("classCode", "Class Code", 100), ("courseCode", "Course", 100),
            ("semester", "Semester", 100), ("capacity", "Capacity", 80),
            ("day", "Day", 80), ("time", "Time", 120), ("lecturerID", "Lecturer", 120)
        ]:
            self._tree.heading(col, text=heading)
            self._tree.column(col, width=w)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._load_classes()

        # Biểu mẫu phân công
        form = tk.Frame(content, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        form.pack(fill="x", pady=5)

        tk.Label(form, text="Assign Lecturer:", font=FONTS["body_bold"],
                 bg=COLORS["card"], fg=COLORS["primary"]).pack(side="left", padx=15, pady=10)

        tk.Label(form, text="Class Code:", font=FONTS["body"],
                 bg=COLORS["card"]).pack(side="left", padx=5)
        self._class_entry = tk.Entry(form, font=FONTS["body"], width=12)
        self._class_entry.pack(side="left", padx=5)

        tk.Label(form, text="Lecturer ID:", font=FONTS["body"],
                 bg=COLORS["card"]).pack(side="left", padx=5)

        from models.lecturer import Lecturer
        lecturers = Lecturer.get_all()
        lec_ids = [l.employeeID for l in lecturers]
        self._lec_var = tk.StringVar()
        combo = ttk.Combobox(form, textvariable=self._lec_var,
                              values=lec_ids, font=FONTS["body"], width=15)
        combo.pack(side="left", padx=5)

        tk.Button(form, text="Assign", font=FONTS["body_bold"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=15, pady=5,
                  cursor="hand2", command=self._assign).pack(side="left", padx=15)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_classes(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        from models.class_section import ClassSection
        for cs in ClassSection.get_all():
            self._tree.insert("", "end", values=(
                cs.classCode, cs.courseCode, cs.semesterCode,
                f"{cs.currentEnrollment}/{cs.maxCapacity}",
                cs.dayOfWeek, f"{cs.startTime}-{cs.endTime}", cs.lecturerID
            ))

    def _on_select(self, event):
        sel = self._tree.selection()
        if sel:
            vals = self._tree.item(sel[0], "values")
            self._class_entry.delete(0, "end")
            self._class_entry.insert(0, vals[0])

    def _assign(self):
        class_code = self._class_entry.get().strip()
        lec_id = self._lec_var.get().strip()
        if not class_code or not lec_id:
            messagebox.showwarning("Warning", "Select both class and lecturer.")
            return

        from models.admin import Admin
        admin = Admin(self._account.username)
        success, msg = admin.assignLecturer(lec_id, class_code)
        if success:
            self._load_classes()
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)

