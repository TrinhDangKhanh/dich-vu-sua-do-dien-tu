from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

# Enums
class TrangThaiDonHang(Enum):
    CHO_TIEP_NHAN = "Chờ tiếp nhận"
    DANG_XU_LY = "Đang xử lý"
    CHO_LINH_KIEN = "Chờ linh kiện"
    DANG_SUA_CHUA = "Đang sửa chữa"
    CHO_THANH_TOAN = "Chờ thanh toán"
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
    DIEN_THOAI = "Điện thoại"
    MAY_TINH_BANG = "Máy tính bảng"
    KHAC = "Khác"

class LoaiBaoCao(Enum):
    DOANH_THU = "Doanh thu"
    DON_HANG = "Đơn hàng"
    KHACH_HANG = "Khách hàng"
    DICH_VU = "Dịch vụ"
class PhanQuyen(Enum):
    ADMIN = "admin"
    QUAN_LY = "quan_ly"
    NHAN_VIEN = "nhan_vien"
    KY_THUAT = "ky_thuat"

# Models
class NhanVien(db.Model):
    __tablename__ = 'nhan_vien'
    
    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    tai_khoan = db.Column(db.String(50), unique=True, nullable=False, index=True)
    mat_khau = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    so_dien_thoai = db.Column(db.String(20), unique=True, index=True)
    vai_tro = db.Column(db.Enum(PhanQuyen), default=PhanQuyen.NHAN_VIEN)
    trang_thai = db.Column(db.String(20), default='hoat_dong')
    ngay_sinh = db.Column(db.Date)
    dia_chi = db.Column(db.Text)
    luong_co_ban = db.Column(db.Float)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Flask-Login requirements
    is_active = db.Column(db.Boolean, default=True)
    
    @property
    def is_authenticated(self):
        return True
    
    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.mat_khau = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.mat_khau, password)
    
    def __repr__(self):
        return f'<NhanVien {self.ho_ten}>'

class KhachHang(db.Model):
    __tablename__ = 'khach_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_khach_hang = db.Column(db.String(20), unique=True, nullable=False, index=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=False, unique=True, index=True)
    email = db.Column(db.String(100), index=True)
    dia_chi = db.Column(db.Text)
    ngay_sinh = db.Column(db.Date)
    gioi_tinh = db.Column(db.String(10))
    cong_ty = db.Column(db.String(100))
    ma_so_thue = db.Column(db.String(50))
    loai_khach_hang = db.Column(db.String(50), default='ca_nhan')  # ca_nhan, doanh_nghiep
    ghi_chu = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    don_hang = db.relationship('DonHang', backref='khach_hang', lazy='dynamic')
    
    def __repr__(self):
        return f'<KhachHang {self.ho_ten}>'

class DichVu(db.Model):
    __tablename__ = 'dich_vu'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_dich_vu = db.Column(db.String(20), unique=True, nullable=False, index=True)
    ten_dich_vu = db.Column(db.String(100), nullable=False)
    mo_ta = db.Column(db.Text)
    gia_ban = db.Column(db.Float, nullable=False)
    thoi_gian_bao_hanh = db.Column(db.Integer)  # số tháng
    loai_dich_vu = db.Column(db.String(50))  # sua_chua, bao_trih, cap_nhat
    trang_thai = db.Column(db.String(20), default='hoat_dong')
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chi_tiet_don_hang = db.relationship('ChiTietDonHang', backref='dich_vu', lazy='dynamic')
    
    def __repr__(self):
        return f'<DichVu {self.ten_dich_vu}>'

class LinhKien(db.Model):
    __tablename__ = 'linh_kien'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_linh_kien = db.Column(db.String(50), unique=True, nullable=False, index=True)
    ten_linh_kien = db.Column(db.String(100), nullable=False)
    mo_ta = db.Column(db.Text)
    so_luong_ton = db.Column(db.Integer, default=0)
    so_luong_toi_thieu = db.Column(db.Integer, default=10)
    gia_nhap = db.Column(db.Float, nullable=False)
    gia_ban = db.Column(db.Float, nullable=False)
    nha_cung_cap = db.Column(db.String(100))
    thong_so_ky_thuat = db.Column(db.Text)
    loai_linh_kien = db.Column(db.String(50))
    trang_thai = db.Column(db.String(20), default='hoat_dong')
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chi_tiet_linh_kien = db.relationship('ChiTietLinhKien', backref='linh_kien', lazy='dynamic')
    nhap_kho = db.relationship('NhapKho', backref='linh_kien', lazy='dynamic')
    
    def __repr__(self):
        return f'<LinhKien {self.ten_linh_kien}>'

