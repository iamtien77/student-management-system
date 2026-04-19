"""
Lớp giao diện cơ sở - hằng số giao diện và cấu hình dùng chung.
Bảng màu được thiết kế khớp với giao diện mẫu (tông xanh navy).
"""
import tkinter as tk
from tkinter import ttk, font as tkfont

# ---- Bảng màu (khớp giao diện mẫu) ----
COLORS = {
    "primary": "#4A6289",       # Xanh navy (nút, thanh bên, ô nhập)
    "primary_dark": "#3A4F6F",  # Xanh navy đậm hơn (khi rê chuột)
    "primary_light": "#5B7AAF", # Xanh navy nhạt hơn
    "bg": "#E8EDF2",            # Nền xanh-xám nhạt
    "card": "#FFFFFF",          # Thẻ nền trắng
    "card_border": "#C5D0DC",   # Khung thẻ border
    "text_dark": "#2C3E50",     # Chữ tối
    "text_light": "#7B8DA6",    # Chữ xám nhạt
    "text_white": "#FFFFFF",    # Chữ trắng
    "error": "#C0392B",         # Màu báo lỗi
    "success": "#27AE60",       # Màu thành công
    "warning": "#F39C12",       # Màu cảnh báo
    "sidebar_bg": "#4A6289",    # Nền thanh bên
    "navbar_bg": "#4A6289",     # Nền thanh điều hướng
    "input_bg": "#4A6289",      # Nền ô nhập liệu
    "input_fg": "#FFFFFF",      # Chữ trong ô nhập liệu
    "tab_active": "#2C3E50",    # Chữ tab đang chọn
    "tab_inactive": "#7B8DA6",  # Chữ tab chưa chọn
    "link": "#4A6289",          # Màu liên kết
}

# ---- Cấu hình phông chữ ----
FONTS = {
    "title": ("Segoe UI", 24, "bold italic"),
    "subtitle": ("Segoe UI", 11),
    "heading": ("Segoe UI", 16, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI", 11, "bold"),
    "nav": ("Segoe UI", 13, "bold"),
    "tab": ("Segoe UI", 11, "bold"),
    "card_title": ("Segoe UI", 10, "bold"),
    "card_icon": ("Segoe UI", 28),
    "input": ("Segoe UI", 11),
}

# ---- Kích thước cửa sổ ----
LOGIN_SIZE = "420x520"
DASHBOARD_SIZE = "1100x700"


class BaseView:
    """Lớp cơ sở cho mọi giao diện với giao diện và hàm tiện ích dùng chung."""

    def __init__(self, root):
        self.root = root

    def clear_window(self):
        """Xóa toàn bộ widget khỏi cửa sổ hiện tại."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def center_window(self, width, height):
        """Căn cửa sổ ra giữa màn hình."""
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def create_rounded_entry(parent, placeholder="", show="", width=280, height=40):
        """Tạo ô nhập liệu theo kiểu giao diện mẫu (nền xanh navy, chữ trắng)."""
        frame = tk.Frame(parent, bg=COLORS["input_bg"], highlightthickness=0)

        entry = tk.Entry(frame, font=FONTS["input"], bg=COLORS["input_bg"],
                         fg=COLORS["input_fg"], insertbackground=COLORS["input_fg"],
                         bd=0, highlightthickness=0, width=30)
        if show:
            entry.config(show=show)

        entry.pack(padx=15, pady=8, fill="x")

        # Hành vi văn bản gợi ý
        if placeholder:
            entry.insert(0, placeholder)
            entry._placeholder = placeholder
            entry._is_placeholder = True

            def on_focus_in(e):
                if entry._is_placeholder:
                    entry.delete(0, "end")
                    entry._is_placeholder = False
                    if show:
                        entry.config(show=show)

            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry._is_placeholder = True
                    if show:
                        entry.config(show="")

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            if show:
                entry.config(show="")  # Hiển thị placeholder dưới dạng văn bản thường

        frame.entry = entry
        return frame

    @staticmethod
    def get_entry_value(frame):
        """Lấy giá trị từ ô nhập liệu đã tạo kiểu, bỏ qua placeholder."""
        entry = frame.entry
        if hasattr(entry, '_is_placeholder') and entry._is_placeholder:
            return ""
        return entry.get().strip()

    @staticmethod
    def create_nav_button(parent, text, command, icon=""):
        """Tạo nút điều hướng theo kiểu giao diện."""
        btn_text = f"{icon}  {text}" if icon else text
        btn = tk.Button(parent, text=btn_text, font=FONTS["body"],
                        bg=COLORS["card"], fg=COLORS["text_dark"],
                        activebackground=COLORS["bg"], activeforeground=COLORS["primary"],
                        bd=0, padx=15, pady=8, anchor="w", cursor="hand2",
                        command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["bg"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["card"]))
        return btn

    @staticmethod
    def show_message(parent, message, msg_type="info"):
        """Hiển thị nhãn thông báo theo kiểu giao diện."""
        colors = {
            "info": COLORS["primary"],
            "success": COLORS["success"],
            "error": COLORS["error"],
            "warning": COLORS["warning"],
        }
        color = colors.get(msg_type, COLORS["text_dark"])
        lbl = tk.Label(parent, text=message, font=FONTS["small"],
                        fg=color, bg=parent.cget("bg"), wraplength=350)
        lbl.pack(pady=5)
        # Tự động xóa sau 5 giây
        parent.after(5000, lambda: lbl.destroy() if lbl.winfo_exists() else None)
        return lbl

    @staticmethod
    def draw_avatar(canvas, cx, cy, radius, color):
        """Vẽ biểu tượng avatar người dùng trên canvas (vòng tròn + nét người)."""
        # Vòng tròn ngoài
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                           outline=color, width=3)
        # Phần đầu
        hr = radius * 0.25
        canvas.create_oval(cx - hr, cy - radius * 0.55 - hr,
                           cx + hr, cy - radius * 0.55 + hr,
                           outline=color, width=2.5)
        # Cung thân người
        body_w = radius * 0.5
        canvas.create_arc(cx - body_w, cy - radius * 0.05,
                          cx + body_w, cy + radius * 0.65,
                          start=0, extent=180, style="arc",
                          outline=color, width=2.5)

