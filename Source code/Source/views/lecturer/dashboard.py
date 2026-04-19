"""
Giao diện điều khiển Giảng viên:
- Thanh điều hướng trên cùng với "Lecturer Dashboard" + menu thả xuống
- Thẻ hồ sơ bên trái
- Các thẻ chức năng: Xem Hồ sơ, Cập nhật Hồ sơ, Điểm danh, Nhập điểm
- Phần thông báo
"""
import tkinter as tk
from views.base_view import BaseView, COLORS, FONTS


class LecturerDashboard(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to
        self._lecturer = None

    def show(self):
        self.clear_window()
        self.root.title("SMS - Lecturer Dashboard")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1100, 700)
        self.root.resizable(True, True)

        from models.lecturer import Lecturer
        self._lecturer = Lecturer.find_by_id(self._account.username)
        self._build_ui()

    def _build_ui(self):
        # ---- THANH ĐIỀU HƯỚNG ----
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(navbar, text="☰", font=("Segoe UI", 18), fg="white",
                 bg=COLORS["navbar_bg"]).pack(side="left", padx=15)
        tk.Label(navbar, text="Lecturer Dashboard", font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left")

        user_frame = tk.Frame(navbar, bg=COLORS["navbar_bg"])
        user_frame.pack(side="right", padx=15)

        display_name = self._lecturer.fullName if self._lecturer else self._account.username
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

        left = tk.Frame(main, bg=COLORS["bg"], width=250)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        self._build_profile_card(left)

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

        if self._lecturer:
            tk.Label(card, text=self._lecturer.fullName, font=FONTS["body_bold"],
                     fg=COLORS["text_dark"], bg=COLORS["card"]).pack()
            info = [
                f"Employee ID: {self._lecturer.employeeID}",
                f"Gender: {self._lecturer.gender}",
                f"Faculty: {self._lecturer.facultyCode}",
                f"Email: {self._lecturer.email}",
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
            ("👥", "Take\nAttendance", "attendance"),
            ("💯", "Enter\nGrades", "enter_grades"),
        ]

        for i, (icon, title, view_name) in enumerate(functions):
            row, col = divmod(i, 2)
            card = tk.Frame(grid, bg=COLORS["card"], cursor="hand2",
                            highlightbackground=COLORS["card_border"], highlightthickness=1)
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
