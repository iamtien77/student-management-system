# Tổng quan Dự án Student Management System (SMS)

Dự án này là một ứng dụng Quản lý Sinh viên được xây dựng bằng Python với giao diện người dùng đồ họa (GUI) sử dụng thư viện Tkinter. Hệ thống được tổ chức theo kiến trúc **Mô hình - Khung nhìn - Bộ điều khiển (MVC - Model-View-Controller)** nhằm mục đích bóc tách rõ ràng giữa phần xử lý dữ liệu, giao diện hiển thị và luồng điều khiển của ứng dụng.

## 1. Cấu trúc Thư mục

Hệ thống được chia thành các thành phần chính sau:

- **`main.py`**: Trái tim của chương trình. Chứa class `Application` phụ trách quản lý luồng điều hướng của toàn bộ hệ thống (Navigation), giữ phiên đăng nhập hiện tại và gọi các màn hình tương ứng.
- **`models/`**: Nơi chứa cấu trúc đại diện dữ liệu như `student.py`, `lecturer.py`, `admin.py`, `grade.py`, v.v. Các class ở đây chịu trách nhiệm thao tác với đối tượng thực tế và gọi `utils/file_handler.py` để lưu trữ dữ liệu xuống file text tĩnh.
- **`views/`**: Toàn bộ giao diện Tkinter được chia tách theo từng đối tượng người dùng:
  - `views/admin/`: Giao diện đặc quyền của Admin (Quản lý User, Lớp, Môn học...).
  - `views/student/`: Dashboard và giao diện của sinh viên (Xem điểm, chương trình đào tạo...).
  - `views/lecturer/`: Dashboard của giảng viên (Chấm điểm, điểm danh...).
  - `views/auth/`: Các màn hình Login, Đổi mật khẩu.
  - `views/components/`: Nơi chứa các thành phần dùng chung như `CrudView` (bảng quản lý dữ liệu động).
- **`controllers/`**: Là cầu nối giữa giao diện và models với một số luồng nghiệp vụ phức tạp về Auth hoặc quản lý tài khoản.
- **`utils/`**: Các file hỗ trợ độc lập:
  - `file_handler.py`: Modun duy nhất tương tác trực tiếp (đọc/ghi/xoá) với các file `.txt` trong database.
  - `auth_helper.py`: Băm (hash) mật khẩu và sinh nội dung auth.
  - `validators.py`: Kiểm tra tính hợp lệ của dữ liệu đầu vào.
- **`data/`**: Chứa các file `*.txt` hoạt động giống như một cơ sở dữ liệu để lưu trữ (ví dụ: `students.txt`, `accounts.txt`).

---

## 2. Hướng dẫn Code & Mở rộng Chức năng Cốt lõi

Nếu bạn muốn thêm một chức năng mới, hãy tuân theo các bước sau trong kiến trúc (Ví dụ: Thêm chức năng xem "Học bổng"):

### Bước 1: Khởi tạo/Cập nhật Models (`models/`)
- Mọi dữ liệu đều phải được map lên class. Ví dụ, thiết kế một lớp `Scholarship` trong `models/scholarship.py`.
- Tích hợp hàm tĩnh `find_by_id()`, `get_all()`, hoặc `save()` bên trong lớp đó, và bạn phải gọi trực tiếp hàm xử lý file từ `utils.file_handler` để đọc ghi file `.txt` dưới thư mục `data`.

### Bước 2: Thiết kế Giao diện Views (`views/`)
- Bạn tạo file View mới (vd: `views/student/scholarship_view.py`).
- Mọi View phải kết thừa từ `BaseView` (nằm trong `views.base_view`). `BaseView` cung cấp các tính năng hỗ trợ như xoá sạch window hiện tại trước khi vẽ lại, thiết lập phong cách màu nền (COLORS, FONTS).
- Trong phương thức `__init__`, luôn nhận vào hàm điều hướng `navigate_to` và account đang đăng nhập hiện để hỗ trợ quay về/chuyển trang.
- Trong phương thức `show()`, hãy gọi các element Tkinter để vẽ giao diện (`_build_ui()`).

### Bước 3: Đăng ký Định tuyến trong `main.py`
- Mở `main.py`.
- Tìm hàm navigate của tài khoản tương ứng (ví dụ: `_student_navigate(self, view_name)`).
- Thêm logic kiểm tra cho view của bạn:
  ```python
  elif view_name == "scholarship":
      from views.student.scholarship_view import ScholarshipView
      ScholarshipView(self.root, self._account, self._student_navigate).show()
  ```

### Bước 4: Khai báo Phím bấm / Menu trong View gọi đến 
- Cập nhật lại giao diện Dashboard (ví dụ: `views/student/dashboard.py`).
- Thêm thẻ nút bấm để kích hoạt hàm `self._navigate("scholarship")`.

