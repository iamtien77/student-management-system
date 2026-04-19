# Sử dụng phiên bản Python chính thức (bản slim để giảm kích thước image)
FROM python:3.11-slim

# Cài đặt system dependencies (Tkinter, X11 apps, timezone)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-tk \
    x11-apps \
    tzdata && \
    rm -rf /var/lib/apt/lists/*

# Chỉnh múi giờ đồng hồ
ENV TZ="Asia/Ho_Chi_Minh"

# Đặt thư mục làm việc
WORKDIR /app

# Copy requirements.txt trước (tối ưu layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Biến môi trường cho Tkinter (đẩy display ra host)
ENV DISPLAY=host.docker.internal:0.0

# Tạo thư mục cho mock data
RUN mkdir -p /app/Source/test_data_mock

# Chạy ứng dụng chính
CMD ["python", "Source/main.py"]
