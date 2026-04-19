"""
views/base_view.py
lop co so cua toan bo tang view trong he thong
dinh nghia:
  - COLORS : bang mau sac nhat quan toan he thong
  - FONTS  : bang phong chu nhat quan toan he thong
  - BaseView: cung cap clear_window, cac ham tao widget chuan va hien thi thong bao
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# BANG MAU SAC HE THONG
# ---------------------------------------------------------------------------
COLORS = {
    "primary":        "#1e3a5f",   # sidebar / header nen toi
    "primary_dark":   "#162d4a",   # sidebar item active / hover
    "primary_light":  "#2a5298",   # header gradient phu
    "accent":         "#3498db",   # nut bam, vien highlight
    "accent_hover":   "#2980b9",   # nut bam khi hover
    "white":          "#ffffff",
    "bg":             "#f0f4f8",   # nen trang chinh
    "bg_card":        "#ffffff",   # nen the, bang
    "text_dark":      "#2c3e50",   # chu chinh
    "text_light":     "#ecf0f1",   # chu tren nen toi
    "text_muted":     "#7f8c8d",   # chu phu / ghi chu
    "success":        "#27ae60",   # thanh cong
    "error":          "#e74c3c",   # loi / xoa
    "warning":        "#f39c12",   # canh bao
    "border":         "#dee2e6",   # vien ngan cach
    "sidebar_item":   "#8da9c4",   # chu menu sidebar chua chon
    "row_even":       "#f8fafc",   # mau hang chan trong bang
    "row_odd":        "#ffffff",   # mau hang le trong bang
    "row_selected":   "#d0e8ff",   # mau hang dang duoc chon
    "tag_draft":      "#fff3cd",   # nen badge trang thai nhap
    "tag_finalized":  "#d4edda",   # nen badge trang thai da chot
}

# ---------------------------------------------------------------------------
# BANG PHONG CHU HE THONG
# ---------------------------------------------------------------------------
FONTS = {
    "default":      ("Helvetica", 10),
    "bold":         ("Helvetica", 10, "bold"),
    "title":        ("Helvetica", 16, "bold"),
    "header":       ("Helvetica", 13, "bold"),
    "small":        ("Helvetica", 9),
    "small_bold":   ("Helvetica", 9, "bold"),
    "button":       ("Helvetica", 10, "bold"),
    "sidebar_item": ("Helvetica", 11),
    "sidebar_logo": ("Helvetica", 14, "bold"),
    "table_header": ("Helvetica", 10, "bold"),
    "input":        ("Helvetica", 11),
}


class BaseView:
    """
    lop co so cua moi man hinh trong he thong
    tat ca cac view phai ke thua lop nay de dam bao tinh nhat quan giao dien

    quy tac su dung:
    - goi self.clear_window() dau tien trong phuong thuc show()
    - su dung self.COLORS va self.FONTS thay vi hard-code mau sac truc tiep
    - goi self.make_button(), self.make_label(), ... de tao widget chuan
    """

    def __init__(self, root: tk.Tk):
        self.root   = root
        self.COLORS = COLORS
        self.FONTS  = FONTS

    # -----------------------------------------------------------------------
    # XOA SACH CUA SO TRUOC KHI VE MAN HINH MOI
    # -----------------------------------------------------------------------

    def clear_window(self):
        """huy toan bo widget dang duoc render de chuan bi render man hinh moi"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # -----------------------------------------------------------------------
    # CAC HAM TIEN ICH THONG BAO
    # -----------------------------------------------------------------------

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_success(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def ask_confirm(self, title: str, message: str) -> bool:
        """hien hop thoai xac nhan Yes/No, tra ve True neu nguoi dung chon Yes"""
        return messagebox.askyesno(title, message)

    # -----------------------------------------------------------------------
    # TAO CAC WIDGET TIEU CHUAN
    # -----------------------------------------------------------------------

    def make_button(self, parent, text: str, command, style: str = "primary", **kwargs):
        """
        tao nut bam theo phong cach he thong co hieu ung hover
        style: "primary" | "danger" | "success" | "warning" | "outline"
        """
        style_map = {
            "primary": (COLORS["accent"],   COLORS["white"],    COLORS["accent_hover"]),
            "danger":  (COLORS["error"],    COLORS["white"],    "#c0392b"),
            "success": (COLORS["success"],  COLORS["white"],    "#229954"),
            "warning": (COLORS["warning"],  COLORS["white"],    "#e67e22"),
            "outline": (COLORS["white"],    COLORS["text_dark"], COLORS["border"]),
        }
        bg, fg, hover = style_map.get(style, style_map["primary"])
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg,
            font=FONTS["button"],
            relief="flat", cursor="hand2",
            padx=14, pady=7,
            activebackground=hover,
            activeforeground=fg,
            **kwargs
        )
        # hieu ung doi mau khi chuot di vao / ra khoi nut
        btn.bind("<Enter>", lambda e, b=bg, h=hover: btn.config(bg=h))
        btn.bind("<Leave>", lambda e, b=bg: btn.config(bg=b))
        return btn

    def make_label(self, parent, text: str, style: str = "default", **kwargs) -> tk.Label:
        """tao nhan voi phong chu va mau sac chuan"""
        font_map = {
            "default": FONTS["default"],
            "title":   FONTS["title"],
            "header":  FONTS["header"],
            "small":   FONTS["small"],
            "muted":   FONTS["small"],
        }
        fg_map = {
            "default": COLORS["text_dark"],
            "title":   COLORS["text_dark"],
            "header":  COLORS["text_dark"],
            "small":   COLORS["text_dark"],
            "muted":   COLORS["text_muted"],
        }
        return tk.Label(
            parent, text=text,
            font=font_map.get(style, FONTS["default"]),
            fg=fg_map.get(style, COLORS["text_dark"]),
            bg=kwargs.pop("bg", COLORS["bg"]),
            **kwargs
        )

    def make_entry(self, parent, **kwargs) -> tk.Entry:
        """tao o nhap lieu theo phong cach he thong"""
        return tk.Entry(
            parent,
            font=FONTS["input"],
            bg=COLORS["white"],
            fg=COLORS["text_dark"],
            relief="solid", bd=1,
            **kwargs
        )

    def make_combobox(self, parent, values: list, **kwargs) -> ttk.Combobox:
        """tao dropdown combobox co danh sach gia tri cho san"""
        cb = ttk.Combobox(parent, values=values, state="readonly",
                          font=FONTS["input"], **kwargs)
        return cb

    # -----------------------------------------------------------------------
    # CAI DAT PHONG CACH CHO TREEVIEW (BANG DU LIEU)
    # -----------------------------------------------------------------------

    def setup_treeview_style(self):
        """ap dung phong cach tuy chinh cho toan bo Treeview trong man hinh"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=COLORS["white"],
            foreground=COLORS["text_dark"],
            fieldbackground=COLORS["white"],
            rowheight=32,
            font=FONTS["default"],
            borderwidth=0,
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=COLORS["primary"],
            foreground=COLORS["white"],
            font=FONTS["table_header"],
            relief="flat",
        )
        # mau hang duoc chon
        style.map(
            "Custom.Treeview",
            background=[("selected", COLORS["row_selected"])],
            foreground=[("selected", COLORS["text_dark"])],
        )

    # -----------------------------------------------------------------------
    # PHUONG THUC SHOW PHAI DUOC OVERRIDE O LOP CON
    # -----------------------------------------------------------------------

    def show(self):
        raise NotImplementedError(
            f"Lop '{self.__class__.__name__}' chua implement phuong thuc show()"
        )