## 3. Chi tiết Việc cần làm ở từng tầng kiến trúc

Dưới đây là bảng trách nhiệm để giữ cho code luôn "sạch" và đúng chuẩn MVC:

### 3.1. Tầng Models (`models/` - Định hình cấu trúc và logic Dữ liệu)
Đây là nơi bạn khai báo các Thực thể (Entities) của hệ thống (ví dụ: `SinhVien`, `GiangVien`, `MonHoc`).
*   **Cần làm:**
    *   Tạo các class đại diện cho cấu trúc của một đối tượng (ví dụ: class `Student` cần lưu ID, tên, tuổi, ngành...).
    *   Viết các phương thức tính toán kinh doanh gắn liền với đối tượng đó (ví dụ tính Điểm Trung Bình, xét học lực...).
    *   Viết các phương thức Class Method (như `find_by_id()`, `save()`, `get_all()`) để ra lệnh gọi xuống Data lưu/đọc dữ liệu.
*   **Không được làm:**
    *   Tuyệt đối **không** được `import tkinter` ở đây. Model không được biết bất cứ thứ gì về màu sắc, nút bấm hay giao diện.

### 3.2. Tầng Views (`views/` - Phần nhìn và Giao tiếp UI)
Đây là màn hình hiển thị trực tiếp cho người dùng.
*   **Cần làm:**
    *   Viết code để "vẽ" giao diện: tạo Cửa sổ, Nút (Button), Bảng (Grid/Treeview), Nhãn (Label)... bằng module Tkinter.
    *   Lắng nghe hành động của người dùng (bắt các sự kiện click chuột/bấm phím).
    *   Đọc dữ liệu từ Models để hiển thị lên UI (ví dụ: lấy giá trị `student.fullName` để in lên màn hình).
*   **Không được làm:**
    *   Không viết các logic tính toán phức tạp, đọc ghi file Database ở đây.
    *   Không tự ý nhảy trang (Navigation) trực tiếp từ Views. Bạn bắt buộc phải "ủy quyền" lệnh yêu cầu chuyển trang cho `main.py` thông qua hàm callback truyền từ khởi tạo.

### 3.3. Tầng Controllers (`controllers/` & `main.py` - Người điều phối)
Thường làm nhiệm vụ quản lý luồng ứng dụng và làm cầu nối ghép các tầng lại với nhau:
*   **Trong `main.py` (Navigation Controller):**
    *   Quản lý toàn bộ quá trình nhảy qua lại giữa các màn hình (Người đùng ấn "Logout" thì bộ này lo việc chuyển từ bảng điều khiển về Login).
    *   Giữ trạng thái đăng nhập chung (Ai đang là người sử dụng phiên làm việc hiện tại).
*   **Trong `controllers/` (Business Controller):**
    *   Tập hợp các luồng chức năng lớn yêu cầu kiểm duyệt dữ liệu trước khi hành động. (Ví dụ: Hàm tạo tài khoản sẽ phải check tính hợp lệ, sau đó mã hóa pass, rồi gọi model lưu Account, và cuối cùng mới gọi model lưu Profile).
*   **Không được làm:**
    *   Controller không nên chứa code in hay vẽ Giao diện (trừ thao tác khởi sinh class View).

### 3.4. Tầng Utils & Data (Tầng đáy)
*   **Tiện ích (`utils/`)**: Nơi bạn viết các "công cụ hỗ trợ" tái sử dụng toàn bộ.
    *   `file_handler.py`: Logic đọc/ghi file text nguyên thủy và chèn/xóa chuỗi dòng.
    *   `validators.py`: Check định dạng email, sđt...
    *   `auth_helper.py`: Tools hash password bảo mật.
*   **Dữ liệu (`data/`)**: Mọi thao tác lưu dữ liệu đều đưa chữ thô thành tệp dạng bảng bằng `.txt` (như `students.txt`). Đây hoàn toàn là vùng lưu trữ thụ động.

---

## 4. Quy tắc cần nhớ

1. **Không can thiệp Tkinter trong Models**: Tầng Models chỉ đại diện cho object data và logic CRUD, tuyệt đối không *import tkinter* tại đây.
2. **Quản lý Routing tập trung**: Việc nhảy tab, thay đổi trang chỉ được xử lý ở `main.py` (`Application._navigate`). Views không tự huỷ chính mình để mở view khác, nó phải gọi `self._navigate()`.
3. **Màu sắc và Theme đồng bộ**: Bất cứ nút bấm (`tk.Button`), nhãn (`tk.Label`), khung (`tk.Frame`) nào cũng phải truyền `bg` (background) và `fg` theo cấu hình `COLORS`, `FONTS` quy định tại `base_view.py` để tránh phá vỡ giao diện chung của hệ thống.
