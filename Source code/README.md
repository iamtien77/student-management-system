# Hệ thống Quản lý Sinh viên (Student Management System)

Đây là một ứng dụng Desktop được phát triển bằng Python (Tkinter) hoạt động dưới mô hình MVC (Model-View-Controller) kết hợp với lưu trữ dữ liệu dạng tệp văn bản. Hệ thống cung cấp các chức năng quản lý toàn diện đối với hoạt động đào tạo của một cơ sở giáo dục, bao gồm quản lý sinh viên, giảng viên, môn học, lớp học phần, điểm số và điểm danh.

## Tính năng chính

Hệ thống cung cấp giao diện và các tính năng tương ứng với 3 vai trò (Roles) chính:

### 1. Quản trị viên (Admin)
- **Quản lý Tài khoản**: Tạo tài khoản, chuyển quyền, vô hiệu hóa, gán vai trò.
- **Quản lý dữ liệu Cấu trúc**: Quản lý thông tin Khoa, Học kỳ, Môn học.
- **Quản lý Thể nhân**: Quản lý hồ sơ Sinh viên, Giảng viên.
- **Quản lý Lớp học phần**: Mở lớp, cập nhật, xóa lớp học phần.
- **Quản lý Công việc**: Phân công giảng viên giảng dạy, chốt điểm (Finalize Grades).

### 2. Giảng viên (Lecturer)
- **Thông tin cá nhân**: Xem và cập nhật hồ sơ thông tin cá nhân.
- **Môn học & Sinh viên**: Theo dõi lịch giảng dạy.
- **Quá trình học tập**: Thực hiện điểm danh sinh viên, nhập điểm các cột (quá trình, giữa kỳ, cuối kỳ).

### 3. Sinh viên (Student)
- **Thông tin cá nhân**: Xem và cập nhật hồ sơ.
- **Thông tin học tập**: Xem chương trình đào tạo (môn học yêu cầu), xem điểm số các môn đã/đang học.

## Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.11+
- **Giao diện (UI/UX)**: `Tkinter` (Custom Python UI)
- **Lưu trữ dữ liệu**: Quản lý dựa trên tập tin cơ bản (Text files `*.txt`)
- **Kiến trúc Thiết kế**: Áp dụng chặt chẽ mô hình MVC (Model - View - Controller), lập trình hướng đối tượng (OOP).
- **Triển khai (Deployment)**: Hỗ trợ Docker và Docker Compose.

## Cấu trúc thư mục định dạng

```text
├── Source/
│   ├── main.py                # Điểm vào chính, điều khiển luồng của ứng dụng
│   ├── controllers/           # Chứa các mô-đun xử lý điều hướng logic
│   ├── models/                # Các class mô hình dữ liệu (Account, Student, Course, v.v.)
│   ├── views/                 # Giao diện người dùng cho các Roles & Components
│   ├── utils/                 # Các tiện ích hệ thống (mã hóa mật khẩu, file handler...)
│   └── data/                  # Nơi lưu trữ file CSDL .txt 
├── tests/                     # (Nếu có) - Các thư mục chứa test script
├── requirements.txt           # Danh sách các thư viện cần cài đặt (nếu có bổ sung ngoài built-in)
├── Dockerfile                 # Dùng để xây dựng image Docker cho ứng dụng Tkinter
├── docker-compose.yml         # Trình cấu hình chạy Docker
└── README.md                  # Tài liệu hệ thống
```

## Hướng dẫn Cài đặt & Chạy ứng dụng

### Cách 1: Chạy trực tiếp (Local)

1. Yêu cầu đã cài đặt Python 3.11 trở lên trên máy tĩnh.
2. Cài đặt các thư viện phụ thuộc (nếu có trong `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy file chính từ thư mục gốc hoặc trong Source/:
   ```bash
   python Source/main.py
   ```

### Cách 2: Chạy thông qua Docker

Do ứng dụng có hệ thống GUI bằng Tkinter, việc chạy qua docker cần forward X11 socket.

1. Khởi động Docker Desktop (Đảm bảo có X-Server sẵn, với Windows khuyến cáo cấu hình VcXsrv hoặc Xming).
2. Thiết lập thông số biến môi trường `DISPLAY` nếu trên Windows.
3. Chạy lệnh:
   ```bash
   docker-compose up --build
   ```

## Thông tin đăng nhập mặc định

Lần đầu chạy, hệ thống sẽ tự sinh ra tài khoản Admin mặc định để sử dụng:

- **Tên đăng nhập (Username)**: `iamtien`
- **Mật khẩu (Password)**: `Tien77@`
- **Quyền (Role)**: `Admin`

---
*Phát triển hỗ trợ mục đích Đồ án/Bài tập Quản lý Hệ thống - 2026.*
