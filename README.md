# STUDENT MANAGEMENT SYSTEM

## MO TA DU AN

He thong quan ly sinh vien duoc xay dung nham phuc vu cong tac quan ly thong tin sinh vien, giang vien, mon hoc va diem so tai cac truong dai hoc, cao dang. He thong ho tro cac chuc nang co ban nhu quan ly ho so sinh vien, dang ky mon hoc, nhap diem va xem ket qua hoc tap.

---

## CONG NGHE SU DUNG

### Backend
- Ngon ngu: Python 3.x
- Framework: Flask 2.3.0
- ORM: Flask-SQLAlchemy 3.0.0
- Authentication: Flask-JWT-Extended 4.5.0
- Database: MySQL (PyMySQL)
- Bao mat: bcrypt, Flask-Limiter, Flask-Talisman

### Frontend
- HTML5, CSS3, JavaScript
- Framework CSS: Bootstrap 5
- Thu vien: jQuery, DataTables

### Database
- MySQL 8.0

---

## CAU TRUC THU MUC

```
student-management-system/
│
├── backend/                          # Backend API
│   ├── app/
│   │   ├── __init__.py              # Khoi tao Flask app
│   │   ├── config.py                # Cau hinh ung dung
│   │   │
│   │   ├── models/                  # Cac model database
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # Tai khoan dang nhap
│   │   │   ├── student.py           # Sinh vien
│   │   │   ├── teacher.py           # Giang vien
│   │   │   ├── department.py        # Khoa
│   │   │   ├── major.py             # Nganh hoc
│   │   │   ├── class_model.py       # Lop hoc
│   │   │   ├── course.py            # Mon hoc
│   │   │   ├── semester.py          # Hoc ky
│   │   │   ├── enrollment.py        # Dang ky mon hoc
│   │   │   ├── grade.py             # Diem
│   │   │   ├── activity_log.py      # Nhat ky hoat dong
│   │   │   └── token_blacklist.py   # Quan ly token
│   │   │
│   │   ├── routes/                  # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # Dang nhap/Dang xuat
│   │   │   ├── student.py           # API sinh vien
│   │   │   ├── teacher.py           # API giang vien
│   │   │   ├── course.py            # API mon hoc
│   │   │   ├── class_route.py       # API lop hoc
│   │   │   ├── department.py        # API khoa
│   │   │   ├── major.py             # API nganh
│   │   │   ├── enrollment.py        # API dang ky mon
│   │   │   └── grade.py             # API diem
│   │   │
│   │   ├── middleware/              # Middleware
│   │   │   ├── __init__.py
│   │   │   ├── rate_limiter.py      # Gioi han request
│   │   │   ├── cors.py              # Cau hinh CORS
│   │   │   └── error_handler.py     # Xu ly loi
│   │   │
│   │   └── utils/                   # Tien ich
│   │       ├── __init__.py
│   │       ├── auth.py              # JWT authentication
│   │       ├── helpers.py           # Ham ho tro
│   │       ├── security.py          # Bao mat
│   │       └── validators.py        # Kiem tra du lieu
│   │
│   ├── run.py                       # Chay ung dung
│   ├── requirements.txt             # Thu vien can cai
│   └── .env.example                 # Mau file cau hinh
│
├── frontend/                        # Giao dien nguoi dung
│   ├── index.html                   # Trang chu
│   ├── css/
│   │   └── style.css               # Style chinh
│   ├── js/
│   │   ├── app.js                  # Main JavaScript
│   │   ├── api.js                  # Goi API
│   │   ├── auth.js                 # Xu ly dang nhap
│   │   ├── student.js              # Quan ly sinh vien
│   │   ├── teacher.js              # Quan ly giang vien
│   │   ├── course.js               # Quan ly mon hoc
│   │   └── grade.js                # Quan ly diem
│   └── pages/
│       ├── login.html              # Trang dang nhap
│       ├── dashboard.html          # Trang tong quan
│       ├── students.html           # Quan ly sinh vien
│       ├── teachers.html           # Quan ly giang vien
│       ├── courses.html            # Quan ly mon hoc
│       ├── classes.html            # Quan ly lop
│       ├── departments.html        # Quan ly khoa
│       ├── majors.html             # Quan ly nganh
│       ├── enrollment.html         # Dang ky mon hoc
│       ├── grades.html             # Nhap diem
│       └── transcript.html         # Xem bang diem
│
├── database/                        # Database scripts
│   ├── schema.sql                  # Cau truc database
│   └── seed.sql                    # Du lieu mau
│
└── README.md                        # Tai lieu huong dan
```

---

## CHUC NANG CHI TIET

### 1. Quan ly tai khoan
- Dang nhap/Dang xuat
- Phan quyen: Admin, Giang vien, Sinh vien
- Doi mat khau
- Khoa tai khoan sau 5 lan dang nhap sai

### 2. Quan ly sinh vien
- Xem danh sach sinh vien
- Them sinh vien moi
- Sua thong tin sinh vien
- Xoa sinh vien
- Tim kiem theo ten, ma sinh vien
- Loc theo lop, khoa, nganh

### 3. Quan ly giang vien
- Xem danh sach giang vien
- Them/Sua/Xoa giang vien
- Phan cong giang vien theo khoa

### 4. Quan ly mon hoc
- Xem danh sach mon hoc
- Them/Sua/Xoa mon hoc
- Quan ly so tin chi

### 5. Quan ly lop hoc
- Tao lop hoc moi
- Gan sinh vien vao lop
- Phan cong giao vien chu nhiem

### 6. Quan ly khoa/nganh
- Them/Sua/Xoa khoa
- Them/Sua/Xoa nganh thuoc khoa

