# User Model - Quản lý tài khoản
# Fields:
#   - id: Primary key
#   - username: Unique, không null
#   - email: Unique, validated email format
#   - password_hash: Mã hóa bcrypt (không lưu plaintext!)
#   - role: enum('admin', 'teacher', 'student')
#   - is_active: Boolean (khóa/mở tài khoản)
#   - login_attempts: Số lần đăng nhập sai (reset sau 5 phút)
#   - locked_until: Thời gian khóa tài khoản
#   - last_login: Lần đăng nhập cuối
#   - created_at: Ngày tạo
#   - updated_at: Ngày cập nhật
#
# Methods:
#   - set_password(): Hash và lưu password
#   - check_password(): Kiểm tra password
#   - is_locked(): Kiểm tra tài khoản bị khóa
#   - increment_login_attempts(): Tăng số lần đăng nhập sai
#   - reset_login_attempts(): Reset về 0
