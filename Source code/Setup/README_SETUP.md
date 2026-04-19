# Hướng dẫn Khởi chạy và Setup (Local / Docker)

Thư mục này chứa các file cấu hình và kịch bản hỗ trợ khởi chạy nhanh dự án.

## Cách 1: Chạy trực tiếp (Khuyên dùng)
Dự án được xây dựng bằng thiết kế giao diện đồ họa **Tkinter**. Lựa chọn tối ưu và ít lỗi đồ họa nhất trên mọi hệ điều hành là chạy bằng Python thuần thiết lập qua môi trường ảo (Virtual Env), kịch bản tự động sẽ sinh venv cho bạn.
- **Trên Windows:** Bấm đúp chuột (chuột trái) vào file `install.bat`. Chọn `1`.
- **Trên macOS / Linux:** Mở terminal, gõ `chmod +x Setup/install.sh` để cấp quyền chạy, sau đó chạy `./Setup/install.sh` và chọn `1`.

## Cách 2: Chạy thông qua Docker Packages
Vì Tkinter là một ứng dụng đồ họa xuất ảnh lên Desktop, bản thân các Container rỗng của Docker sẽ cảnh báo lỗi thiếu Màn hình Hiển thị (`_tkinter.TclError: couldn't connect to display`).
Để chạy Docker an toàn:
1. **Trên Windows**: Tải giả lập X-Server, khuyên dùng **VcXsrv Windows X Server**. Mở **XLaunch** của VcXsrv -> Đánh dấu vào ô `"Disable access control"` -> Nhấp file `install.bat`, Chọn số `2` để Build Docker.
2. **Trên macOS**: Phải dùng phần mềm **XQuartz**. Hãy chạy ứng dụng XQuartz, vào Preference, tích chọn "Allow connections from network clients". Khởi động lại terminal tĩnh và máy Mac nếu cần. Chạy `./Setup/install.sh` rồi chọn `2`.
3. **Trên Linux**: Giao thức GUI đã kết tinh sẵn với X11, do đó bạn chỉ cần cấp quyền bằng lệnh Terminal: `xhost +local:docker`. Sau đó chạy `./Setup/install.sh` rồi chọn số `2`. Cờ thông số `-v /tmp/.X11-unix:/tmp/.X11-unix` đã hỗ trợ xuất file thẳng ra ngoài màn hình gốc.