### 7. Dang ky mon hoc
- Xem mon hoc co the dang ky
- Dang ky mon hoc
- Huy dang ky

### 8. Quan ly diem
- Nhap diem (diem qua trinh, giua ky, cuoi ky)
- Tinh diem tong ket
- Xem bang diem theo hoc ky
- Tinh GPA

---

## TINH NANG BAO MAT

### Authentication
- Dang nhap bang JWT Token
- Access Token het han sau 1 gio
- Refresh Token het han sau 7 ngay
- Thu hoi token khi dang xuat

### Authorization
- Phan quyen theo role (Admin, Teacher, Student)
- Kiem tra quyen truoc khi thuc hien thao tac

### Password Security
- Ma hoa mat khau bang bcrypt
- Yeu cau mat khau toi thieu 8 ky tu
- Khoa tai khoan sau 5 lan nhap sai

### Input Validation
- Kiem tra dinh dang email
- Kiem tra so dien thoai
- Loc ky tu dac biet (chong XSS)
- Su dung ORM (chong SQL Injection)

### Rate Limiting
- Gioi han 5 lan dang nhap trong 5 phut
- Gioi han 100 request API trong 1 gio

### Logging
- Ghi log moi hoat dong cua nguoi dung
- Luu thong tin IP, thiet bi
- Theo doi dang nhap bat thuong

---

## HUONG DAN CAI DAT

### Yeu cau he thong
- Python 3.8 tro len
- MySQL 8.0 tro len
- Node.js (tuy chon, cho Live Server)

### Buoc 1: Clone du an
```bash
git clone https://github.com/username/student-management-system.git
cd student-management-system
```

### Buoc 2: Tao database
```sql
CREATE DATABASE student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Chay file schema.sql de tao cac bang:
```bash
mysql -u root -p student_db < database/schema.sql
```

### Buoc 3: Cau hinh Backend
```bash
cd backend

# Tao moi truong ao
python -m venv venv

# Kich hoat moi truong ao
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cai dat thu vien
pip install -r requirements.txt

# Tao file .env tu mau
copy .env.example .env
# Sau do sua cac thong so trong file .env
```

### Buoc 4: Cau hinh file .env
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=mysql+pymysql://root:password@localhost/student_db
```

### Buoc 5: Chay Backend
```bash
python run.py
```
Server se chay tai: http://localhost:5000

### Buoc 6: Chay Frontend
Mo file frontend/index.html bang trinh duyet
Hoac su dung Live Server trong VS Code

---

## API ENDPOINTS

### Authentication
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| POST | /api/auth/login | Dang nhap |
| POST | /api/auth/logout | Dang xuat |
| POST | /api/auth/refresh | Lam moi token |
| GET | /api/auth/me | Lay thong tin user |
| PUT | /api/auth/change-password | Doi mat khau |

### Students
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/students | Danh sach sinh vien |
| GET | /api/students/:id | Chi tiet sinh vien |
| POST | /api/students | Them sinh vien |
| PUT | /api/students/:id | Sua sinh vien |
| DELETE | /api/students/:id | Xoa sinh vien |
| GET | /api/students/:id/grades | Xem diem |

### Teachers
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/teachers | Danh sach giang vien |
| GET | /api/teachers/:id | Chi tiet giang vien |
| POST | /api/teachers | Them giang vien |
| PUT | /api/teachers/:id | Sua giang vien |
| DELETE | /api/teachers/:id | Xoa giang vien |

### Courses
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/courses | Danh sach mon hoc |
| POST | /api/courses | Them mon hoc |
| PUT | /api/courses/:id | Sua mon hoc |
| DELETE | /api/courses/:id | Xoa mon hoc |

### Classes
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/classes | Danh sach lop |
| GET | /api/classes/:id/students | Sinh vien trong lop |
| POST | /api/classes | Them lop |
| PUT | /api/classes/:id | Sua lop |
| DELETE | /api/classes/:id | Xoa lop |

### Enrollments
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/enrollments | Danh sach dang ky |
| POST | /api/enrollments | Dang ky mon |
| DELETE | /api/enrollments/:id | Huy dang ky |

### Grades
| Method | Endpoint | Mo ta |
|--------|----------|-------|
| GET | /api/grades | Danh sach diem |
| POST | /api/grades | Nhap diem |
| PUT | /api/grades/:id | Sua diem |

---

## CO SO DU LIEU

### Danh sach cac bang

1. **users** - Tai khoan dang nhap
2. **students** - Thong tin sinh vien
3. **teachers** - Thong tin giang vien
4. **departments** - Khoa
5. **majors** - Nganh hoc
6. **classes** - Lop hoc
7. **courses** - Mon hoc
8. **semesters** - Hoc ky
9. **enrollments** - Dang ky mon hoc
10. **grades** - Diem
11. **activity_logs** - Nhat ky hoat dong
12. **token_blacklist** - Token da thu hoi

### So do quan he
```
departments (1) -----> (n) majors
departments (1) -----> (n) teachers
majors (1) -----> (n) classes
classes (1) -----> (n) students
users (1) -----> (1) students/teachers
students (1) -----> (n) enrollments
courses (1) -----> (n) enrollments
enrollments (1) -----> (1) grades
```

---

## TAI KHOAN MAC DINH

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| teacher1 | teacher123 | Teacher |
| student1 | student123 | Student |

---

## TAC GIA

- Ten: [Ten sinh vien]
- MSSV: [Ma so sinh vien]
- Lop: [Ten lop]
- Truong: [Ten truong]

---

## GIAY PHEP

Du an nay duoc phat trien cho muc dich hoc tap.
