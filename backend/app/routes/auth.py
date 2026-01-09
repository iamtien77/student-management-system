# Auth Routes - Xác thực người dùng
# 
# POST /api/auth/login
#   - Validate input (username, password)
#   - Check rate limit (5 attempts / 5 min)
#   - Verify password với bcrypt
#   - Generate JWT tokens
#   - Log đăng nhập
#
# POST /api/auth/logout
#   - Revoke token (thêm vào blacklist)
#
# POST /api/auth/refresh
#   - Tạo access token mới từ refresh token
#
# GET /api/auth/me
#   - Lấy thông tin user hiện tại
#
# PUT /api/auth/change-password
#   - Validate password cũ
#   - Validate password mới (độ mạnh)
#   - Hash password mới
