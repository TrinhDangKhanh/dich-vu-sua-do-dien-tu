# 🛠️ PC Care - Hệ thống Quản lý Dịch vụ Chăm sóc Máy tính 💻

![GitHub repo size](https://img.shields.io/github/repo-size/TrinhDangKhanh/dich-vu-sua-do-dien-tu?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/TrinhDangKhanh/dich-vu-sua-do-dien-tu?color=red&style=for-the-badge)

Hệ thống quản lý dịch vụ sửa chữa thiết bị điện tử chuyên nghiệp, giúp tối ưu hóa quy trình tiếp nhận, theo dõi và bàn giao thiết bị cho khách hàng. Phát triển bằng Python Flask với giao diện hiện đại và đầy đủ chức năng.

---

## 🌟 Tính năng chính

### 📋 Quản lý Đơn hàng
- **Tiếp nhận thiết bị:** Ghi nhận thông tin khách hàng và thiết bị
- **Theo dõi trạng thái:** Cập nhật tiến trình sửa chữa theo thời gian thực
- **Quản lý lỗi:** Ghi chú chi tiết tình trạng và yêu cầu của khách hàng
- **Lịch sử:** Theo dõi toàn bộ lịch sử sửa chữa của từng khách hàng

### 👥 Quản lý Khách hàng
- **Hồ sơ khách hàng:** Lưu trữ thông tin liên hệ và lịch sử
- **Tìm kiếm:** Tìm kiếm nhanh khách hàng theo tên, SĐT, email
- **Thống kê:** Xem số lượng đơn hàng của từng khách hàng

### � Quản lý Dịch vụ
- **Danh mục dịch vụ:** Quản lý các loại dịch vụ sửa chữa
- **Bảng giá:** Cập nhật giá dịch vụ và thời gian bảo hành
- **Tùy chỉnh:** Thêm/sửa/xóa dịch vụ theo nhu cầu

### 📦 Quản lý Kho linh kiện
- **Tồn kho:** Theo dõi số lượng linh kiện còn lại
- **Nhập/xuất:** Quản lý việc nhập và sử dụng linh kiện
- **Cảnh báo:** Thông báo khi linh kiện sắp hết

### 📊 Báo cáo & Thống kê
- **Doanh thu:** Thống kê doanh thu theo ngày/tháng/năm
- **Hiệu suất:** Báo cáo số lượng đơn hàng hoàn thành
- **Top dịch vụ:** Xem các dịch vụ được sử dụng nhiều nhất
- **Xuất dữ liệu:** Xuất báo cáo ra Excel, PDF

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ | Phiên bản |
| :--- | :--- | :--- |
| **Backend** | Python Flask | 2.3.3 |
| **Database** | SQLAlchemy | 1.4.53 |
| **Frontend** | Bootstrap 5 | 5.3.0 |
| **Authentication** | Flask-Login | 0.6.3 |
| **Security** | Werkzeug | 2.3.7 |
| **Database** | SQLite | Mặc định |

---

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8 trở lên
- 2GB RAM tối thiểu
- 500MB dung lượng ổ cứng

### 2. Cài đặt dự án
```bash
# Clone repository
git clone https://github.com/TrinhDangKhanh/dich-vu-sua-do-dien-tu.git
cd dich-vu-sua-do-dien-tu

# Tạo môi trường ảo (khuyến khích)
python -m venv venv
venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

### 3. Khởi động ứng dụng
```bash
# Chạy ứng dụng
python app.py

# Ứng dụng sẽ khởi động tại: http://127.0.0.1:5000
```

---

## 🔐 Tài khoản mặc định

| Tài khoản | Mật khẩu | Vai trò |
| :--- | :--- | :--- |
| `admin` | `admin123` | Quản trị viên |

---

## � Hướng dẫn sử dụng

### 1. Đăng nhập
- Truy cập http://127.0.0.1:5000
- Đăng nhập với tài khoản admin/admin123

### 2. Tạo đơn hàng mới
1. Click "Tạo đơn hàng mới" từ dashboard
2. Nhập thông tin khách hàng
3. Nhập thông tin thiết bị
4. Mô tả chi tiết lỗi
5. Lưu đơn hàng

### 3. Cập nhật trạng thái đơn hàng
1. Vào "Danh sách đơn hàng"
2. Click nút "Cập nhật trạng thái"
3. Chọn trạng thái mới
4. Lưu thay đổi

### 4. Quản lý dịch vụ
1. Vào mục "Quản lý" → "Dịch vụ"
2. Thêm dịch vụ mới với giá và thời gian bảo hành
3. Sửa hoặc xóa dịch vụ hiện có

### 5. Xem báo cáo
1. Vào mục "Báo cáo"
2. Chọn tháng/năm cần xem
3. Xem thống kê doanh thu và hiệu suất

---

## 📁 Cấu trúc dự án

```
chámocmaytih/
├── app.py                 # Ứng dụng chính
├── database.py           # Models database
├── config.py             # Cấu hình hệ thống
├── requirements.txt      # Dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── dang_nhap.html
│   ├── don_hang/
│   ├── khach_hang/
│   ├── dich_vu/
│   ├── linh_kien/
│   └── bao_cao/
├── static/              # Static files
│   ├── css/style.css
│   ├── js/script.js
│   └── uploads/
└── pc_care.db          # Database SQLite
```

---

## 🔧 Tùy chỉnh cấu hình

### Database
Mặc định sử dụng SQLite. Để chuyển sang MySQL:

```python
# Trong config.py
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/pc_care'
```

### Cấu hình khác
```python
# Thay đổi secret key
SECRET_KEY = 'your-secret-key-here'

# Thay đổi thời gian session
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

# Thay đổi số lượng item mỗi trang
ITEMS_PER_PAGE = 10
```

---

## � Khắc phục sự cố

### 1. Lỗi SQLAlchemy với Python 3.13
```bash
# Sử dụng phiên bản tương thích
pip install SQLAlchemy==1.4.53 Flask-SQLAlchemy==3.0.5
```

### 2. Lỗi import module
```bash
# Kiểm tra cài đặt dependencies
pip install -r requirements.txt --force-reinstall
```

### 3. Database không được tạo
- Database sẽ tự động tạo khi khởi động ứng dụng lần đầu
- Nếu có lỗi, xóa file `pc_care.db` và khởi động lại

---

## 🤝 Đóng góp

1. Fork project
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 Giấy phép

Dự án này được cấp phép theo MIT License - xem file [LICENSE](LICENSE) để biết chi tiết.

---

## 👥 Tác giả

**Đặng Khánh** - *Initial work* - [TrinhDangKhanh](https://github.com/TrinhDangKhanh)

---

## 📞 Hỗ trợ

Nếu bạn có câu hỏi hoặc cần hỗ trợ, vui lòng:
- Liên hệ: admin@pccare.com
- Gửi issue trên GitHub
- Xem tài liệu tại: https://docs.pccare.com

---

⭐ Nếu dự án này hữu ích, hãy cho tôi một star trên GitHub!