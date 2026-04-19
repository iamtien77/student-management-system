"""
Màn hình quên mật khẩu - UC3
Bước 1: Nhập Email hoặc Số điện thoại để xác minh danh tính
Bước 2: Đặt mật khẩu mới trực tiếp
"""
import tkinter as tk
from views.base_view import BaseView, COLORS, FONTS


class ForgotPasswordView(BaseView):
    def __init__(self, root, on_back_to_login):
        super().__init__(root)
        self._on_back = on_back_to_login
        self._found_username = None

    def show(self):
        self.clear_window()
        self.root.title("Forgot Password")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(420, 480)
        self.root.resizable(False, False)
        self._build_step1()

    def _build_step1(self):
        """Bước 1: Nhập Email/Số điện thoại để xác minh."""
        card = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=420)

        tk.Label(card, text="Forgot Password?", font=FONTS["title"],
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(30, 5))
        tk.Label(card, text="Enter your registered Email or Phone",
                 font=FONTS["small"], fg=COLORS["text_light"],
                 bg=COLORS["card"]).pack(pady=(0, 15))

        # Ảnh đại diện
        canvas = tk.Canvas(card, width=80, height=80, bg=COLORS["card"],
                           highlightthickness=0)
        canvas.pack(pady=(0, 15))
        self.draw_avatar(canvas, 40, 40, 35, COLORS["primary"])

        # Ô nhập định danh
        self._id_frame = self.create_rounded_entry(card, "Email or Phone Number")
        self._id_frame.pack(padx=40, fill="x", pady=10)

        # Khu vực thông báo
        self._msg_frame = tk.Frame(card, bg=COLORS["card"], height=30)
        self._msg_frame.pack(fill="x", padx=40)

        # Nút xác minh
        btn = tk.Button(card, text="Verify", font=FONTS["button"],
                        bg=COLORS["primary"], fg=COLORS["text_white"],
                        activebackground=COLORS["primary_dark"],
                        bd=0, padx=20, pady=8, cursor="hand2",
                        command=self._verify)
        btn.pack(pady=10)

        # Liên kết quay lại
        back = tk.Label(card, text="< Back to Login", font=FONTS["small"],
                        fg=COLORS["primary"], bg=COLORS["card"], cursor="hand2")
        back.pack(pady=5)
        back.bind("<Button-1>", lambda e: self._on_back())

    def _verify(self):
        for w in self._msg_frame.winfo_children():
            w.destroy()
        identifier = self.get_entry_value(self._id_frame)
        if not identifier:
            self.show_message(self._msg_frame, "Please enter Email or Phone.", "error")
            return

        from models.account import Account
        success, result = Account.forgotPassword(identifier)
        if success:
            self._found_username = result
            self.clear_window()
            self._build_step2()
        else:
            self.show_message(self._msg_frame, result, "error")

    def _build_step2(self):
        """Bước 2: Đặt mật khẩu mới."""
        card = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=420)

        tk.Label(card, text="Reset Password", font=FONTS["title"],
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(30, 5))
        tk.Label(card, text=f"Account: {self._found_username}",
                 font=FONTS["body"], fg=COLORS["text_dark"],
                 bg=COLORS["card"]).pack(pady=(0, 20))

        # Mật khẩu mới
        self._new_pwd = self.create_rounded_entry(card, "New Password", show="*")
        self._new_pwd.pack(padx=40, fill="x", pady=8)

        # Xác nhận mật khẩu
        self._confirm_pwd = self.create_rounded_entry(card, "Confirm Password", show="*")
        self._confirm_pwd.pack(padx=40, fill="x", pady=8)

        # Khu vực thông báo
        self._msg_frame2 = tk.Frame(card, bg=COLORS["card"], height=30)
        self._msg_frame2.pack(fill="x", padx=40)

        # Nút đặt lại mật khẩu
        btn = tk.Button(card, text="Reset Password", font=FONTS["button"],
                        bg=COLORS["primary"], fg=COLORS["text_white"],
                        activebackground=COLORS["primary_dark"],
                        bd=0, padx=20, pady=8, cursor="hand2",
                        command=self._reset)
        btn.pack(pady=15)

    def _reset(self):
        for w in self._msg_frame2.winfo_children():
            w.destroy()
        new_pwd = self.get_entry_value(self._new_pwd)
        confirm = self.get_entry_value(self._confirm_pwd)

        if not new_pwd or not confirm:
            self.show_message(self._msg_frame2, "Please fill both fields.", "error")
            return
        if new_pwd != confirm:
            self.show_message(self._msg_frame2, "Passwords do not match.", "error")
            return

        from models.account import Account
        account = Account.find_by_username(self._found_username)
        if account:
            success, msg = account.resetPassword(new_pwd)
            if success:
                self.show_message(self._msg_frame2, msg, "success")
                self.root.after(2000, self._on_back)
            else:
                self.show_message(self._msg_frame2, msg, "error")

