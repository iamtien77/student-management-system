"""
Giao diện điều khiển Sinh Viên:
- Thanh điều hướng trên cùng với "Student Dashboard" + menu thả xuống (Đổi Mật khẩu, Đăng xuất)
- Thẻ hồ sơ bên trái với thông tin sinh viên
- Các thẻ chức năng: Xem Hồ sơ, Cập nhật Hồ sơ, Xem Chương trình Đào tạo
- Phần thông báo ở dưới cùng
"""
import tkinter as tk
from views.base_view import BaseView, COLORS, FONTS


class StudentDashboard(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to
        self._student = None

    def show(self):
        self.clear_window()
        self.root.title("SMS - Student Dashboard")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1100, 700)
        self.root.resizable(True, True)

        from models.student import Student
        self._student = Student.find_by_id(self._account.username)
        self._build_ui()

    def _build_ui(self):
        # ---- THANH ĐIỀU HƯỚNG ----
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(navbar, text="☰", font=("Segoe UI", 18), fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=15)
        tk.Label(navbar, text="Student Dashboard", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left")

        user_frame = tk.Frame(navbar, bg=COLORS["navbar_bg"])
        user_frame.pack(side="right", padx=15)

        display_name = self._student.fullName if self._student else self._account.username
        user_btn = tk.Menubutton(user_frame,
                                  text=f"Welcome, {display_name}  ▼",
                                  font=FONTS["body"], fg="white",
                                  bg=COLORS["navbar_bg"],
                                  activebackground=COLORS["primary_dark"],
                                  bd=0, cursor="hand2")
        user_menu = tk.Menu(user_btn, tearoff=0, font=FONTS["small"])
        user_menu.add_command(label="🔑  Change Password",
                              command=lambda: self._navigate("change_password"))
        user_menu.add_separator()
        user_menu.add_command(label="🚪  Logout",
                              command=lambda: self._navigate("logout"))
        user_btn.config(menu=user_menu)
        user_btn.pack(side="right")

        # ---- NỘI DUNG CHÍNH ----
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Trái - Thẻ hồ sơ
        left = tk.Frame(main, bg=COLORS["bg"], width=250)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        self._build_profile_card(left)

        # Phải - Các thẻ chức năng
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)
        self._build_function_cards(right)
        self._build_notification(right)

    def _build_profile_card(self, parent):
        card = tk.Frame(parent, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(fill="x")

        canvas = tk.Canvas(card, width=80, height=80, bg=COLORS["card"],
                           highlightthickness=0)
        canvas.pack(pady=(15, 5))
        self.draw_avatar(canvas, 40, 40, 35, COLORS["primary"])

        if self._student:
            tk.Label(card, text=self._student.fullName, font=FONTS["body_bold"],
                     fg=COLORS["text_dark"], bg=COLORS["card"]).pack()
            info = [
                f"Student ID: {self._student.studentID}",
                f"Gender: {self._student.gender}",
                f"Day of Birth: {self._student.dob}",
                f"Email: {self._student.email}",
            ]
            for line in info:
                tk.Label(card, text=line, font=FONTS["small"],
                         fg=COLORS["text_light"], bg=COLORS["card"],
                         anchor="w").pack(fill="x", padx=15, pady=1)
        tk.Frame(card, height=15, bg=COLORS["card"]).pack()

    def _build_function_cards(self, parent):
        grid = tk.Frame(parent, bg=COLORS["bg"])
        grid.pack(fill="both", expand=True)

        functions = [
            ("🔭", "View Profile", "view_profile"),
            ("📝", "Update Profile", "update_profile"),
            ("📜", "View Training\nProgram", "training_program"),
            ("📊", "View Grades", "view_grades"),
        ]

        for i, (icon, title, view_name) in enumerate(functions):
            card = tk.Frame(grid, bg=COLORS["card"], cursor="hand2",
                            highlightbackground=COLORS["card_border"], highlightthickness=1)
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            tk.Label(card, text=icon, font=("Segoe UI", 30),
                     bg=COLORS["card"], fg=COLORS["primary"]).pack(pady=(20, 5))
            tk.Label(card, text=title, font=FONTS["card_title"],
                     bg=COLORS["card"], fg=COLORS["text_dark"],
                     justify="center").pack(pady=(0, 20))

            card.bind("<Button-1>", lambda e, v=view_name: self._navigate(v))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, v=view_name: self._navigate(v))

            def on_enter(e, c=card):
                c.config(highlightbackground=COLORS["primary"], highlightthickness=2)
            def on_leave(e, c=card):
                c.config(highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

        for c in range(2):
            grid.columnconfigure(c, weight=1)
        for r in range(2):
            grid.rowconfigure(r, weight=1)

    def _build_notification(self, parent):
        notif = tk.Frame(parent, bg=COLORS["card"],
                         highlightbackground=COLORS["card_border"], highlightthickness=1)
        notif.pack(fill="x", pady=(10, 0))

        tk.Label(notif, text="Notification", font=FONTS["body_bold"],
                 fg=COLORS["text_dark"], bg=COLORS["card"],
                 anchor="w").pack(fill="x", padx=15, pady=(8, 5))
        tk.Label(notif, text="•   Welcome to Student Management System.",
                 font=FONTS["small"], fg=COLORS["text_dark"],
                 bg=COLORS["card"], anchor="w").pack(fill="x", padx=20, pady=(0, 8))
