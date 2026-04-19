"""
Giao diện điều khiển Admin - Theo nguyên mẫu mockup:
- Thanh điều hướng trên cùng với "Admin Dashboard" + menu thả xuống "Welcome, Admin"
- Trái: Thẻ hồ sơ + Hoạt động gần đây
- Phải: Lưới thẻ chức năng 3x3 với các biểu tượng
- Dưới cùng: Phần thông báo
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView, COLORS, FONTS, DASHBOARD_SIZE


class AdminDashboard(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to  # hàm điều hướng(view_name)

    def show(self):
        self.clear_window()
        self.root.title("SMS - Admin Dashboard")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1100, 700)
        self.root.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        # ---- THANH ĐIỀU HƯỚNG ----
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(navbar, text="☰", font=("Segoe UI", 18), fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=15)
        tk.Label(navbar, text="Admin Dashboard", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left")

        # Cột phải - thông tin người dùng
        user_frame = tk.Frame(navbar, bg=COLORS["navbar_bg"])
        user_frame.pack(side="right", padx=15)

        user_btn = tk.Menubutton(user_frame, text=f"Welcome, {self._account.username}  ▼",
                                  font=FONTS["body"], fg="white",
                                  bg=COLORS["navbar_bg"], activebackground=COLORS["primary_dark"],
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

        # Cột trái - Hồ sơ
        left = tk.Frame(main, bg=COLORS["bg"], width=220)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        self._build_profile_card(left)
        self._build_activity_card(left)

        # Cột phải - Lưới chức năng + Thông báo
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)
        self._build_function_grid(right)
        self._build_notification(right)

    def _build_profile_card(self, parent):
        card = tk.Frame(parent, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(fill="x", pady=(0, 10))

        # Khung ảnh đại diện trống
        avatar_frame = tk.Frame(card, bg=COLORS["card"])
        avatar_frame.pack(pady=(15, 5))
        canvas = tk.Canvas(avatar_frame, width=80, height=80,
                           bg=COLORS["card"], highlightthickness=0)
        canvas.pack()
        self.draw_avatar(canvas, 40, 40, 35, COLORS["primary"])

        tk.Label(card, text="Admin", font=FONTS["body_bold"],
                 fg=COLORS["text_dark"], bg=COLORS["card"]).pack()
        tk.Label(card, text=f"Admin ID: {self._account.username}",
                 font=FONTS["small"], fg=COLORS["text_light"],
                 bg=COLORS["card"]).pack(pady=(0, 15))

    def _build_activity_card(self, parent):
        card = tk.Frame(parent, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.pack(fill="x")

        tk.Label(card, text="Recent Activity", font=FONTS["body_bold"],
                 fg=COLORS["text_dark"], bg=COLORS["card"],
                 anchor="w").pack(fill="x", padx=10, pady=(10, 5))

        # Các hoạt động mẫu
        activities = [
            "● System started.",
            "● Admin logged in.",
        ]
        for act in activities:
            tk.Label(card, text=act, font=FONTS["small"],
                     fg=COLORS["text_light"], bg=COLORS["card"],
                     anchor="w", wraplength=190).pack(fill="x", padx=15, pady=2)
        tk.Frame(card, height=10, bg=COLORS["card"]).pack()

    def _build_function_grid(self, parent):
        grid_frame = tk.Frame(parent, bg=COLORS["bg"])
        grid_frame.pack(fill="both", expand=True)

        # Định nghĩa các thẻ chức năng: (biểu tượng, tiêu đề, tên_giao_diện)
        functions = [
            ("👤+", "Create\nAccount", "create_account"),
            ("🎓", "Manage\nStudent Profile", "manage_student"),
            ("📓", "Manage\nLecturer Profile", "manage_lecturer"),
            ("👥", "Manage\nFaculty", "manage_faculty"),
            ("📅", "Manage\nSemester", "manage_semester"),
            ("📋", "Manage\nCourse", "manage_course"),
            ("🏫", "Manage\nClass", "manage_class"),
            ("🔄", "Assign\nLecturer", "assign_lecturer"),
            ("📌", "Finalize\nGrades", "finalize_grades"),
        ]

        for i, (icon, title, view_name) in enumerate(functions):
            row, col = divmod(i, 3)
            card = tk.Frame(grid_frame, bg=COLORS["card"], cursor="hand2",
                            highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(card, text=icon, font=("Segoe UI", 26),
                     bg=COLORS["card"], fg=COLORS["primary"]).pack(pady=(12, 2))
            tk.Label(card, text=title, font=FONTS["card_title"],
                     bg=COLORS["card"], fg=COLORS["text_dark"],
                     justify="center").pack(pady=(0, 12))

            # Xử lý sự kiện nhấp chuột
            card.bind("<Button-1>", lambda e, v=view_name: self._navigate(v))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, v=view_name: self._navigate(v))

            # Hiệu ứng di chuột
            def on_enter(e, c=card):
                c.config(highlightbackground=COLORS["primary"], highlightthickness=2)
            def on_leave(e, c=card):
                c.config(highlightbackground=COLORS["card_border"], highlightthickness=1)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

        for c in range(3):
            grid_frame.columnconfigure(c, weight=1)
        for r in range(3):
            grid_frame.rowconfigure(r, weight=1)

    def _build_notification(self, parent):
        notif = tk.Frame(parent, bg=COLORS["card"],
                         highlightbackground=COLORS["card_border"], highlightthickness=1)
        notif.pack(fill="x", pady=(10, 0))

        tk.Label(notif, text="Notification", font=FONTS["body_bold"],
                 fg=COLORS["text_dark"], bg=COLORS["card"],
                 anchor="w").pack(fill="x", padx=15, pady=(8, 5))

        tk.Label(notif, text="•   System: Welcome to Student Management System.",
                 font=FONTS["small"], fg=COLORS["text_dark"],
                 bg=COLORS["card"], anchor="w").pack(fill="x", padx=20, pady=(0, 8))
