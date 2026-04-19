"""
Màn hình tạo tài khoản - UC1
Quản trị viên tạo tài khoản cho sinh viên/giảng viên.
Hệ thống tự sinh tên đăng nhập (= ID) và mật khẩu ngẫu nhiên.
"""
import tkinter as tk
from tkinter import messagebox
from views.base_view import BaseView, COLORS, FONTS


class CreateAccountView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Create Account")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(550, 700)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Thanh điều hướng
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)
        tk.Button(navbar, text="< Back", font=FONTS["body"], fg="white",
                  bg=COLORS["navbar_bg"], bd=0, cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left", padx=15)
        tk.Label(navbar, text="Create Account", font=FONTS["nav"], fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Khung biểu mẫu
        card = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=15)

        # Chọn vai trò
        role_frame = tk.Frame(card, bg=COLORS["card"])
        role_frame.pack(fill="x", padx=30, pady=(15, 5))
        tk.Label(role_frame, text="Account Type:", font=FONTS["body_bold"],
                 fg=COLORS["text_dark"], bg=COLORS["card"]).pack(side="left")
        self._role_var = tk.StringVar(value="Student")
        for role in ["Student", "Lecturer"]:
            tk.Radiobutton(role_frame, text=role, variable=self._role_var,
                           value=role, font=FONTS["body"], bg=COLORS["card"],
                           activebackground=COLORS["card"],
                           command=self._toggle_fields).pack(side="left", padx=10)

        # Các trường nhập liệu
        fields = [
            ("ID (Student ID / Employee ID)", "user_id"),
            ("National ID (CCCD)", "cccd"),
            ("Full Name", "full_name"),
            ("Date of Birth (DD/MM/YYYY)", "dob"),
            ("Email", "email"),
            ("Gender", "gender"),
            ("Phone Number", "phone"),
            ("Faculty Code", "faculty"),
            ("Program ID (Student only)", "program_id"),
            ("Status (Student only)", "status"),
        ]

        self._entries = {}
        form = tk.Frame(card, bg=COLORS["card"])
        form.pack(fill="both", expand=True, padx=30)

        for label_text, key in fields:
            tk.Label(form, text=label_text + ":", font=FONTS["small"],
                     fg=COLORS["text_dark"], bg=COLORS["card"],
                     anchor="w").pack(fill="x", pady=(6, 1))
            entry = tk.Entry(form, font=FONTS["input"], bd=1, relief="solid",
                             highlightcolor=COLORS["primary"])
            entry.pack(fill="x", ipady=3)
            self._entries[key] = entry

        # Trạng thái mặc định
        self._entries["status"].insert(0, "Active")
        self._toggle_fields()

        # Khu vực thông báo
        self._msg_frame = tk.Frame(card, bg=COLORS["card"])
        self._msg_frame.pack(fill="x", padx=30)

        # Nút tạo mới
        tk.Button(card, text="Create Account", font=FONTS["button"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=25, pady=8,
                  cursor="hand2", command=self._create).pack(pady=15)

    def _toggle_fields(self):
        is_student = self._role_var.get() == "Student"
        state = "normal" if is_student else "disabled"
        self._entries["program_id"].config(state=state)
        self._entries["status"].config(state=state)

    def _create(self):
        for w in self._msg_frame.winfo_children():
            w.destroy()

        from models.admin import Admin
        admin = Admin(self._account.username)

        role = self._role_var.get()
        success, msg, password = admin.createAccount(
            userID=self._entries["user_id"].get().strip(),
            cccd=self._entries["cccd"].get().strip(),
            fullName=self._entries["full_name"].get().strip(),
            dob=self._entries["dob"].get().strip(),
            email=self._entries["email"].get().strip(),
            gender=self._entries["gender"].get().strip(),
            phone=self._entries["phone"].get().strip(),
            facultyCode=self._entries["faculty"].get().strip(),
            role=role,
            programID=self._entries["program_id"].get().strip() if role == "Student" else "",
            status=self._entries["status"].get().strip() if role == "Student" else "",
        )

        if success:
            messagebox.showinfo("Account Created",
                                f"{msg}\n\nGenerated Password: {password}\n\n"
                                f"Please deliver this password to the user manually.")
            # Xóa trắng biểu mẫu
            for entry in self._entries.values():
                try:
                    entry.delete(0, "end")
                except tk.TclError:
                    pass
            self._entries["status"].insert(0, "Active")
        else:
            self.show_message(self._msg_frame, msg, "error")

