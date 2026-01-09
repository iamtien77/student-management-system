# Configuration - Cấu hình ứng dụng
# 
# Security Settings:
#   - SECRET_KEY: Khóa bí mật cho Flask session
#   - JWT_SECRET_KEY: Khóa bí mật cho JWT
#   - JWT_ACCESS_TOKEN_EXPIRES: Thời gian hết hạn access token (1 hour)
#   - JWT_REFRESH_TOKEN_EXPIRES: Thời gian hết hạn refresh token (7 days)
#   - BCRYPT_LOG_ROUNDS: Độ phức tạp mã hóa password (12)
#   - PASSWORD_MIN_LENGTH: Độ dài tối thiểu password (8)
#
# Database Settings:
#   - SQLALCHEMY_DATABASE_URI: Connection string MySQL
#   - SQLALCHEMY_TRACK_MODIFICATIONS: False
#
# Rate Limiting:
#   - RATELIMIT_DEFAULT: 100/hour
#   - RATELIMIT_LOGIN: 5/5minutes
#
# CORS Settings:
#   - CORS_ORIGINS: Allowed origins list