class DonHang(db.Model):
    __tablename__ = 'don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_don_hang = db.Column(db.String(20), unique=True, nullable=False, index=True)
    khach_hang_id = db.Column(db.Integer, db.ForeignKey('khach_hang.id'), nullable=False)
    nhan_vien_id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'))
    
    # Thông tin thiết bị
    ten_thiet_bi = db.Column(db.String(100), nullable=False)
    loai_thiet_bi = db.Column(db.Enum(LoaiThietBi), nullable=False)
    nhan_hieu = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial_number = db.Column(db.String(100), unique=True, index=True)
    mat_khau = db.Column(db.String(100))  # encrypted
    
    # Thông tin sửa chữa
    mo_ta_loi = db.Column(db.Text, nullable=False)
    mo_ta_bao_hanh = db.Column(db.Text)
    trang_thai = db.Column(db.Enum(TrangThaiDonHang), default=TrangThaiDonHang.CHO_TIEP_NHAN)
    trang_thai_thanh_toan = db.Column(db.Enum(TrangThaiThanhToan), default=TrangThaiThanhToan.CHUA_THANH_TOAN)
    
    # Chi phí
    tong_tien = db.Column(db.Float, default=0)
    tien_dat_coc = db.Column(db.Float, default=0)
    chi_phi_khac = db.Column(db.Float, default=0)
    
    # Thời gian
    ngay_tiep_nhan = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_bat_dau_sua = db.Column(db.DateTime)
    ngay_hoan_thanh = db.Column(db.DateTime)
    ngay_giao_hang = db.Column(db.DateTime)
    ngay_hen_tra = db.Column(db.DateTime)
    
    # Ghi chú
    ghi_chu_nhan_vien = db.Column(db.Text)
    ghi_chu_khach_hang = db.Column(db.Text)
    danh_gia_khach_hang = db.Column(db.Integer, default=5)  # 1-5 sao
    
    # Metadata
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chi_tiet_don_hang = db.relationship('ChiTietDonHang', backref='don_hang', lazy='dynamic', cascade='all, delete-orphan')
    linh_kien_su_dung = db.relationship('ChiTietLinhKien', backref='don_hang', lazy='dynamic', cascade='all, delete-orphan')
    lich_su = db.relationship('LichSuDonHang', backref='don_hang', lazy='dynamic')
    
    def __repr__(self):
        return f'<DonHang {self.ma_don_hang}>'

class ChiTietDonHang(db.Model):
    __tablename__ = 'chi_tiet_don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    dich_vu_id = db.Column(db.Integer, db.ForeignKey('dich_vu.id'), nullable=False)
    so_luong = db.Column(db.Integer, default=1)
    don_gia = db.Column(db.Float, nullable=False)
    giam_gia = db.Column(db.Float, default=0)
    thanh_tien = db.Column(db.Float, nullable=False)
    ghi_chu = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    loai = db.Column(db.String(20), default='thay_moi')  # thay_moi, sua_chua
    ghi_chu = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChiTietLinhKien {self.id}>'

class NhapKho(db.Model):
    __tablename__ = 'nhap_kho'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_phieu_nhap = db.Column(db.String(20), unique=True, nullable=False, index=True)
    linh_kien_id = db.Column(db.Integer, db.ForeignKey('linh_kien.id'), nullable=False)
    nhan_vien_id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    don_gia = db.Column(db.Float, nullable=False)
    thanh_tien = db.Column(db.Float, nullable=False)
    nha_cung_cap = db.Column(db.String(100))
    ngay_nhap = db.Column(db.DateTime, default=datetime.utcnow)
    ghi_chu = db.Column(db.Text)
    
    def __repr__(self):
        return f'<NhapKho {self.ma_phieu_nhap}>'

class LichSuDonHang(db.Model):
    __tablename__ = 'lich_su_don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    nhan_vien_id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), nullable=False)
    hanh_dong = db.Column(db.String(100), nullable=False)  # tao_moi, cap_nhat_trang_thai, etc.
    trang_thai_cu = db.Column(db.String(50))
    trang_thai_moi = db.Column(db.String(50))
    ghi_chu = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LichSuDonHang {self.id}>'

class BaoCao(db.Model):
    __tablename__ = 'bao_cao'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_bao_cao = db.Column(db.String(20), unique=True, nullable=False, index=True)
    loai_bao_cao = db.Column(db.Enum(LoaiBaoCao), nullable=False)
    ten_bao_cao = db.Column(db.String(200), nullable=False)
    thang = db.Column(db.Integer, nullable=False)
    nam = db.Column(db.Integer, nullable=False)
    noi_dung = db.Column(db.Text)
    duong_dan_file = db.Column(db.String(500))  # path to exported file
    nhan_vien_tao_id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), nullable=False)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BaoCao {self.ten_bao_cao}>'

class CaiDat(db.Model):
    __tablename__ = 'cai_dat'
    
    id = db.Column(db.Integer, primary_key=True)
    ten_cai_dat = db.Column(db.String(100), unique=True, nullable=False)
    gia_tri = db.Column(db.Text)
    mo_ta = db.Column(db.Text)
    loai = db.Column(db.String(50))  # string, number, boolean, json
    nhom = db.Column(db.String(50))  # he_thong, bao_mat, etc.
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CaiDat {self.ten_cai_dat}>'

class LichSuHoatDong(db.Model):
    __tablename__ = 'lich_su_hoat_dong'
    
    id = db.Column(db.Integer, primary_key=True)
    nhan_vien_id = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), nullable=False)
    hanh_dong = db.Column(db.String(100), nullable=False)
    doi_tuong = db.Column(db.String(100))  # don_hang, khach_hang, etc.
    doi_tuong_id = db.Column(db.Integer)
    chi_tiet = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LichSuHoatDong {self.hanh_dong}>'

# Indexes for better performance
# Note: Indexes will be created automatically by SQLAlchemy based on index=True in column definitions
