"""
Màn hình đổi mật khẩu - UC5 (dùng chung cho mọi vai trò)
Nhập mật khẩu hiện tại → mật khẩu mới → xác nhận → kiểm tra hợp lệ → lưu.
"""
import tkinter as tk
from tkinter import messagebox
from views.base_view import BaseView, COLORS, FONTS


class ChangePasswordView(BaseView):
    def __init__(self, root, account, navigate_to):
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to

    def show(self):
        self.clear_window()
        self.root.title("SMS - Change Password")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(450, 480)
        self.root.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        card = tk.Frame(self.root, bg=COLORS["card"],
                        highlightbackground=COLORS["card_border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=430)

        tk.Label(card, text="Change Password", font=FONTS["title"],
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(25, 5))
        tk.Label(card, text=f"Account: {self._account.username}",
                 font=FONTS["body"], fg=COLORS["text_light"],
                 bg=COLORS["card"]).pack(pady=(0, 20))

        self._old_pwd = self.create_rounded_entry(card, "Current Password", show="*")
        self._old_pwd.pack(padx=40, fill="x", pady=6)

        self._new_pwd = self.create_rounded_entry(card, "New Password", show="*")
        self._new_pwd.pack(padx=40, fill="x", pady=6)

        self._confirm = self.create_rounded_entry(card, "Confirm New Password", show="*")
        self._confirm.pack(padx=40, fill="x", pady=6)

        self._msg_frame = tk.Frame(card, bg=COLORS["card"], height=30)
        self._msg_frame.pack(fill="x", padx=40)

        btn_frame = tk.Frame(card, bg=COLORS["card"])
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save", font=FONTS["button"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=25, pady=6,
                  cursor="hand2", command=self._save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", font=FONTS["button"],
                  bg=COLORS["text_light"], fg="white", bd=0, padx=20, pady=6,
                  cursor="hand2",
                  command=lambda: self._navigate("dashboard")).pack(side="left")

    def _save(self):
        for w in self._msg_frame.winfo_children():
            w.destroy()

        old = self.get_entry_value(self._old_pwd)
        new = self.get_entry_value(self._new_pwd)
        confirm = self.get_entry_value(self._confirm)

        if not old or not new or not confirm:
            self.show_message(self._msg_frame, "All fields are required.", "error")
            return
        if new != confirm:
            self.show_message(self._msg_frame, "New passwords do not match.", "error")
            return

        success, msg = self._account.changePassword(old, new)
        if success:
            messagebox.showinfo("Success", "Password changed successfully.\nPlease login again.")
            self._navigate("logout")
        else:
            self.show_message(self._msg_frame, msg, "error")
