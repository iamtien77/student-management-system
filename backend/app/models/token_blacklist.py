# Token Blacklist Model - Quản lý token bị thu hồi
# Fields:
#   - id: Primary key
#   - jti: JWT ID (unique identifier của token)
#   - token_type: access / refresh
#   - user_id: Foreign key to User
#   - revoked_at: Thời gian thu hồi
#   - expires_at: Thời gian hết hạn của token
#
# Dùng để:
#   - Thu hồi token khi logout
#   - Vô hiệu hóa tất cả token khi đổi password
#   - Xóa token hết hạn định kỳ
