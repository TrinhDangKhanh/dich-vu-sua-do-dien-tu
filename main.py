#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hệ thống quản lý dịch vụ sửa chữa máy tính PC Care - Phiên bản Python thuần
"""

from datetime import datetime
from enum import Enum
import json
import os

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

class KhachHang:
    def __init__(self, id, ho_ten, so_dien_thoai, email="", dia_chi=""):
        self.id = id
        self.ho_ten = ho_ten
        self.so_dien_thoai = so_dien_thoai
        self.email = email
        self.dia_chi = dia_chi
        self.ngay_tao = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'ho_ten': self.ho_ten,
            'so_dien_thoai': self.so_dien_thoai,
            'email': self.email,
            'dia_chi': self.dia_chi,
            'ngay_tao': self.ngay_tao.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data):
        kh = cls(data['id'], data['ho_ten'], data['so_dien_thoai'], 
                data.get('email', ''), data.get('dia_chi', ''))
        kh.ngay_tao = datetime.strptime(data['ngay_tao'], '%Y-%m-%d %H:%M:%S')
        return kh

class DichVu:
    def __init__(self, id, ten_dich_vu, gia_ban, thoi_gian_bao_hanh=0, mo_ta=""):
        self.id = id
        self.ten_dich_vu = ten_dich_vu
        self.mo_ta = mo_ta
        self.gia_ban = gia_ban
        self.thoi_gian_bao_hanh = thoi_gian_bao_hanh
        self.ngay_tao = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'ten_dich_vu': self.ten_dich_vu,
            'mo_ta': self.mo_ta,
            'gia_ban': self.gia_ban,
            'thoi_gian_bao_hanh': self.thoi_gian_bao_hanh,
            'ngay_tao': self.ngay_tao.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data):
        dv = cls(data['id'], data['ten_dich_vu'], data['gia_ban'], 
                data.get('thoi_gian_bao_hanh', 0), data.get('mo_ta', ''))
        dv.ngay_tao = datetime.strptime(data['ngay_tao'], '%Y-%m-%d %H:%M:%S')
        return dv

class LinhKien:
    def __init__(self, id, ten_linh_kien, ma_linh_kien, so_luong_ton=0, gia_nhap=0, gia_ban=0, nha_cung_cap="", thong_so_ky_thuat=""):
        self.id = id
        self.ten_linh_kien = ten_linh_kien
        self.ma_linh_kien = ma_linh_kien
        self.so_luong_ton = so_luong_ton
        self.gia_nhap = gia_nhap
        self.gia_ban = gia_ban
        self.nha_cung_cap = nha_cung_cap
        self.thong_so_ky_thuat = thong_so_ky_thuat
        self.ngay_tao = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'ten_linh_kien': self.ten_linh_kien,
            'ma_linh_kien': self.ma_linh_kien,
            'so_luong_ton': self.so_luong_ton,
            'gia_nhap': self.gia_nhap,
            'gia_ban': self.gia_ban,
            'nha_cung_cap': self.nha_cung_cap,
            'thong_so_ky_thuat': self.thong_so_ky_thuat,
            'ngay_tao': self.ngay_tao.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data):
        lk = cls(data['id'], data['ten_linh_kien'], data['ma_linh_kien'],
                data.get('so_luong_ton', 0), data.get('gia_nhap', 0), 
                data.get('gia_ban', 0), data.get('nha_cung_cap', ''),
                data.get('thong_so_ky_thuat', ''))
        lk.ngay_tao = datetime.strptime(data['ngay_tao'], '%Y-%m-%d %H:%M:%S')
        return lk

class DonHang:
    def __init__(self, id, ma_don_hang, khach_hang_id, ten_thiet_bi, loai_thiet_bi, mo_ta_loi):
        self.id = id
        self.ma_don_hang = ma_don_hang
        self.khach_hang_id = khach_hang_id
        self.ten_thiet_bi = ten_thiet_bi
        self.loai_thiet_bi = loai_thiet_bi
        self.nhan_hieu = ""
        self.model = ""
        self.serial_number = ""
        self.mat_khau = ""
        self.mo_ta_loi = mo_ta_loi
        self.trang_thai = TrangThaiDonHang.CHO_TIEP_NHAN
        self.trang_thai_thanh_toan = TrangThaiThanhToan.CHUA_THANH_TOAN
        self.tong_tien = 0
        self.tien_dat_coc = 0
        self.ngay_tiep_nhan = datetime.now()
        self.ngay_hoan_thanh = None
        self.ngay_giao_hang = None
        self.ghi_chu_nhan_vien = ""
        self.ghi_chu_khach_hang = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'ma_don_hang': self.ma_don_hang,
            'khach_hang_id': self.khach_hang_id,
            'ten_thiet_bi': self.ten_thiet_bi,
            'loai_thiet_bi': self.loai_thiet_bi.value,
            'nhan_hieu': self.nhan_hieu,
            'model': self.model,
            'serial_number': self.serial_number,
            'mat_khau': self.mat_khau,
            'mo_ta_loi': self.mo_ta_loi,
            'trang_thai': self.trang_thai.value,
            'trang_thai_thanh_toan': self.trang_thai_thanh_toan.value,
            'tong_tien': self.tong_tien,
            'tien_dat_coc': self.tien_dat_coc,
            'ngay_tiep_nhan': self.ngay_tiep_nhan.strftime('%Y-%m-%d %H:%M:%S'),
            'ngay_hoan_thanh': self.ngay_hoan_thanh.strftime('%Y-%m-%d %H:%M:%S') if self.ngay_hoan_thanh else None,
            'ngay_giao_hang': self.ngay_giao_hang.strftime('%Y-%m-%d %H:%M:%S') if self.ngay_giao_hang else None,
            'ghi_chu_nhan_vien': self.ghi_chu_nhan_vien,
            'ghi_chu_khach_hang': self.ghi_chu_khach_hang
        }
    
    @classmethod
    def from_dict(cls, data):
        dh = cls(data['id'], data['ma_don_hang'], data['khach_hang_id'],
                data['ten_thiet_bi'], LoaiThietBi(data['loai_thiet_bi']), data['mo_ta_loi'])
        dh.nhan_hieu = data.get('nhan_hieu', '')
        dh.model = data.get('model', '')
        dh.serial_number = data.get('serial_number', '')
        dh.mat_khau = data.get('mat_khau', '')
        dh.trang_thai = TrangThaiDonHang(data['trang_thai'])
        dh.trang_thai_thanh_toan = TrangThaiThanhToan(data['trang_thai_thanh_toan'])
        dh.tong_tien = data.get('tong_tien', 0)
        dh.tien_dat_coc = data.get('tien_dat_coc', 0)
        dh.ngay_tiep_nhan = datetime.strptime(data['ngay_tiep_nhan'], '%Y-%m-%d %H:%M:%S')
        dh.ngay_hoan_thanh = datetime.strptime(data['ngay_hoan_thanh'], '%Y-%m-%d %H:%M:%S') if data.get('ngay_hoan_thanh') else None
        dh.ngay_giao_hang = datetime.strptime(data['ngay_giao_hang'], '%Y-%m-%d %H:%M:%S') if data.get('ngay_giao_hang') else None
        dh.ghi_chu_nhan_vien = data.get('ghi_chu_nhan_vien', '')
        dh.ghi_chu_khach_hang = data.get('ghi_chu_khach_hang', '')
        return dh

class QuanLyPC:
    def __init__(self):
        self.khach_hangs = []
        self.dich_vus = []
        self.linh_kiens = []
        self.don_hangs = []
        self.next_id = {'khach_hang': 1, 'dich_vu': 1, 'linh_kien': 1, 'don_hang': 1}
        self.data_file = 'pc_care_data.json'
        self.load_data()
    
    def load_data(self):
        """Tải dữ liệu từ file JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Tải khách hàng
                for kh_data in data.get('khach_hangs', []):
                    kh = KhachHang.from_dict(kh_data)
                    self.khach_hangs.append(kh)
                
                # Tải dịch vụ
                for dv_data in data.get('dich_vus', []):
                    dv = DichVu.from_dict(dv_data)
                    self.dich_vus.append(dv)
                
                # Tải linh kiện
                for lk_data in data.get('linh_kiens', []):
                    lk = LinhKien.from_dict(lk_data)
                    self.linh_kiens.append(lk)
                
                # Tải đơn hàng
                for dh_data in data.get('don_hangs', []):
                    dh = DonHang.from_dict(dh_data)
                    self.don_hangs.append(dh)
                
                # Tải next_id
                self.next_id = data.get('next_id', {'khach_hang': 1, 'dich_vu': 1, 'linh_kien': 1, 'don_hang': 1})
                
                print(f"✅ Đã tải dữ liệu từ {self.data_file}")
            except Exception as e:
                print(f"❌ Lỗi khi tải dữ liệu: {e}")
                self.init_sample_data()
        else:
            self.init_sample_data()
    
    def save_data(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            data = {
                'khach_hangs': [kh.to_dict() for kh in self.khach_hangs],
                'dich_vus': [dv.to_dict() for dv in self.dich_vus],
                'linh_kiens': [lk.to_dict() for lk in self.linh_kiens],
                'don_hangs': [dh.to_dict() for dh in self.don_hangs],
                'next_id': self.next_id
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Đã lưu dữ liệu vào {self.data_file}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu dữ liệu: {e}")
    
    def init_sample_data(self):
        """Khởi tạo dữ liệu mẫu"""
        print("🔄 Khởi tạo dữ liệu mẫu...")
        
        # Thêm khách hàng mẫu
        khach_hang_mau = [
            KhachHang(1, "Nguyễn Văn An", "0912345678", "an.nguyen@email.com", "Hà Nội"),
            KhachHang(2, "Trần Thị Bình", "0987654321", "binh.tran@email.com", "TP. Hồ Chí Minh"),
            KhachHang(3, "Lê Văn Cường", "0934567890", "cuong.le@email.com", "Đà Nẵng"),
            KhachHang(4, "Phạm Thị Dung", "0967890123", "dung.pham@email.com", "Hải Phòng"),
            KhachHang(5, "Hoàng Văn Em", "0978901234", "em.hoang@email.com", "Cần Thơ"),
        ]
        self.khach_hangs.extend(khach_hang_mau)
        
        # Thêm dịch vụ mẫu
        dich_vu_mau = [
            DichVu(1, "Cài đặt Windows", 200000, 1, "Cài đặt Windows 10/11, driver và phần mềm cơ bản"),
            DichVu(2, "Vệ sinh máy tính", 150000, 0, "Vệ sinh tổng quát, tản nhiệt, keo tản nhiệt"),
            DichVu(3, "Thay keo tản nhiệt", 250000, 3, "Thay keo tản nhiệt cho CPU/GPU"),
            DichVu(4, "Nâng cấp RAM", 100000, 36, "Nâng cấp RAM laptop, PC"),
            DichVu(5, "Thay SSD", 100000, 36, "Thay SSD, cài đặt hệ điều hành"),
            DichVu(6, "Thay màn hình Laptop", 1500000, 6, "Thay màn hình LCD, LED cho laptop"),
            DichVu(7, "Sửa chữa Mainboard", 500000, 3, "Sửa chữa các lỗi mainboard, chipset"),
            DichVu(8, "Cứu dữ liệu", 800000, 0, "Cứu dữ liệu từ ổ cứng hỏng, format"),
        ]
        self.dich_vus.extend(dich_vu_mau)
        
        # Thêm linh kiện mẫu
        linh_kien_mau = [
            LinhKien(1, "RAM DDR4 8GB", "RAM8G01", 50, 800000, 1200000, "Kingston", "DDR4-3200"),
            LinhKien(2, "RAM DDR4 16GB", "RAM16G01", 30, 1500000, 2200000, "Corsair", "DDR4-3200"),
            LinhKien(3, "SSD 240GB SATA", "SSD24001", 25, 600000, 950000, "Samsung", "2.5 inch SATA"),
            LinhKien(4, "SSD 480GB SATA", "SSD48001", 20, 1000000, 1650000, "Crucial", "2.5 inch SATA"),
            LinhKien(5, "Keo tản nhiệt", "GEL001", 100, 50000, 100000, "Arctic Silver", "Silicone thermal paste"),
        ]
        self.linh_kiens.extend(linh_kien_mau)
        
        # Cập nhật next_id
        self.next_id = {
            'khach_hang': len(self.khach_hangs) + 1,
            'dich_vu': len(self.dich_vus) + 1,
            'linh_kien': len(self.linh_kiens) + 1,
            'don_hang': 1
        }
        
        # Thêm đơn hàng mẫu
        don_hang_mau = [
            DonHang(1, "DH20240501001", 1, "Dell XPS 15", LoaiThietBi.LAPTOP, "Máy chạy chậm, nóng, cần vệ sinh và nâng cấp"),
            DonHang(2, "DH20240501002", 2, "Macbook Pro 13\"", LoaiThietBi.MACBOOK, "Màn hình bị sọc, cần thay màn hình mới"),
            DonHang(3, "DH20240501003", 3, "PC Gaming", LoaiThietBi.PC_DESKTOP, "Máy không lên nguồn, cần kiểm tra main"),
        ]
        
        # Cập nhật trạng thái và thông tin cho đơn hàng mẫu
        don_hang_mau[0].trang_thai = TrangThaiDonHang.DANG_XU_LY
        don_hang_mau[0].tong_tien = 1350000
        don_hang_mau[0].nhan_hieu = "Dell"
        don_hang_mau[0].model = "XPS 9570"
        
        don_hang_mau[1].trang_thai = TrangThaiDonHang.CHO_LINH_KIEN
        don_hang_mau[1].tong_tien = 3200000
        don_hang_mau[1].nhan_hieu = "Apple"
        don_hang_mau[1].model = "Macbook Pro 2020"
        
        don_hang_mau[2].trang_thai = TrangThaiDonHang.HOAN_THANH
        don_hang_mau[2].tong_tien = 500000
        don_hang_mau[2].ngay_hoan_thanh = datetime.now()
        don_hang_mau[2].nhan_hieu = "Custom"
        don_hang_mau[2].model = "Gaming PC"
        
        self.don_hangs.extend(don_hang_mau)
        self.next_id['don_hang'] = len(self.don_hangs) + 1
        
        self.save_data()
        print("✅ Đã khởi tạo dữ liệu mẫu thành công!")

if __name__ == "__main__":
    ql = QuanLyPC()
    print("🔧 PC Care Management System - Python Version")
    print("📊 Hệ thống quản lý dịch vụ sửa chữa máy tính")
    print("=" * 50)
    print(f"👥 Khách hàng: {len(ql.khach_hangs)}")
    print(f"🛠️ Dịch vụ: {len(ql.dich_vus)}")
    print(f"🔩 Linh kiện: {len(ql.linh_kiens)}")
    print(f"📋 Đơn hàng: {len(ql.don_hangs)}")
    print("=" * 50)
