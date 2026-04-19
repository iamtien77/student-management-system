"""
views/components/crud_view.py
component CRUD tai su dung duoc cho tat ca man hinh quan ly du lieu:
  - hien thi bang du lieu (Treeview)
  - thanh cong cu (tim kiem, them, sua, xoa)
  - bien co chon hang
su dung bang cach truyen cau hinh (columns, data, callbacks) tu ben ngoai vao
"""

import tkinter as tk
from tkinter import ttk
from views.base_view import COLORS, FONTS


class CrudView:
    """
    component bang CRUD tong quat
    duoc nhung vao trong cac View lon de tao phan quan ly du lieu

    tham so khoi tao:
      parent   : frame cha se chua component nay
      columns  : list[dict] vd [{"key":"id","label":"Ma","width":80}, ...]
      on_add   : callable → mo hop thoai them moi
      on_edit  : callable(row_data: dict) → mo hop thoai sua
      on_delete: callable(row_data: dict) → xu ly xoa
      on_search: callable(query: str) → list[dict] → tra du lieu da loc
      title    : tieu de hien thi phia tren bang
    """

    def __init__(self, parent, columns: list,
                 on_add=None, on_edit=None, on_delete=None,
                 on_search=None, title: str = ""):
        self.parent    = parent
        self.columns   = columns
        self.on_add    = on_add
        self.on_edit   = on_edit
        self.on_delete = on_delete
        self.on_search = on_search
        self.title     = title

        # bien luu du lieu dang hien thi (list of dict)
        self._current_data: list = []

        self._build(parent)

    # -----------------------------------------------------------------------
    # XAY DUNG GIAO DIEN COMPONENT
    # -----------------------------------------------------------------------

    def _build(self, parent):
        """xay dung toan bo layout cua component CrudView"""
        container = tk.Frame(parent, bg=COLORS["bg"])
        container.pack(fill="both", expand=True, padx=16, pady=8)

        # --- tieu de ---
        if self.title:
            tk.Label(container, text=self.title,
                     font=FONTS["header"], fg=COLORS["text_dark"],
                     bg=COLORS["bg"]).pack(anchor="w", pady=(0, 8))

        # --- thanh cong cu (search + nut) ---
        toolbar = tk.Frame(container, bg=COLORS["bg"])
        toolbar.pack(fill="x", pady=(0, 8))

        # o tim kiem
        self._search_var = tk.StringVar()
        search_frame = tk.Frame(toolbar, bg=COLORS["bg"])
        search_frame.pack(side="left")

        tk.Label(search_frame, text="🔍", font=FONTS["default"],
                 bg=COLORS["bg"]).pack(side="left", padx=(0, 4))
        search_entry = tk.Entry(
            search_frame, textvariable=self._search_var,
            font=FONTS["input"], width=26, relief="solid", bd=1,
            bg=COLORS["white"]
        )
        search_entry.pack(side="left")

        # khi nguoi dung nhap vao o tim kiem → goi _do_search sau 300ms
        self._search_var.trace_add("write", lambda *a: self.parent.after(
            300, self._do_search))

        # cac nut hanh dong
        btn_frame = tk.Frame(toolbar, bg=COLORS["bg"])
        btn_frame.pack(side="right")

        if self.on_add:
            self._make_toolbar_btn(btn_frame, "+ Them moi", self.on_add, "success")
        if self.on_edit:
            self._make_toolbar_btn(btn_frame, "✏ Sua", self._edit_selected, "primary")
        if self.on_delete:
            self._make_toolbar_btn(btn_frame, "🗑 Xoa", self._delete_selected, "danger")

        # --- bang du lieu treeview ---
        table_frame = tk.Frame(container, bg=COLORS["bg"])
        table_frame.pack(fill="both", expand=True)

        # setup style cho treeview
        self._setup_style()

        # scrollbar doc
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # scrollbar ngang
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # treeview chinh
        col_keys = [c["key"] for c in self.columns]
        self.tree = ttk.Treeview(
            table_frame,
            columns=col_keys,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode="browse",        # chi cho phep chon 1 hang
        )
        self.tree.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # cai dat tieu de va do rong tung cot
        for col in self.columns:
            self.tree.heading(col["key"], text=col["label"],
                              anchor="center")
            self.tree.column(col["key"],
                             width=col.get("width", 120),
                             minwidth=60,
                             anchor=col.get("anchor", "center"))

        # dat mau xen ke hang chan/le khi chon hang
        self.tree.tag_configure("even", background=COLORS["row_even"])
        self.tree.tag_configure("odd",  background=COLORS["row_odd"])

        # --- dong thong tin so luong ban ghi ---
        self._info_label = tk.Label(
            container, text="", font=FONTS["small"],
            fg=COLORS["text_muted"], bg=COLORS["bg"]
        )
        self._info_label.pack(anchor="w", pady=(4, 0))

    def _setup_style(self):
        """ap dung CSS-like phong cach cho Treeview"""
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
        style.map(
            "Custom.Treeview",
            background=[("selected", COLORS["row_selected"])],
            foreground=[("selected", COLORS["text_dark"])],
        )

    def _make_toolbar_btn(self, parent, text: str, command, style: str):
        """tao nut tren thanh cong cu voi phong cach tuong ung"""
        color_map = {
            "success": COLORS["success"],
            "primary": COLORS["accent"],
            "danger":  COLORS["error"],
        }
        bg = color_map.get(style, COLORS["accent"])
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=COLORS["white"],
            font=FONTS["small_bold"],
            relief="flat", cursor="hand2",
            padx=12, pady=5
        )
        btn.pack(side="left", padx=3)
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["primary_dark"] if style == "primary" else bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))

    # -----------------------------------------------------------------------
    # CAP NHAT DU LIEU TRONG BANG
    # -----------------------------------------------------------------------

    def load_data(self, data: list):
        """
        tai danh sach du lieu vao bang (list of dict)
        moi dict phai co day du cac key tuong ung voi cot da dinh nghia
        """
        self._current_data = data
        self._render_rows(data)

    def _render_rows(self, data: list):
        """xoa bang cu va ve lai voi du lieu moi, to mau xen ke hang"""
        # xoa toan bo hang cu
        for item in self.tree.get_children():
            self.tree.delete(item)

        # chen tung hang moi
        for i, record in enumerate(data):
            values = [record.get(c["key"], "") for c in self.columns]
            tag    = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=values, tags=(tag,))

        # cap nhat dong thong tin so luong
        self._info_label.config(
            text=f"Hien thi {len(data)} / {len(self._current_data)} ban ghi"
        )

    # -----------------------------------------------------------------------
    # TIM KIEM
    # -----------------------------------------------------------------------

    def _do_search(self):
        """
        loc du lieu dua tren tu khoa trong o tim kiem
        neu co on_search tu ben ngoai → goi callback do
        nguoc lai → tu loc noi bo bang cach tim kiem toan van trong tat ca cot
        """
        query = self._search_var.get().strip().lower()

        if self.on_search:
            # nhung vao callback loc tu ben ngoai (su dung model de loc)
            filtered = self.on_search(query)
        else:
            # tu loc noi bo: duyet tat ca cot, kiem tra xem co chuoi con khop khong
            if not query:
                filtered = self._current_data
            else:
                filtered = [
                    row for row in self._current_data
                    if any(query in str(v).lower() for v in row.values())
                ]

        self._render_rows(filtered)

    # -----------------------------------------------------------------------
    # XU LY NUT HANH DONG
    # -----------------------------------------------------------------------

    def _get_selected_row_data(self) -> dict | None:
        """
        lay du lieu cua hang dang duoc chon trong bang
        tra ve dict hoac None neu chua chon hang nao
        """
        selection = self.tree.selection()
        if not selection:
            return None

        # lay cac gia tri cua hang duoc chon
        values = self.tree.item(selection[0], "values")
        # map nguoc lai vao dict bang thu tu cot
        return {col["key"]: val for col, val in zip(self.columns, values)}

    def _edit_selected(self):
        """khi bam nut Sua: lay du lieu hang dang chon roi goi callback on_edit"""
        row_data = self._get_selected_row_data()
        if not row_data:
            from tkinter import messagebox
            messagebox.showwarning("Chua chon", "Vui long chon 1 hang de sua")
            return
        self.on_edit(row_data)

    def _delete_selected(self):
        """khi bam nut Xoa: xac nhan roi goi callback on_delete"""
        row_data = self._get_selected_row_data()
        if not row_data:
            from tkinter import messagebox
            messagebox.showwarning("Chua chon", "Vui long chon 1 hang de xoa")
            return
        self.on_delete(row_data)

    # -----------------------------------------------------------------------
    # UTILITY
    # -----------------------------------------------------------------------

    def clear_search(self):
        """xoa noi dung o tim kiem"""
        self._search_var.set("")

    def refresh(self, new_data: list):
        """tai lai bang voi du lieu moi (goi sau khi them/sua/xoa thanh cong)"""
        self.load_data(new_data)
