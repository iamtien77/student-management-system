# Auth Middleware - JWT Authentication
# Functions:
#   - token_required(): Decorator kiểm tra JWT token hợp lệ
#   - admin_required(): Decorator kiểm tra quyền admin
#   - teacher_required(): Decorator kiểm tra quyền giảng viên
#   - get_current_user(): Lấy thông tin user từ token
#   - create_access_token(): Tạo JWT access token (hết hạn 1 giờ)
#   - create_refresh_token(): Tạo refresh token (hết hạn 7 ngày)
#   - verify_token(): Xác thực token
#   - revoke_token(): Thu hồi token (logout)
#   - check_token_blacklist(): Kiểm tra token đã bị thu hồi chưa
