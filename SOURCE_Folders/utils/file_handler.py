"""
utils/file_handler.py
mo-dun duy nhat duoc phep doc/ghi file .txt trong thu muc data/
ho tro 2 dinh dang dong:
  - plain: "gia_tri_1|gia_tri_2|..."          → tra ve list[str]
  - dict : "key1=val1|key2=val2|..."          → tra ve list[dict]
ham write_file tu dong phat hien kieu du lieu de ghi dung dinh dang
"""

import os

# thu muc goc chua cac file data, tinh tuong doi tu vi tri main.py
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resolve_path(relative_path: str) -> str:
    """ghep duong dan tuong doi voi thu muc goc cua du an"""
    return os.path.join(_BASE_DIR, relative_path)


def _ensure_file(path: str):
    """tao file trong neu chua ton tai, tranh loi FileNotFoundError"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        open(path, "w", encoding="utf-8").close()


# ---------------------------------------------------------------------------
# DOC FILE
# ---------------------------------------------------------------------------

def read_file(relative_path: str):
    """
    doc file .txt va tra ve du lieu da duoc parse:
      - neu dong dau tien chua dau '=' → dinh dang dict  → list[dict]
      - nguoc lai                       → dinh dang plain → list[str]
    """
    path = _resolve_path(relative_path)
    _ensure_file(path)

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n").rstrip("\r") for line in f]

    # loai dong trong
    lines = [l for l in lines if l.strip()]
    if not lines:
        return []

    # phat hien dinh dang: neu co dau '=' trong dong dau → dict format
    if "=" in lines[0]:
        result = []
        for line in lines:
            record = {}
            for part in line.split("|"):
                if "=" in part:
                    key, _, value = part.partition("=")
                    record[key.strip()] = value.strip()
            if record:
                result.append(record)
        return result
    else:
        # tra ve danh sach cac dong nguyen ban (plain format)
        return lines


# ---------------------------------------------------------------------------
# GHI FILE
# ---------------------------------------------------------------------------

def write_file(relative_path: str, data: list):
    """
    ghi danh sach data xuong file .txt:
      - neu phan tu la dict → ghi theo dinh dang "key=val|key=val|..."
      - neu phan tu la str  → ghi nguyen ban
    """
    path = _resolve_path(relative_path)
    _ensure_file(path)

    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            if isinstance(item, dict):
                # ghep cac cap key=value bang dau |
                line = "|".join(f"{k}={v}" for k, v in item.items())
            else:
                line = str(item)
            f.write(line + "\n")
