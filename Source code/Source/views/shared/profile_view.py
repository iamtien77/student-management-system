"""
Màn hình hồ sơ - UC6 (Xem) + UC7 (Cập nhật)
Sinh viên: chỉ được sửa Email, Số điện thoại.
Giảng viên: chỉ được sửa Email, Số điện thoại (không sửa Khoa).
"""
import tkinter as tk
from tkinter import messagebox
from views.base_view import BaseView, COLORS, FONTS


class ProfileView(BaseView):
    def __init__(self, root, account, navigate_to, mode="view"):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to
        self._mode = mode  # "view" hoặc "update"

    def show(self):
        self.clear_window()
        title = "View Profile" if self._mode == "view" else "Update Profile"
        self.root.title(f"SMS - {title}")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(550, 600)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Tải hồ sơ cá nhân
        role = self._account.role
        profile = None
        if role == "Student":
            from models.student import Student
            profile = Student.find_by_id(self._account.username)
        elif role == "Lecturer":
            from models.lecturer import Lecturer
            profile = Lecturer.find_by_id(self._account.username)

        if not profile:
            messagebox.showerror("Error", "Profile not found.")
            self._navigate("dashboard")
            return

        # Thanh điều hướng
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        title = "View Profile" if self._mode == "view" else "Update Profile"
        tk.Label(navbar, text=title, font=FONTS["nav"], fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Khung thẻ
        card = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=15)

        # Ảnh đại diện
        canvas = tk.Canvas(card, width=80, height=80, bg=COLORS["card"],
                           highlightthickness=0)
        canvas.pack(pady=(15, 5))
        self.draw_avatar(canvas, 40, 40, 35, COLORS["primary"])

        tk.Label(card, text=profile.fullName, font=FONTS["heading"],
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(0, 15))

        # Các trường nhập liệu
        if role == "Student":
            fields = [
                ("Student ID", profile.studentID, False),
                ("National ID (CCCD)", profile.cccd, False),
                ("Full Name", profile.fullName, False),
                ("Date of Birth", profile.dob, False),
                ("Gender", profile.gender, False),
                ("Faculty", profile.facultyCode, False),
                ("Program", profile.programID, False),
                ("Status", profile.status, False),
                ("Email", profile.email, True),
                ("Phone Number", profile.phoneNumber, True),
            ]
        else:
            fields = [
                ("Employee ID", profile.employeeID, False),
                ("National ID (CCCD)", profile.cccd, False),
                ("Full Name", profile.fullName, False),
                ("Date of Birth", profile.dob, False),
                ("Gender", profile.gender, False),
                ("Faculty", profile.facultyCode, False),
                ("Email", profile.email, True),
                ("Phone Number", profile.phoneNumber, True),
            ]

        form = tk.Frame(card, bg=COLORS["card"])
        form.pack(fill="x", padx=40)

        self._entries = {}
        for label, value, editable in fields:
            row = tk.Frame(form, bg=COLORS["card"])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label + ":", font=FONTS["body_bold"],
                     fg=COLORS["text_dark"], bg=COLORS["card"],
                     width=18, anchor="w").pack(side="left")
            entry = tk.Entry(row, font=FONTS["body"], bd=1, relief="solid")
            entry.insert(0, value)
            if self._mode == "view" or not editable:
                entry.config(state="readonly", readonlybackground="#F0F0F0")
            entry.pack(side="left", fill="x", expand=True, ipady=2)
            if editable:
                self._entries[label] = entry

        # Thông báo và lưu
        self._msg_frame = tk.Frame(card, bg=COLORS["card"])
        self._msg_frame.pack(fill="x", padx=40)

        if self._mode == "update":
            tk.Button(card, text="Save Changes", font=FONTS["button"],
                      bg=COLORS["primary"], fg="white", bd=0, padx=25, pady=8,
                      cursor="hand2",
                      command=lambda: self._save(profile)).pack(pady=15)

    def _save(self, profile):
        for w in self._msg_frame.winfo_children():
            w.destroy()
        email = self._entries["Email"].get().strip()
        phone = self._entries["Phone Number"].get().strip()
        success, msg = profile.updatePersonalInfo(email=email, phoneNumber=phone)
        if success:
            messagebox.showinfo("Success", msg)
            self._navigate("dashboard")
        else:
            self.show_message(self._msg_frame, msg, "error")

