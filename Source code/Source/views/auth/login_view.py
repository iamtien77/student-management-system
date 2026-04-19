"""
Màn hình đăng nhập - khớp với thiết kế mẫu:
- Thẻ nền trắng căn giữa màn hình
- Tiêu đề "Welcome Back!" / "Hello Lecturer!" / "Nice day, Admin!"
- Biểu tượng avatar hình tròn
- Ô nhập liệu nền xanh navy
- Liên kết "Forgot Password?"
- Các tab Student | Lecturer | Admin ở phía dưới
"""
import tkinter as tk
from views.base_view import BaseView, COLORS, FONTS, LOGIN_SIZE


class LoginView(BaseView):
    def __init__(self, root, on_login_success, on_forgot_password):
        super().__init__(root)
        self._on_login_success = on_login_success
        self._on_forgot_password = on_forgot_password
        self._current_tab = "Student"  # Tab mặc định
        self._msg_label = None

    def show(self):
        self.clear_window()
        self.root.title("Student Management System - Login")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(420, 520)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        # Khung thẻ chính
        card = tk.Frame(self.root, bg=COLORS["card"], bd=0,
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=480)

        # Tiêu đề - thay đổi theo tab được chọn
        greetings = {
            "Student": "Welcome Back!",
            "Lecturer": "Hello Lecturer!",
            "Admin": "Nice day, Admin!"
        }
        self._title_label = tk.Label(card, text=greetings[self._current_tab],
                                      font=FONTS["title"], fg=COLORS["primary"],
                                      bg=COLORS["card"])
        self._title_label.pack(pady=(25, 0))

        # Tiêu đề phụ
        tk.Label(card, text="Please sign in to your account",
                 font=FONTS["small"], fg=COLORS["text_light"],
                 bg=COLORS["card"]).pack(pady=(0, 10))

        # Ảnh đại diện circle
        avatar_canvas = tk.Canvas(card, width=100, height=100,
                                   bg=COLORS["card"], highlightthickness=0)
        avatar_canvas.pack(pady=(5, 15))
        self.draw_avatar(avatar_canvas, 50, 50, 45, COLORS["primary"])

        # Ô tên đăng nhập
        self._username_frame = self.create_rounded_entry(card, "Enter Username")
        self._username_frame.pack(padx=40, pady=(5, 8), fill="x")

        # Ô mật khẩu
        self._password_frame = self.create_rounded_entry(card, "Enter Password", show="*")
        self._password_frame.pack(padx=40, pady=(0, 5), fill="x")

        # Liên kết quên mật khẩu
        forgot_frame = tk.Frame(card, bg=COLORS["card"])
        forgot_frame.pack(padx=40, fill="x")
        forgot_btn = tk.Label(forgot_frame, text="Forgot Password?",
                               font=FONTS["small"], fg=COLORS["primary"],
                               bg=COLORS["card"], cursor="hand2")
        forgot_btn.pack(side="right")
        forgot_btn.bind("<Button-1>", lambda e: self._on_forgot_password())
        forgot_btn.bind("<Enter>", lambda e: forgot_btn.config(
            font=("Segoe UI", 9, "underline")))
        forgot_btn.bind("<Leave>", lambda e: forgot_btn.config(font=FONTS["small"]))

        # Khu vực thông báo
        self._msg_frame = tk.Frame(card, bg=COLORS["card"], height=25)
        self._msg_frame.pack(fill="x", padx=40)

        # Nút đăng nhập
        login_btn = tk.Button(card, text="Login", font=FONTS["button"],
                              bg=COLORS["primary"], fg=COLORS["text_white"],
                              activebackground=COLORS["primary_dark"],
                              bd=0, padx=20, pady=8, cursor="hand2",
                              command=self._do_login)
        login_btn.pack(pady=(5, 10))

        # Phím nhấn xuống dòng sẽ kích hoạt đăng nhập
        self._password_frame.entry.bind("<Return>", lambda e=None: self._do_login())
        self._username_frame.entry.bind("<Return>", lambda e=None: self._do_login())

        # Các tab vai trò ở phía dưới
        tab_frame = tk.Frame(card, bg=COLORS["card"])
        tab_frame.pack(side="bottom", pady=(0, 20))

        tabs = ["Student", "Lecturer", "Admin"]
        self._tab_labels = {}
        for i, tab in enumerate(tabs):
            if i > 0:
                tk.Label(tab_frame, text=" | ", font=FONTS["tab"],
                         fg=COLORS["text_light"], bg=COLORS["card"]).pack(side="left")

            lbl = tk.Label(tab_frame, text=tab, font=FONTS["tab"],
                           bg=COLORS["card"], cursor="hand2")
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e=None, t=tab: self._switch_tab(t))
            self._tab_labels[tab] = lbl

        self._update_tabs()

    def _switch_tab(self, tab):
        self._current_tab = tab
        self._update_tabs()

        greetings = {
            "Student": "Welcome Back!",
            "Lecturer": "Hello Lecturer!",
            "Admin": "Nice day, Admin!"
        }
        self._title_label.config(text=greetings[tab])

    def _update_tabs(self):
        for name, lbl in self._tab_labels.items():
            if name == self._current_tab:
                lbl.config(fg=COLORS["tab_active"],
                           font=("Segoe UI", 11, "bold underline"))
            else:
                lbl.config(fg=COLORS["tab_inactive"], font=FONTS["tab"])

    def _do_login(self):
        # Xóa thông báo trước đó
        for w in self._msg_frame.winfo_children():
            w.destroy()

        username = self.get_entry_value(self._username_frame)
        password = self.get_entry_value(self._password_frame)

        if not username or not password:
            self.show_message(self._msg_frame, "Please enter both fields.", "error")
            return

        from models.account import Account
        success, result = Account.login(username, password)

        if success:
            account = result
            self._on_login_success(account)
        else:
            self.show_message(self._msg_frame, result, "error")

