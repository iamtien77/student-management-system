# Mô-đun Xử lý File (File Handler)
# Cung cấp các hàm tiện ích để đọc/ghi dữ liệu vào file .txt
# Sử dụng ghi nguyên tử (file tạm + đổi tên) để tránh hỏng dữ liệu
# Tất cả dữ liệu được lưu dưới dạng bản ghi phân cách bởi ký tự '|'

import os

# Đường dẫn tới thư mục data nằm cùng cấp với thư mục Source
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _path(filename):
    # Trả về đường dẫn đầy đủ tới file dữ liệu trong thư mục data
    return os.path.join(DATA_DIR, filename)


def read_all_lines(filename):
    # Đọc tất cả dòng không rỗng từ file, trả về danh sách chuỗi
    fp = _path(filename)
    try:
        if not os.path.exists(fp):
            return []
        with open(fp, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except Exception as e:
        print(f"[FileHandler] Read error {filename}: {e}")
        return []


def write_all_lines(filename, lines):
    # Ghi danh sách dòng vào file (ghi đè toàn bộ)
    # Sử dụng file tạm (.tmp) rồi đổi tên để đảm bảo tính nguyên tử
    fp = _path(filename)
    tmp = fp + ".tmp"
    try:
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip():
                    f.write(line.strip() + "\n")
            f.flush()
            os.fsync(f.fileno())
        # Thay thế file cũ bằng file mới
        if os.path.exists(fp):
            os.remove(fp)
        os.rename(tmp, fp)
        return True
    except Exception as e:
        print(f"[FileHandler] Write error {filename}: {e}")
        if os.path.exists(tmp):
            os.remove(tmp)
        return False


def append_line(filename, line):
    # Thêm một dòng mới vào cuối file
    fp = _path(filename)
    try:
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "a", encoding="utf-8") as f:
            f.write(line.strip() + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception as e:
        print(f"[FileHandler] Append error {filename}: {e}")
        return False


def read_records(filename, delim="|"):
    # Đọc tất cả bản ghi từ file, mỗi dòng tách thành danh sách trường
    return [[c.strip() for c in l.split(delim)] for l in read_all_lines(filename)]


def write_records(filename, records, delim="|"):
    # Ghi danh sách bản ghi vào file (ghi đè)
    return write_all_lines(filename, [delim.join(str(c) for c in r) for r in records])


def find_record(filename, idx, value, delim="|"):
    # Tìm bản ghi đầu tiên có trường tại vị trí idx khớp với value
    for r in read_records(filename, delim):
        if len(r) > idx and r[idx] == value.strip():
            return r
    return None


def find_all_records(filename, idx, value, delim="|"):
    # Tìm tất cả bản ghi có trường tại vị trí idx khớp với value
    return [r for r in read_records(filename, delim) if len(r) > idx and r[idx] == value.strip()]


def update_record(filename, key_idx, key_val, new_record, delim="|"):
    # Cập nhật bản ghi có khóa tại vị trí key_idx bằng giá trị key_val
    records = read_records(filename, delim)
    for i, r in enumerate(records):
        if len(r) > key_idx and r[key_idx] == key_val.strip():
            records[i] = new_record
            return write_records(filename, records, delim)
    return False


def delete_record(filename, key_idx, key_val, delim="|"):
    # Xóa bản ghi có khóa tại vị trí key_idx bằng giá trị key_val
    records = read_records(filename, delim)
    new = [r for r in records if not (len(r) > key_idx and r[key_idx] == key_val.strip())]
    if len(new) < len(records):
        return write_records(filename, new, delim)
    return False
