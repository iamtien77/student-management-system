# Activity Log Model - Ghi lại hoạt động
# Fields:
#   - id: Primary key
#   - user_id: Foreign key to User
#   - action: Loại hành động (login, logout, create, update, delete)
#   - table_name: Bảng bị ảnh hưởng
#   - record_id: ID record bị ảnh hưởng
#   - ip_address: Địa chỉ IP
#   - user_agent: Trình duyệt/thiết bị
#   - created_at: Thời gian
#
# Dùng để:
#   - Theo dõi ai làm gì
#   - Phát hiện hành vi bất thường
#   - Audit trail cho bảo mật
