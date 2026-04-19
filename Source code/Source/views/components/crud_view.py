"""
Màn hình CRUD dùng chung - tái sử dụng để quản lý Sinh viên, Giảng viên,
Khoa, Học kỳ, Môn học, Lớp học phần.
Sử dụng bảng Treeview cùng các nút Thêm/Sửa/Xóa.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView, COLORS, FONTS


class CrudView(BaseView):
    """
    Màn hình CRUD tổng quát với bảng dữ liệu và hộp thoại biểu mẫu.
    Lớp con cấu hình: title, columns, model_class, fields.
    """

    def __init__(self, root, account, navigate_to, config):
        """
        config = {
            'title': str,
            'columns': [(col_id, heading, width), ...],
            'fields': [(field_name, label, editable_on_update: bool), ...],
            'get_all': callable -> list of tuples,
            'add': callable(data_dict) -> (success, msg),
            'update': callable(data_dict) -> (success, msg),
            'delete': callable(key) -> (success, msg),
            'key_field': str (tên trường dùng làm khóa chính),
        }
        """
        super().__init__(root)
        self._account = account
        self._navigate = navigate_to
        self._config = config

    def show(self):
        self.clear_window()
        self.root.title(f"SMS - {self._config['title']}")
        self.root.configure(bg=COLORS["bg"])
        self.center_window(1100, 700)
        self._build_ui()

    def _build_ui(self):
        # Thanh điều hướng
        navbar = tk.Frame(self.root, bg=COLORS["navbar_bg"], height=50)
        navbar.pack(fill="x")
        navbar.pack_propagate(False)

        back_btn = tk.Button(navbar, text="< Back", font=FONTS["body"],
                             fg="white", bg=COLORS["navbar_bg"],
                             activebackground=COLORS["primary_dark"],
                             bd=0, cursor="hand2",
                             command=lambda: self._navigate("dashboard"))
        back_btn.pack(side="left", padx=15)

        tk.Label(navbar, text=self._config['title'], font=FONTS["nav"],
                 fg="white", bg=COLORS["navbar_bg"]).pack(side="left", padx=10)

        # Nội dung
        content = tk.Frame(self.root, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Thanh nút chức năng
        btn_bar = tk.Frame(content, bg=COLORS["bg"])
        btn_bar.pack(fill="x", pady=(0, 10))

        tk.Button(btn_bar, text="+ Add", font=FONTS["body_bold"],
                  bg=COLORS["success"], fg="white", bd=0, padx=15, pady=5,
                  cursor="hand2", command=self._show_add_dialog).pack(side="left", padx=5)
        tk.Button(btn_bar, text="Edit", font=FONTS["body_bold"],
                  bg=COLORS["warning"], fg="white", bd=0, padx=15, pady=5,
                  cursor="hand2", command=self._show_edit_dialog).pack(side="left", padx=5)
        tk.Button(btn_bar, text="Delete", font=FONTS["body_bold"],
                  bg=COLORS["error"], fg="white", bd=0, padx=15, pady=5,
                  cursor="hand2", command=self._do_delete).pack(side="left", padx=5)
        tk.Button(btn_bar, text="Refresh", font=FONTS["body_bold"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=15, pady=5,
                  cursor="hand2", command=self._refresh).pack(side="right", padx=5)

        # Bảng dữ liệu
        table_frame = tk.Frame(content, bg=COLORS["card"])
        table_frame.pack(fill="both", expand=True)

        columns = [c[0] for c in self._config['columns']]
        self._tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                   selectmode="browse")

        # Cấu hình kiểu hiển thị
        style = ttk.Style()
        style.configure("Treeview", font=FONTS["body"], rowheight=28,
                        background=COLORS["card"], fieldbackground=COLORS["card"])
        style.configure("Treeview.Heading", font=FONTS["body_bold"],
                        background=COLORS["primary"], foreground="white")

        for col_id, heading, width in self._config['columns']:
            self._tree.heading(col_id, text=heading)
            self._tree.column(col_id, width=width, minwidth=50)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                   command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Màu xen kẽ giữa các dòng
        self._tree.tag_configure("oddrow", background="#F5F7FA")
        self._tree.tag_configure("evenrow", background=COLORS["card"])

        self._refresh()

    def _refresh(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        records = self._config['get_all']()
        for i, record in enumerate(records):
            tag = "oddrow" if i % 2 else "evenrow"
            self._tree.insert("", "end", values=record, tags=(tag,))

    def _show_add_dialog(self):
        self._show_form_dialog("Add", {})

    def _show_edit_dialog(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return
        values = self._tree.item(selected[0], "values")
        data = {}
        columns = [c[0] for c in self._config['columns']]
        for i, col in enumerate(columns):
            if i < len(values):
                data[col] = values[i]
        self._show_form_dialog("Edit", data)

    def _show_form_dialog(self, mode, data):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{mode} - {self._config['title']}")
        dialog.configure(bg=COLORS["card"])
        dialog.geometry("450x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Căn giữa hộp thoại
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 450) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 500) // 2
        dialog.geometry(f"+{x}+{y}")

        tk.Label(dialog, text=f"{mode} Record", font=FONTS["heading"],
                 fg=COLORS["primary"], bg=COLORS["card"]).pack(pady=(15, 10))

        # Biểu mẫu cuộn được
        content_frame = tk.Frame(dialog, bg=COLORS["card"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        form_canvas = tk.Canvas(content_frame, bg=COLORS["card"], highlightthickness=0)
        form_scroll = ttk.Scrollbar(content_frame, orient="vertical", command=form_canvas.yview)
        form_frame = tk.Frame(form_canvas, bg=COLORS["card"])

        form_frame.bind("<Configure>",
                        lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw")
        form_canvas.configure(yscrollcommand=form_scroll.set)

        form_canvas.pack(side="left", fill="both", expand=True)
        form_scroll.pack(side="right", fill="y")

        entries = {}
        for field_name, label, editable_on_update in self._config['fields']:
            tk.Label(form_frame, text=label + ":", font=FONTS["body_bold"],
                     fg=COLORS["text_dark"], bg=COLORS["card"],
                     anchor="w").pack(fill="x", pady=(8, 2))
            entry = tk.Entry(form_frame, font=FONTS["input"], bd=1,
                             relief="solid", highlightcolor=COLORS["primary"])
            entry.pack(fill="x", pady=(0, 2), ipady=4)

            if field_name in data:
                entry.insert(0, data[field_name])
            if mode == "Edit" and not editable_on_update:
                entry.config(state="readonly", readonlybackground="#E8E8E8")

            entries[field_name] = entry

        # Khu vực thông báo
        msg_frame = tk.Frame(dialog, bg=COLORS["card"], height=30)
        msg_frame.pack(fill="x", padx=20)

        # Các nút
        btn_frame = tk.Frame(dialog, bg=COLORS["card"])
        btn_frame.pack(pady=10)

        def save():
            for w in msg_frame.winfo_children():
                w.destroy()
            result = {}
            for field_name, label, _ in self._config['fields']:
                result[field_name] = entries[field_name].get().strip()
                if not result[field_name]:
                    self.show_message(msg_frame, f"{label} cannot be empty.", "error")
                    entries[field_name].config(highlightbackground=COLORS["error"],
                                               highlightthickness=2)
                    return

            if mode == "Add":
                success, msg = self._config['add'](result)
            else:
                success, msg = self._config['update'](result)

            if success:
                dialog.destroy()
                self._refresh()
                messagebox.showinfo("Success", msg)
            else:
                self.show_message(msg_frame, msg, "error")

        tk.Button(btn_frame, text="Save", font=FONTS["button"],
                  bg=COLORS["primary"], fg="white", bd=0, padx=20, pady=6,
                  cursor="hand2", command=save).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", font=FONTS["button"],
                  bg=COLORS["text_light"], fg="white", bd=0, padx=20, pady=6,
                  cursor="hand2", command=dialog.destroy).pack(side="left")

    def _do_delete(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        values = self._tree.item(selected[0], "values")
        key_field = self._config['key_field']
        columns = [c[0] for c in self._config['columns']]
        key_idx = columns.index(key_field) if key_field in columns else 0
        key_val = values[key_idx]

        if messagebox.askyesno("Confirm", f"Delete record '{key_val}'?"):
            success, msg = self._config['delete'](key_val)
            if success:
                self._refresh()
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

