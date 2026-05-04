from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class TrangThaiDonHang(Enum):
    CHO_TIEP_NHAN = "Chờ tiếp nhận"
    DANG_XU_LY = "Đang xử lý"
    CHO_LINH_KIEN = "Chờ linh kiện"
    DANG_SUA_CHUA = "Đang sửa chữa"
    HOAN_THANH = "Hoàn thành"
    DA_GIAO = "Đã giao"
    HUY = "Hủy"

class TrangThaiThanhToan(Enum):
    CHUA_THANH_TOAN = "Chưa thanh toán"
    DA_DAT_COC = "Đã đặt cọc"
    DA_THANH_TOAN = "Đã thanh toán"

class LoaiThietBi(Enum):
    LAPTOP = "Laptop"
    PC_DESKTOP = "PC Desktop"
    MACBOOK = "Macbook"
    MAY_IN = "Máy in"
    MAN_HINH = "Màn hình"
    KHAC = "Khác"

class KhachHang(db.Model):
    __tablename__ = 'khach_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100))
    dia_chi = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quan hệ
    don_hang = db.relationship('DonHang', backref='khach_hang', lazy=True)
    
    def __repr__(self):
        return f'<KhachHang {self.ho_ten}>'

class DichVu(db.Model):
    __tablename__ = 'dich_vu'
    
    id = db.Column(db.Integer, primary_key=True)
    ten_dich_vu = db.Column(db.String(100), nullable=False)
    mo_ta = db.Column(db.Text)
    gia_ban = db.Column(db.Float, default=0)
    thoi_gian_bao_hanh = db.Column(db.Integer)  # số tháng
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quan hệ
    chi_tiet_don_hang = db.relationship('ChiTietDonHang', backref='dich_vu', lazy=True)
    
    def __repr__(self):
        return f'<DichVu {self.ten_dich_vu}>'

class LinhKien(db.Model):
    __tablename__ = 'linh_kien'
    
    id = db.Column(db.Integer, primary_key=True)
    ten_linh_kien = db.Column(db.String(100), nullable=False)
    ma_linh_kien = db.Column(db.String(50), unique=True)
    so_luong_ton = db.Column(db.Integer, default=0)
    gia_nhap = db.Column(db.Float)
    gia_ban = db.Column(db.Float)
    nha_cung_cap = db.Column(db.String(100))
    thong_so_ky_thuat = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Quan hệ
    chi_tiet_linh_kien = db.relationship('ChiTietLinhKien', backref='linh_kien', lazy=True)
    
    def __repr__(self):
        return f'<LinhKien {self.ten_linh_kien}>'

class DonHang(db.Model):
    __tablename__ = 'don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_don_hang = db.Column(db.String(20), unique=True, nullable=False)
    khach_hang_id = db.Column(db.Integer, db.ForeignKey('khach_hang.id'), nullable=False)
    
    # Thông tin thiết bị
    ten_thiet_bi = db.Column(db.String(100), nullable=False)
    loai_thiet_bi = db.Column(db.Enum(LoaiThietBi), nullable=False)
    nhan_hieu = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    mat_khau = db.Column(db.String(100))  # mật khẩu máy tính
    
    # Thông tin sửa chữa
    mo_ta_loi = db.Column(db.Text, nullable=False)
    trang_thai = db.Column(db.Enum(TrangThaiDonHang), default=TrangThaiDonHang.CHO_TIEP_NHAN)
    trang_thai_thanh_toan = db.Column(db.Enum(TrangThaiThanhToan), default=TrangThaiThanhToan.CHUA_THANH_TOAN)
    
    # Chi phí
    tong_tien = db.Column(db.Float, default=0)
    tien_dat_coc = db.Column(db.Float, default=0)
    
    # Thời gian
    ngay_tiep_nhan = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_hoan_thanh = db.Column(db.DateTime)
    ngay_giao_hang = db.Column(db.DateTime)
    
    # Ghi chú
    ghi_chu_nhan_vien = db.Column(db.Text)
    ghi_chu_khach_hang = db.Column(db.Text)
    
    # Quan hệ
    chi_tiet_don_hang = db.relationship('ChiTietDonHang', backref='don_hang', lazy=True)
    linh_kien_su_dung = db.relationship('ChiTietLinhKien', backref='don_hang', lazy=True)
    
    def __repr__(self):
        return f'<DonHang {self.ma_don_hang}>'

class ChiTietDonHang(db.Model):
    __tablename__ = 'chi_tiet_don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    dich_vu_id = db.Column(db.Integer, db.ForeignKey('dich_vu.id'), nullable=False)
    so_luong = db.Column(db.Integer, default=1)
    don_gia = db.Column(db.Float, nullable=False)
    thanh_tien = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<ChiTietDonHang {self.id}>'

class ChiTietLinhKien(db.Model):
    __tablename__ = 'chi_tiet_linh_kien'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    linh_kien_id = db.Column(db.Integer, db.ForeignKey('linh_kien.id'), nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    don_gia = db.Column(db.Float, nullable=False)
    thanh_tien = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<ChiTietLinhKien {self.id}>'

class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    
    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    tai_khoan = db.Column(db.String(50), unique=True, nullable=False)
    mat_khau = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    so_dien_thoai = db.Column(db.String(20))
    vai_tro = db.Column(db.String(20), default='nhan_vien')  # admin, nhan_vien
    trang_thai = db.Column(db.String(20), default='hoat_dong')  # hoat_dong, nghi_viec
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Flask-Login yêu cầu các thuộc tính này
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def is_authenticated(self):
        return True
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<NhanVien {self.ho_ten}>'
