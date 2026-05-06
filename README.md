# 🛠️ PC Care - Hệ thống Quản lý Dịch vụ Sửa chữa Điện tử Chuyên nghiệp

![GitHub repo size](https://img.shields.io/github/repo-size/TrinhDangKhanh/dich-vu-sua-do-dien-tu?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/TrinhDangKhanh/dich-vu-sua-do-dien-tu?color=red&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Hệ thống quản lý dịch vụ sửa chữa thiết bị điện tử chuyên nghiệp với database cải tiến, giao diện hiện đại và đầy đủ tính năng. Phát triển bằng Python Flask với UI/UX được thiết kế lại hoàn toàn, responsive và thân thiện với người dùng.

## ✨ What's New (v2.0)

- 🎨 **Modern UI Redesign**: Giao diện được thiết kế lại hoàn toàn với gradient headers, hover effects
- 📱 **Enhanced Mobile Experience**: Responsive design tối ưu cho mọi thiết bị
- 🔧 **Improved Forms**: Form tạo đơn hàng, dịch vụ, linh kiện với validation và loading states
- 🎯 **Better UX**: Micro-interactions, smooth transitions, intuitive navigation
- 🛡️ **Enhanced Security**: Cải thiện validation và error handling
- 📊 **Updated Dashboard**: Thống kê real-time với visual improvements

---

## 🌟 Tính năng chính

### 📋 Quản lý Đơn hàng Nâng cao
- **Tiếp nhận thiết bị:** Ghi nhận thông tin khách hàng và thiết bị đầy đủ
- **Theo dõi trạng thái:** 8 trạng thái từ Chờ tiếp nhận đến Đã giao
- **Quản lý nhân viên:** Giao đơn hàng cho nhân viên cụ thể
- **Lịch sử thay đổi:** Tracking toàn bộ lịch sử cập nhật đơn hàng
- **Đánh giá khách hàng:** Hệ thống đánh giá 1-5 sao

### 👥 Quản lý Khách hàng Chuyên nghiệp
- **Hồ sơ khách hàng:** Mã khách hàng tự động (KH001, KH002...)
- **Phân loại:** Cá nhân/Doanh nghiệp với thông tin công ty
- **Tìm kiếm nhanh:** Theo tên, SĐT, email, mã khách hàng
- **Lịch sử:** Đơn hàng và dịch vụ đã sử dụng

### 🔧 Quản lý Dịch vụ Đa dạng
- **Mã dịch vụ:** Tự động (DV001, DV002...)
- **Phân loại:** Sửa chữa/Bảo trì/Cập nhật
- **Bảng giá:** Giá bán và thời gian bảo hành
- **Trạng thái:** Kích hoạt/Vô hiệu dịch vụ

### 📦 Quản lý Kho linh kiện Thông minh
- **Mã linh kiện:** Tự động (LK001, LK002...)
- **Tồn kho:** Số lượng tồn và tồn kho tối thiểu
- **Nhập kho:** Quản lý phiếu nhập và nhà cung cấp
- **Phân loại:** RAM, SSD, Màn hình, Pin, Sạc, Phụ kiện

### 📊 Báo cáo & Thống kê Hiện đại
- **Biểu đồ Thu Chi:** Chart.js với gradient đẹp mắt
- **Thống kê đa dạng:** Doanh thu, đơn hàng, khách hàng, dịch vụ
- **Bộ lọc:** Theo tháng/năm linh hoạt
- **Xuất báo cáo:** Excel, PDF, In, Gửi email

### 🔐 Hệ thống Phân quyền
- **4 vai trò:** Admin, Quản lý, Nhân viên, Kỹ thuật
- **Bảo mật:** Mật khẩu mã hóa với Werkzeug
- **Lịch sử hoạt động:** Log tất cả hành động người dùng
- **Cấu hình hệ thống:** Quản lý cài đặt ứng dụng

### 📱 Giao diện Responsive & Modern
- **Modern Design:** Custom CSS với gradient headers và hover effects
- **Mobile First:** Tối ưu hoàn toàn cho mobile và tablet
- **Dark Mode Ready:** Chuẩn bị cho dark mode
- **Fast Loading:** Tối ưu hóa performance
- **Micro-interactions:** Smooth transitions và animations
- **Form Validation:** Real-time validation với user-friendly error messages

### 🎨 UI/UX Improvements (v2.0)
- **Gradient Headers:** Mỗi module có màu sắc riêng (Blue cho đơn hàng, Green cho dịch vụ, Orange cho linh kiện)
- **Enhanced Forms:** Modern input fields với focus states và loading indicators
- **Better Navigation:** Intuitive menu structure với breadcrumbs
- **Responsive Grid:** Adaptive layout cho mọi screen size
- **Loading States:** Professional loading animations
- **Success/Error Messages:** Beautiful toast notifications

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ | Phiên bản |
| :--- | :--- | :--- |
| **Backend** | Python Flask | 2.3.3 |
| **Database ORM** | SQLAlchemy | 1.4.53 |
| **Authentication** | Flask-Login | 0.6.3 |
| **Security** | Werkzeug | 2.3.7 |
| **Database** | SQLite | Mặc định |
| **Charts** | Chart.js | 3.9.1 |
| **Frontend** | Custom CSS | Tailwind-style |
| **Templates** | Jinja2 | 3.1.2 |

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

### 2. Tạo đơn hàng mới (Enhanced v2.0)
1. Click "Tạo đơn hàng mới" từ dashboard
2. Nhập thông tin khách hàng (tự động tạo nếu chưa tồn tại)
3. Nhập thông tin thiết bị với validation real-time
4. Mô tả chi tiết lỗi
5. Lưu đơn hàng với loading animation

### 3. Cập nhật trạng thái đơn hàng
1. Vào "Danh sách đơn hàng"
2. Click nút "Cập nhật trạng thái"
3. Chọn trạng thái mới với smooth transitions
4. Lưu thay đổi với success notifications

### 4. Quản lý dịch vụ (Modern UI)
1. Vào mục "Dịch vụ" → "Tạo dịch vụ mới"
2. Điền form với gradient green header
3. Thêm loại dịch vụ, giá, thời gian bảo hành
4. Xem real-time validation

### 5. Quản lý linh kiện (Modern UI)
1. Vào mục "Linh kiện" → "Tạo linh kiện mới"
2. Điền form với gradient orange header
3. Quản lý tồn kho, giá nhập/xuất
4. Validation cho giá bán > giá nhập

### 6. Xem báo cáo
1. Vào mục "Báo cáo"
2. Chọn tháng/năm cần xem
3. Xem thống kê doanh thu với improved charts
4. Export báo cáo với enhanced UI

---

## 📁 Cấu trúc dự án

```
chámocmaytih/
├── app.py                      # Ứng dụng chính Flask
├── database_improved.py        # Models database cải tiến (12 bảng)
├── database.py                 # Models database cũ
├── config.py                   # Cấu hình hệ thống
├── requirements.txt            # Dependencies
├── check_db.py                 # Script kiểm tra database
├── templates/                  # HTML templates
│   ├── base.html              # Template chính
│   ├── dashboard.html          # Dashboard thống kê
│   ├── dang_nhap.html          # Đăng nhập
│   ├── don_hang/               # Quản lý đơn hàng
│   │   ├── danh_sach.html
│   │   ├── tao_moi.html
│   │   └── chi_tiet.html
│   ├── khach_hang/             # Quản lý khách hàng
│   │   └── danh_sach.html
│   ├── dich_vu/                # Quản lý dịch vụ
│   │   ├── danh_sach.html
│   │   └── tao_moi.html
│   ├── linh_kien/              # Quản lý linh kiện
│   │   ├── danh_sach.html
│   │   └── tao_moi.html
│   └── bao_cao/                # Báo cáo & thống kê
│       └── index.html
├── static/                     # Static files
│   ├── css/style.css          # Custom CSS
│   └── js/script.js           # JavaScript
├── instance/                   # Database files
│   └── pc_care.db             # SQLite database
└── __pycache__/                # Python cache
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