# Rate Limiter Middleware
# Chống brute force attack
# Functions:
#   - rate_limit(): Decorator giới hạn request
#   - check_rate_limit(): Kiểm tra số lượng request
#   - Config: 5 login attempts / 5 minutes
#   - Config: 100 API calls / minute
