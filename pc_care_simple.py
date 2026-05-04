#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PC Care Management System - Python Version (Simple)
Hệ thống quản lý dịch vụ sửa chữa máy tính
"""

from datetime import datetime
from enum import Enum
import json
import os

class TrangThaiDonHang(Enum):
    CHO_TIEP_NHAN = "Cho tiep nhan"
    DANG_XU_LY = "Dang xu ly"
    CHO_LINH_KIEN = "Cho linh kien"
    DANG_SUA_CHUA = "Dang sua chua"
    HOAN_THANH = "Hoan thanh"
    DA_GIAO = "Da giao"
    HUY = "Huy"

class TrangThaiThanhToan(Enum):
    CHUA_THANH_TOAN = "Chua thanh toan"
    DA_DAT_COC = "Da dat coc"
    DA_THANH_TOAN = "Da thanh toan"

class LoaiThietBi(Enum):
    LAPTOP = "Laptop"
    PC_DESKTOP = "PC Desktop"
    MACBOOK = "Macbook"
    MAY_IN = "May in"
    MAN_HINH = "Man hinh"
    KHAC = "Khac"

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
        """Tai du lieu tu file JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Tai khach hang
                for kh_data in data.get('khach_hangs', []):
                    kh = KhachHang.from_dict(kh_data)
                    self.khach_hangs.append(kh)
                
                # Tai dich vu
                for dv_data in data.get('dich_vus', []):
                    dv = DichVu.from_dict(dv_data)
                    self.dich_vus.append(dv)
                
                # Tai linh kien
                for lk_data in data.get('linh_kiens', []):
                    lk = LinhKien.from_dict(lk_data)
                    self.linh_kiens.append(lk)
                
                # Tai don hang
                for dh_data in data.get('don_hangs', []):
                    dh = DonHang.from_dict(dh_data)
                    self.don_hangs.append(dh)
                
                # Tai next_id
                self.next_id = data.get('next_id', {'khach_hang': 1, 'dich_vu': 1, 'linh_kien': 1, 'don_hang': 1})
                
                print(f"Da tai du lieu tu {self.data_file}")
            except Exception as e:
                print(f"Loi khi tai du lieu: {e}")
                self.init_sample_data()
        else:
            self.init_sample_data()
    
    def save_data(self):
        """Luu du lieu vao file JSON"""
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
            
            print(f"Da luu du lieu vao {self.data_file}")
        except Exception as e:
            print(f"Loi khi luu du lieu: {e}")
    
    def init_sample_data(self):
        """Khoi tao du lieu mau"""
        print("Dang khoi tao du lieu mau...")
        
        # Them khach hang mau
        khach_hang_mau = [
            KhachHang(1, "Nguyen Van An", "0912345678", "an.nguyen@email.com", "Ha Noi"),
            KhachHang(2, "Tran Thi Binh", "0987654321", "binh.tran@email.com", "TP. Ho Chi Minh"),
            KhachHang(3, "Le Van Cuong", "0934567890", "cuong.le@email.com", "Da Nang"),
            KhachHang(4, "Pham Thi Dung", "0967890123", "dung.pham@email.com", "Hai Phong"),
            KhachHang(5, "Hoang Van Em", "0978901234", "em.hoang@email.com", "Can Tho"),
        ]
        self.khach_hangs.extend(khach_hang_mau)
        
        # Them dich vu mau
        dich_vu_mau = [
            DichVu(1, "Cai dat Windows", 200000, 1, "Cai dat Windows 10/11, driver va phan mem co ban"),
            DichVu(2, "Ve sinh may tinh", 150000, 0, "Ve sinh tong quat, tan nhiet, keo tan nhiet"),
            DichVu(3, "Thay keo tan nhiet", 250000, 3, "Thay keo tan nhiet cho CPU/GPU"),
            DichVu(4, "Nang cap RAM", 100000, 36, "Nang cap RAM laptop, PC"),
            DichVu(5, "Thay SSD", 100000, 36, "Thay SSD, cai dat he dieu hanh"),
            DichVu(6, "Thay man hinh Laptop", 1500000, 6, "Thay man hinh LCD, LED cho laptop"),
            DichVu(7, "Sua chua Mainboard", 500000, 3, "Sua chua cac loi mainboard, chipset"),
            DichVu(8, "Cuu du lieu", 800000, 0, "Cuu du lieu tu o cung hong, format"),
        ]
        self.dich_vus.extend(dich_vu_mau)
        
        # Them linh kien mau
        linh_kien_mau = [
            LinhKien(1, "RAM DDR4 8GB", "RAM8G01", 50, 800000, 1200000, "Kingston", "DDR4-3200"),
            LinhKien(2, "RAM DDR4 16GB", "RAM16G01", 30, 1500000, 2200000, "Corsair", "DDR4-3200"),
            LinhKien(3, "SSD 240GB SATA", "SSD24001", 25, 600000, 950000, "Samsung", "2.5 inch SATA"),
            LinhKien(4, "SSD 480GB SATA", "SSD48001", 20, 1000000, 1650000, "Crucial", "2.5 inch SATA"),
            LinhKien(5, "Keo tan nhiet", "GEL001", 100, 50000, 100000, "Arctic Silver", "Silicone thermal paste"),
        ]
        self.linh_kiens.extend(linh_kien_mau)
        
        # Cap nhat next_id
        self.next_id = {
            'khach_hang': len(self.khach_hangs) + 1,
            'dich_vu': len(self.dich_vus) + 1,
            'linh_kien': len(self.linh_kiens) + 1,
            'don_hang': 1
        }
        
        # Them don hang mau
        don_hang_mau = [
            DonHang(1, "DH20240501001", 1, "Dell XPS 15", LoaiThietBi.LAPTOP, "May cham cham, nong, can ve sinh va nang cap"),
            DonHang(2, "DH20240501002", 2, "Macbook Pro 13\"", LoaiThietBi.MACBOOK, "Man hinh bi soc, can thay man hinh moi"),
            DonHang(3, "DH20240501003", 3, "PC Gaming", LoaiThietBi.PC_DESKTOP, "May khong len nguon, can kiem tra main"),
        ]
        
        # Cap nhat trang thai va thong tin cho don hang mau
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
        print("Da khoi tao du lieu mau thanh cong!")

def clear_screen():
    """Xoa man hinh console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Dung man hinh de nguoi dung doc"""
    input("\nNhan Enter de tiep tuc...")

def show_main_menu():
    """Hien thi menu chinh"""
    ql = QuanLyPC()
    
    while True:
        clear_screen()
        print("=" * 60)
        print("PC CARE MANAGEMENT SYSTEM")
        print("He thong Quan ly Dich vu Sua chua May tinh")
        print("=" * 60)
        print(f"Khach hang: {len(ql.khach_hangs)} | Dich vu: {len(ql.dich_vus)} | Linh kien: {len(ql.linh_kiens)} | Don hang: {len(ql.don_hangs)}")
        print("-" * 60)
        print("1. Quan ly Khach hang")
        print("2. Quan ly Dich vu")
        print("3. Quan ly Linh kien")
        print("4. Quan ly Don hang")
        print("5. Thong ke")
        print("6. Luu du lieu")
        print("0. Thoat")
        print("-" * 60)
        
        choice = input("Chon chuc nang (0-6): ").strip()
        
        if choice == '1':
            menu_khach_hang(ql)
        elif choice == '2':
            menu_dich_vu(ql)
        elif choice == '3':
            menu_linh_kien(ql)
        elif choice == '4':
            menu_don_hang(ql)
        elif choice == '5':
            menu_thong_ke(ql)
        elif choice == '6':
            ql.save_data()
            pause()
        elif choice == '0':
            print("Cam on da su dung PC Care Management System!")
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def menu_khach_hang(ql):
    """Menu quan ly khach hang"""
    while True:
        clear_screen()
        print("QUAN LY KHACH HANG")
        print("-" * 30)
        print("1. Danh sach khach hang")
        print("2. Them khach hang moi")
        print("3. Tim kiem khach hang")
        print("4. Sua thong tin khach hang")
        print("5. Xoa khach hang")
        print("0. Quay lai")
        print("-" * 30)
        
        choice = input("Chon chuc nang (0-5): ").strip()
        
        if choice == '1':
            show_khach_hang_list(ql)
        elif choice == '2':
            add_khach_hang(ql)
        elif choice == '3':
            search_khach_hang(ql)
        elif choice == '4':
            edit_khach_hang(ql)
        elif choice == '5':
            delete_khach_hang(ql)
        elif choice == '0':
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def show_khach_hang_list(ql):
    """Hien thi danh sach khach hang"""
    clear_screen()
    print("DANH SACH KHACH HANG")
    print("-" * 50)
    
    if not ql.khach_hangs:
        print("Chua co khach hang nao!")
    else:
        print(f"{'ID':<5} {'Ho ten':<25} {'SDT':<15} {'Email':<25}")
        print("-" * 70)
        for kh in ql.khach_hangs:
            print(f"{kh.id:<5} {kh.ho_ten:<25} {kh.so_dien_thoai:<15} {kh.email:<25}")
    
    print(f"\nTong so: {len(ql.khach_hangs)} khach hang")
    pause()

def add_khach_hang(ql):
    """Them khach hang moi"""
    clear_screen()
    print("THEM KHACH HANG MOI")
    print("-" * 30)
    
    try:
        ho_ten = input("Ho ten: ").strip()
        if not ho_ten:
            print("Ho ten khong duoc de trong!")
            pause()
            return
        
        so_dien_thoai = input("So dien thoai: ").strip()
        if not so_dien_thoai:
            print("So dien thoai khong duoc de trong!")
            pause()
            return
        
        # Kiem tra trung SDT
        for kh in ql.khach_hangs:
            if kh.so_dien_thoai == so_dien_thoai:
                print("So dien thoai da ton tai!")
                pause()
                return
        
        email = input("Email: ").strip()
        dia_chi = input("Dia chi: ").strip()
        
        new_kh = KhachHang(
            ql.next_id['khach_hang'],
            ho_ten, so_dien_thoai, email, dia_chi
        )
        
        ql.khach_hangs.append(new_kh)
        ql.next_id['khach_hang'] += 1
        
        print(f"Da them khach hang {ho_ten} thanh cong!")
        ql.save_data()
        
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def search_khach_hang(ql):
    """Tim kiem khach hang"""
    clear_screen()
    print("TIM KIEM KHACH HANG")
    print("-" * 30)
    
    keyword = input("Nhap tu khoa (Ten, SDT, Email): ").strip().lower()
    
    if not keyword:
        print("Vui long nhap tu khoa tim kiem!")
        pause()
        return
    
    results = []
    for kh in ql.khach_hangs:
        if (keyword in kh.ho_ten.lower() or 
            keyword in kh.so_dien_thoai.lower() or 
            keyword in kh.email.lower()):
            results.append(kh)
    
    clear_screen()
    print(f"KET QUA TIM KIEM: '{keyword}'")
    print("-" * 50)
    
    if not results:
        print("Khong tim thay khach hang nao!")
    else:
        print(f"{'ID':<5} {'Ho ten':<25} {'SDT':<15} {'Email':<25}")
        print("-" * 70)
        for kh in results:
            print(f"{kh.id:<5} {kh.ho_ten:<25} {kh.so_dien_thoai:<15} {kh.email:<25}")
    
    print(f"\nTim thay {len(results)} ket qua")
    pause()

def edit_khach_hang(ql):
    """Sua thong tin khach hang"""
    clear_screen()
    print("SUA THONG TIN KHACH HANG")
    print("-" * 30)
    
    try:
        kh_id = int(input("Nhap ID khach hang: "))
        
        kh = None
        for k in ql.khach_hangs:
            if k.id == kh_id:
                kh = k
                break
        
        if not kh:
            print("Khong tim thay khach hang!")
            pause()
            return
        
        print(f"Thong tin hien tai:")
        print(f"   Ho ten: {kh.ho_ten}")
        print(f"   SDT: {kh.so_dien_thoai}")
        print(f"   Email: {kh.email}")
        print(f"   Dia chi: {kh.dia_chi}")
        
        print("\nNhap thong tin moi (de trong neu khong thay doi):")
        
        ho_ten = input(f"Ho ten [{kh.ho_ten}]: ").strip()
        so_dien_thoai = input(f"SDT [{kh.so_dien_thoai}]: ").strip()
        email = input(f"Email [{kh.email}]: ").strip()
        dia_chi = input(f"Dia chi [{kh.dia_chi}]: ").strip()
        
        if ho_ten:
            kh.ho_ten = ho_ten
        if so_dien_thoai:
            kh.so_dien_thoai = so_dien_thoai
        if email:
            kh.email = email
        if dia_chi:
            kh.dia_chi = dia_chi
        
        print("Cap nhat thong tin thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def delete_khach_hang(ql):
    """Xoa khach hang"""
    clear_screen()
    print("XOA KHACH HANG")
    print("-" * 30)
    
    try:
        kh_id = int(input("Nhap ID khach hang: "))
        
        kh = None
        for i, k in enumerate(ql.khach_hangs):
            if k.id == kh_id:
                kh = k
                index = i
                break
        
        if not kh:
            print("Khong tim thay khach hang!")
            pause()
            return
        
        print(f"Thong tin khach hang:")
        print(f"   Ho ten: {kh.ho_ten}")
        print(f"   SDT: {kh.so_dien_thoai}")
        
        # Kiem tra xem co don hang nao khong
        don_hang_count = sum(1 for dh in ql.don_hangs if dh.khach_hang_id == kh_id)
        if don_hang_count > 0:
            print(f"Canh bao: Khach hang co {don_hang_count} don hang!")
        
        confirm = input("Ban co chac muon xoa? (y/N): ").strip().lower()
        
        if confirm == 'y':
            ql.khach_hangs.pop(index)
            print("Xoa khach hang thanh cong!")
            ql.save_data()
        else:
            print("Da huy xoa!")
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def menu_dich_vu(ql):
    """Menu quan ly dich vu"""
    while True:
        clear_screen()
        print("QUAN LY DICH VU")
        print("-" * 30)
        print("1. Danh sach dich vu")
        print("2. Them dich vu moi")
        print("3. Sua dich vu")
        print("4. Xoa dich vu")
        print("0. Quay lai")
        print("-" * 30)
        
        choice = input("Chon chuc nang (0-4): ").strip()
        
        if choice == '1':
            show_dich_vu_list(ql)
        elif choice == '2':
            add_dich_vu(ql)
        elif choice == '3':
            edit_dich_vu(ql)
        elif choice == '4':
            delete_dich_vu(ql)
        elif choice == '0':
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def show_dich_vu_list(ql):
    """Hien thi danh sach dich vu"""
    clear_screen()
    print("DANH SACH DICH VU")
    print("-" * 50)
    
    if not ql.dich_vus:
        print("Chua co dich vu nao!")
    else:
        print(f"{'ID':<5} {'Ten dich vu':<25} {'Gia':<15} {'Bao hanh':<10}")
        print("-" * 65)
        for dv in ql.dich_vus:
            gia_str = f"{dv.gia_ban:,} VNĐ"
            bh_str = f"{dv.thoi_gian_bao_hanh} thang" if dv.thoi_gian_bao_hanh > 0 else "Khong"
            print(f"{dv.id:<5} {dv.ten_dich_vu:<25} {gia_str:<15} {bh_str:<10}")
    
    print(f"\nTong so: {len(ql.dich_vus)} dich vu")
    pause()

def add_dich_vu(ql):
    """Them dich vu moi"""
    clear_screen()
    print("THEM DICH VU MOI")
    print("-" * 30)
    
    try:
        ten_dich_vu = input("Ten dich vu: ").strip()
        if not ten_dich_vu:
            print("Ten dich vu khong duoc de trong!")
            pause()
            return
        
        # Kiem tra trung ten
        for dv in ql.dich_vus:
            if dv.ten_dich_vu == ten_dich_vu:
                print("Dich vu da ton tai!")
                pause()
                return
        
        gia_ban = float(input("Gia ban: "))
        if gia_ban < 0:
            print("Gia khong duoc am!")
            pause()
            return
        
        thoi_gian_bao_hanh = int(input("Thoi gian bao hanh (thang, 0 neu khong co): "))
        mo_ta = input("Mo ta: ").strip()
        
        new_dv = DichVu(
            ql.next_id['dich_vu'],
            ten_dich_vu, gia_ban, thoi_gian_bao_hanh, mo_ta
        )
        
        ql.dich_vus.append(new_dv)
        ql.next_id['dich_vu'] += 1
        
        print(f"Da them dich vu {ten_dich_vu} thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("Gia hoac thoi gian bao hanh khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def edit_dich_vu(ql):
    """Sua dich vu"""
    clear_screen()
    print("SUA DICH VU")
    print("-" * 30)
    
    try:
        dv_id = int(input("Nhap ID dich vu: "))
        
        dv = None
        for d in ql.dich_vus:
            if d.id == dv_id:
                dv = d
                break
        
        if not dv:
            print("Khong tim thay dich vu!")
            pause()
            return
        
        print(f"Thong tin hien tai:")
        print(f"   Ten dich vu: {dv.ten_dich_vu}")
        print(f"   Gia: {dv.gia_ban:,} VNĐ")
        print(f"   Bao hanh: {dv.thoi_gian_bao_hanh} thang")
        print(f"   Mo ta: {dv.mo_ta}")
        
        print("\nNhap thong tin moi (de trong neu khong thay doi):")
        
        ten_dich_vu = input(f"Ten dich vu [{dv.ten_dich_vu}]: ").strip()
        gia_str = input(f"Gia [{dv.gia_ban}]: ").strip()
        thoi_gian_str = input(f"Bao hanh (thang) [{dv.thoi_gian_bao_hanh}]: ").strip()
        mo_ta = input(f"Mo ta [{dv.mo_ta}]: ").strip()
        
        if ten_dich_vu:
            dv.ten_dich_vu = ten_dich_vu
        if gia_str:
            gia = float(gia_str)
            if gia >= 0:
                dv.gia_ban = gia
            else:
                print("Gia khong hop le, giu nguyen gia cu")
        if thoi_gian_str:
            thoi_gian = int(thoi_gian_str)
            if thoi_gian >= 0:
                dv.thoi_gian_bao_hanh = thoi_gian
            else:
                print("Thoi gian bao hanh khong hop le, giu nguyen gia tri cu")
        if mo_ta:
            dv.mo_ta = mo_ta
        
        print("Cap nhat dich vu thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("ID hoac gia khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def delete_dich_vu(ql):
    """Xoa dich vu"""
    clear_screen()
    print("XOA DICH VU")
    print("-" * 30)
    
    try:
        dv_id = int(input("Nhap ID dich vu: "))
        
        dv = None
        for i, d in enumerate(ql.dich_vus):
            if d.id == dv_id:
                dv = d
                index = i
                break
        
        if not dv:
            print("Khong tim thay dich vu!")
            pause()
            return
        
        print(f"Thong tin dich vu:")
        print(f"   Ten: {dv.ten_dich_vu}")
        print(f"   Gia: {dv.gia_ban:,} VNĐ")
        
        confirm = input("Ban co chac muon xoa? (y/N): ").strip().lower()
        
        if confirm == 'y':
            ql.dich_vus.pop(index)
            print("Xoa dich vu thanh cong!")
            ql.save_data()
        else:
            print("Da huy xoa!")
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def menu_linh_kien(ql):
    """Menu quan ly linh kien"""
    while True:
        clear_screen()
        print("QUAN LY LINH KIEN")
        print("-" * 30)
        print("1. Danh sach linh kien")
        print("2. Them linh kien moi")
        print("3. Sua linh kien")
        print("4. Xoa linh kien")
        print("5. Nhap hang")
        print("0. Quay lai")
        print("-" * 30)
        
        choice = input("Chon chuc nang (0-5): ").strip()
        
        if choice == '1':
            show_linh_kien_list(ql)
        elif choice == '2':
            add_linh_kien(ql)
        elif choice == '3':
            edit_linh_kien(ql)
        elif choice == '4':
            delete_linh_kien(ql)
        elif choice == '5':
            nhap_hang(ql)
        elif choice == '0':
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def show_linh_kien_list(ql):
    """Hien thi danh sach linh kien"""
    clear_screen()
    print("DANH SACH LINH KIEN")
    print("-" * 50)
    
    if not ql.linh_kiens:
        print("Chua co linh kien nao!")
    else:
        print(f"{'ID':<5} {'Ten linh kien':<20} {'Ma':<12} {'Ton':<8} {'Gia ban':<15}")
        print("-" * 70)
        for lk in ql.linh_kiens:
            gia_str = f"{lk.gia_ban:,} VNĐ"
            ton_str = str(lk.so_luong_ton)
            print(f"{lk.id:<5} {lk.ten_linh_kien:<20} {lk.ma_linh_kien:<12} {ton_str:<8} {gia_str:<15}")
    
    print(f"\nTong so: {len(ql.linh_kiens)} linh kien")
    pause()

def add_linh_kien(ql):
    """Them linh kien moi"""
    clear_screen()
    print("THEM LINH KIEN MOI")
    print("-" * 30)
    
    try:
        ten_linh_kien = input("Ten linh kien: ").strip()
        if not ten_linh_kien:
            print("Ten linh kien khong duoc de trong!")
            pause()
            return
        
        ma_linh_kien = input("Ma linh kien: ").strip()
        if not ma_linh_kien:
            print("Ma linh kien khong duoc de trong!")
            pause()
            return
        
        # Kiem tra trung ma
        for lk in ql.linh_kiens:
            if lk.ma_linh_kien == ma_linh_kien:
                print("Ma linh kien da ton tai!")
                pause()
                return
        
        so_luong_ton = int(input("So luong ton kho: "))
        gia_nhap = float(input("Gia nhap: "))
        gia_ban = float(input("Gia ban: "))
        nha_cung_cap = input("Nha cung cap: ").strip()
        thong_so_ky_thuat = input("Thong so ky thuat: ").strip()
        
        new_lk = LinhKien(
            ql.next_id['linh_kien'],
            ten_linh_kien, ma_linh_kien, so_luong_ton,
            gia_nhap, gia_ban, nha_cung_cap, thong_so_ky_thuat
        )
        
        ql.linh_kiens.append(new_lk)
        ql.next_id['linh_kien'] += 1
        
        print(f"Da them linh kien {ten_linh_kien} thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("So luong hoac gia khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def edit_linh_kien(ql):
    """Sua linh kien"""
    clear_screen()
    print("SUA LINH KIEN")
    print("-" * 30)
    
    try:
        lk_id = int(input("Nhap ID linh kien: "))
        
        lk = None
        for l in ql.linh_kiens:
            if l.id == lk_id:
                lk = l
                break
        
        if not lk:
            print("Khong tim thay linh kien!")
            pause()
            return
        
        print(f"Thong tin hien tai:")
        print(f"   Ten: {lk.ten_linh_kien}")
        print(f"   Ma: {lk.ma_linh_kien}")
        print(f"   Ton kho: {lk.so_luong_ton}")
        print(f"   Gia nhap: {lk.gia_nhap:,} VNĐ")
        print(f"   Gia ban: {lk.gia_ban:,} VNĐ")
        print(f"   Nha cung cap: {lk.nha_cung_cap}")
        
        print("\nNhap thong tin moi (de trong neu khong thay doi):")
        
        ten_linh_kien = input(f"Ten linh kien [{lk.ten_linh_kien}]: ").strip()
        ma_linh_kien = input(f"Ma linh kien [{lk.ma_linh_kien}]: ").strip()
        ton_str = input(f"Ton kho [{lk.so_luong_ton}]: ").strip()
        gia_nhap_str = input(f"Gia nhap [{lk.gia_nhap}]: ").strip()
        gia_ban_str = input(f"Gia ban [{lk.gia_ban}]: ").strip()
        nha_cung_cap = input(f"Nha cung cap [{lk.nha_cung_cap}]: ").strip()
        thong_so_ky_thuat = input(f"Thong so ky thuat [{lk.thong_so_ky_thuat}]: ").strip()
        
        if ten_linh_kien:
            lk.ten_linh_kien = ten_linh_kien
        if ma_linh_kien:
            lk.ma_linh_kien = ma_linh_kien
        if ton_str:
            ton = int(ton_str)
            if ton >= 0:
                lk.so_luong_ton = ton
        if gia_nhap_str:
            gia_nhap = float(gia_nhap_str)
            if gia_nhap >= 0:
                lk.gia_nhap = gia_nhap
        if gia_ban_str:
            gia_ban = float(gia_ban_str)
            if gia_ban >= 0:
                lk.gia_ban = gia_ban
        if nha_cung_cap:
            lk.nha_cung_cap = nha_cung_cap
        if thong_so_ky_thuat:
            lk.thong_so_ky_thuat = thong_so_ky_thuat
        
        print("Cap nhat linh kien thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("ID hoac gia tri khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def delete_linh_kien(ql):
    """Xoa linh kien"""
    clear_screen()
    print("XOA LINH KIEN")
    print("-" * 30)
    
    try:
        lk_id = int(input("Nhap ID linh kien: "))
        
        lk = None
        for i, l in enumerate(ql.linh_kiens):
            if l.id == lk_id:
                lk = l
                index = i
                break
        
        if not lk:
            print("Khong tim thay linh kien!")
            pause()
            return
        
        print(f"Thong tin linh kien:")
        print(f"   Ten: {lk.ten_linh_kien}")
        print(f"   Ma: {lk.ma_linh_kien}")
        print(f"   Ton kho: {lk.so_luong_ton}")
        
        if lk.so_luong_ton > 0:
            print(f"Canh bao: Con {lk.so_luong_ton} san pham trong kho!")
        
        confirm = input("Ban co chac muon xoa? (y/N): ").strip().lower()
        
        if confirm == 'y':
            ql.linh_kiens.pop(index)
            print("Xoa linh kien thanh cong!")
            ql.save_data()
        else:
            print("Da huy xoa!")
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def nhap_hang(ql):
    """Nhap hang linh kien"""
    clear_screen()
    print("NHAP HANG LINH KIEN")
    print("-" * 30)
    
    try:
        lk_id = int(input("Nhap ID linh kien: "))
        
        lk = None
        for l in ql.linh_kiens:
            if l.id == lk_id:
                lk = l
                break
        
        if not lk:
            print("Khong tim thay linh kien!")
            pause()
            return
        
        print(f"Thong tin linh kien:")
        print(f"   Ten: {lk.ten_linh_kien}")
        print(f"   Ton kho hien tai: {lk.so_luong_ton}")
        
        so_luong = int(input("So luong nhap: "))
        if so_luong <= 0:
            print("So luong phai lon hon 0!")
            pause()
            return
        
        gia_nhap_moi = input(f"Gia nhap moi [{lk.gia_nhap:,}]: ").strip()
        if gia_nhap_moi:
            gia_nhap = float(gia_nhap_moi)
            if gia_nhap >= 0:
                lk.gia_nhap = gia_nhap
            else:
                print("Gia nhap khong hop le, giu nguyen gia cu")
        
        lk.so_luong_ton += so_luong
        
        print(f"Nhap thanh cong {so_luong} {lk.ten_linh_kien}")
        print(f"Ton kho moi: {lk.so_luong_ton}")
        ql.save_data()
        
    except ValueError:
        print("ID hoac so luong khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def menu_don_hang(ql):
    """Menu quan ly don hang"""
    while True:
        clear_screen()
        print("QUAN LY DON HANG")
        print("-" * 30)
        print("1. Danh sach don hang")
        print("2. Tao don hang moi")
        print("3. Chi tiet don hang")
        print("4. Cap nhat trang thai")
        print("5. Xoa don hang")
        print("0. Quay lai")
        print("-" * 30)
        
        choice = input("Chon chuc nang (0-5): ").strip()
        
        if choice == '1':
            show_don_hang_list(ql)
        elif choice == '2':
            add_don_hang(ql)
        elif choice == '3':
            show_don_hang_detail(ql)
        elif choice == '4':
            update_trang_thai_don_hang(ql)
        elif choice == '5':
            delete_don_hang(ql)
        elif choice == '0':
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def show_don_hang_list(ql):
    """Hien thi danh sach don hang"""
    clear_screen()
    print("DANH SACH DON HANG")
    print("-" * 50)
    
    if not ql.don_hangs:
        print("Chua co don hang nao!")
    else:
        print(f"{'ID':<5} {'Ma don':<15} {'Khach hang':<20} {'Thiet bi':<20} {'Trang thai':<15}")
        print("-" * 85)
        for dh in ql.don_hangs:
            kh = next((k for k in ql.khach_hangs if k.id == dh.khach_hang_id), None)
            kh_ten = kh.ho_ten if kh else "Unknown"
            
            # Cat ten neu qua dai
            ten_tb = dh.ten_thiet_bi[:17] + "..." if len(dh.ten_thiet_bi) > 17 else dh.ten_thiet_bi
            ten_kh = kh_ten[:17] + "..." if len(kh_ten) > 17 else kh_ten
            
            print(f"{dh.id:<5} {dh.ma_don_hang:<15} {ten_kh:<20} {ten_tb:<20} {dh.trang_thai.value:<15}")
    
    print(f"\nTong so: {len(ql.don_hangs)} don hang")
    pause()

def add_don_hang(ql):
    """Tao don hang moi"""
    clear_screen()
    print("TAO DON HANG MOI")
    print("-" * 30)
    
    try:
        # Chon khach hang
        print("Chon khach hang:")
        if not ql.khach_hangs:
            print("Chua co khach hang nao trong he thong!")
            pause()
            return
        
        for kh in ql.khach_hangs:
            print(f"   {kh.id}. {kh.ho_ten} - {kh.so_dien_thoai}")
        
        kh_id = int(input("Nhap ID khach hang: "))
        
        kh = None
        for k in ql.khach_hangs:
            if k.id == kh_id:
                kh = k
                break
        
        if not kh:
            print("Khong tim thay khach hang!")
            pause()
            return
        
        # Thong tin thiet bi
        ten_thiet_bi = input("Ten thiet bi: ").strip()
        if not ten_thiet_bi:
            print("Ten thiet bi khong duoc de trong!")
            pause()
            return
        
        print("\nLoai thiet bi:")
        for i, loai in enumerate(LoaiThietBi, 1):
            print(f"   {i}. {loai.value}")
        
        loai_choice = int(input("Chon loai thiet bi (1-6): "))
        if 1 <= loai_choice <= 6:
            loai_thiet_bi = list(LoaiThietBi)[loai_choice - 1]
        else:
            print("Lua chon khong hop le!")
            pause()
            return
        
        nhan_hieu = input("Nhan hieu: ").strip()
        model = input("Model: ").strip()
        serial_number = input("Serial number: ").strip()
        mat_khau = input("Mat khau may tinh (neu co): ").strip()
        mo_ta_loi = input("Mo ta loi: ").strip()
        
        if not mo_ta_loi:
            print("Mo ta loi khong duoc de trong!")
            pause()
            return
        
        # Tao ma don hang
        ma_don_hang = f"DH{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        new_dh = DonHang(
            ql.next_id['don_hang'],
            ma_don_hang, kh_id, ten_thiet_bi, loai_thiet_bi, mo_ta_loi
        )
        
        new_dh.nhan_hieu = nhan_hieu
        new_dh.model = model
        new_dh.serial_number = serial_number
        new_dh.mat_khau = mat_khau
        
        ql.don_hangs.append(new_dh)
        ql.next_id['don_hang'] += 1
        
        print(f"Da tao don hang {ma_don_hang} thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("ID hoac lua chon khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def show_don_hang_detail(ql):
    """Hien thi chi tiet don hang"""
    clear_screen()
    print("CHI TIET DON HANG")
    print("-" * 30)
    
    try:
        dh_id = int(input("Nhap ID don hang: "))
        
        dh = None
        for d in ql.don_hangs:
            if d.id == dh_id:
                dh = d
                break
        
        if not dh:
            print("Khong tim thay don hang!")
            pause()
            return
        
        kh = next((k for k in ql.khach_hangs if k.id == dh.khach_hang_id), None)
        
        print("THONG TIN DON HANG")
        print("=" * 50)
        print(f"Ma don hang: {dh.ma_don_hang}")
        print(f"Ngay tiep nhan: {dh.ngay_tiep_nhan.strftime('%d/%m/%Y %H:%M')}")
        print(f"Khach hang: {kh.ho_ten if kh else 'Unknown'}")
        print(f"SDT: {kh.so_dien_thoai if kh else 'N/A'}")
        
        print(f"\nTHONG TIN THIET BI")
        print("-" * 30)
        print(f"Ten thiet bi: {dh.ten_thiet_bi}")
        print(f"Loai: {dh.loai_thiet_bi.value}")
        print(f"Nhan hieu: {dh.nhan_hieu}")
        print(f"Model: {dh.model}")
        print(f"Serial: {dh.serial_number}")
        
        print(f"\nMO TA LOI")
        print("-" * 30)
        print(dh.mo_ta_loi)
        
        print(f"\nTRANG THAI")
        print("-" * 30)
        print(f"Trang thai: {dh.trang_thai.value}")
        print(f"Thanh toan: {dh.trang_thai_thanh_toan.value}")
        print(f"Tong tien: {dh.tong_tien:,} VNĐ")
        print(f"Dat coc: {dh.tien_dat_coc:,} VNĐ")
        
        if dh.ngay_hoan_thanh:
            print(f"Ngay hoan thanh: {dh.ngay_hoan_thanh.strftime('%d/%m/%Y %H:%M')}")
        
        if dh.ghi_chu_nhan_vien:
            print(f"\nGHI CHU NHAN VIEN")
            print("-" * 30)
            print(dh.ghi_chu_nhan_vien)
        
        if dh.ghi_chu_khach_hang:
            print(f"\nGHI CHU KHACH HANG")
            print("-" * 30)
            print(dh.ghi_chu_khach_hang)
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def update_trang_thai_don_hang(ql):
    """Cap nhat trang thai don hang"""
    clear_screen()
    print("CAP NHAT TRANG THAI DON HANG")
    print("-" * 30)
    
    try:
        dh_id = int(input("Nhap ID don hang: "))
        
        dh = None
        for d in ql.don_hangs:
            if d.id == dh_id:
                dh = d
                break
        
        if not dh:
            print("Khong tim thay don hang!")
            pause()
            return
        
        print(f"Don hang: {dh.ma_don_hang}")
        print(f"Trang thai hien tai: {dh.trang_thai.value}")
        print(f"Thanh toan hien tai: {dh.trang_thai_thanh_toan.value}")
        
        print("\nChon trang thai moi:")
        for i, trang_thai in enumerate(TrangThaiDonHang, 1):
            print(f"   {i}. {trang_thai.value}")
        
        trang_thai_choice = int(input("Chon trang thai (1-7): "))
        if 1 <= trang_thai_choice <= 7:
            trang_thai_moi = list(TrangThaiDonHang)[trang_thai_choice - 1]
        else:
            print("Lua chon khong hop le!")
            pause()
            return
        
        print("\nChon trang thai thanh toan:")
        for i, trang_thai_tt in enumerate(TrangThaiThanhToan, 1):
            print(f"   {i}. {trang_thai_tt.value}")
        
        tt_choice = int(input("Chon trang thai thanh toan (1-3): "))
        if 1 <= tt_choice <= 3:
            tt_moi = list(TrangThaiThanhToan)[tt_choice - 1]
        else:
            print("Lua chon khong hop le!")
            pause()
            return
        
        # Cap nhat ngay hoan thanh neu trang thai la hoan thanh
        if trang_thai_moi == TrangThaiDonHang.HOAN_THANH and dh.trang_thai != TrangThaiDonHang.HOAN_THANH:
            dh.ngay_hoan_thanh = datetime.now()
        
        dh.trang_thai = trang_thai_moi
        dh.trang_thai_thanh_toan = tt_moi
        
        # Cap nhat tong tien neu thanh toan
        if tt_moi == TrangThaiThanhToan.DA_THANH_TOAN:
            try:
                tong_tien = float(input("Nhap tong tien: "))
                if tong_tien >= 0:
                    dh.tong_tien = tong_tien
                else:
                    print("Tong tien khong hop le")
            except ValueError:
                print("Tong tien khong hop le, giu nguyen gia cu")
        
        print("Cap nhat trang thai thanh cong!")
        ql.save_data()
        
    except ValueError:
        print("ID hoac lua chon khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def delete_don_hang(ql):
    """Xoa don hang"""
    clear_screen()
    print("XOA DON HANG")
    print("-" * 30)
    
    try:
        dh_id = int(input("Nhap ID don hang: "))
        
        dh = None
        for i, d in enumerate(ql.don_hangs):
            if d.id == dh_id:
                dh = d
                index = i
                break
        
        if not dh:
            print("Khong tim thay don hang!")
            pause()
            return
        
        print(f"Thong tin don hang:")
        print(f"   Ma don: {dh.ma_don_hang}")
        print(f"   Khach hang: {next((k.ho_ten for k in ql.khach_hangs if k.id == dh.khach_hang_id), 'Unknown')}")
        print(f"   Thiet bi: {dh.ten_thiet_bi}")
        print(f"   Trang thai: {dh.trang_thai.value}")
        
        if dh.trang_thai == TrangThaiDonHang.HOAN_THANH:
            print("Canh bao: Don hang da hoan thanh!")
        elif dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN:
            print("Canh bao: Don hang da thanh toan!")
        
        confirm = input("Ban co chac muon xoa? (y/N): ").strip().lower()
        
        if confirm == 'y':
            ql.don_hangs.pop(index)
            print("Xoa don hang thanh cong!")
            ql.save_data()
        else:
            print("Da huy xoa!")
        
    except ValueError:
        print("ID khong hop le!")
    except Exception as e:
        print(f"Loi: {e}")
    
    pause()

def menu_thong_ke(ql):
    """Menu thong ke"""
    while True:
        clear_screen()
        print("THONG KE & BAO CAO")
        print("-" * 30)
        print("1. Tong quan")
        print("2. Thong ke don hang")
        print("3. Doanh thu")
        print("0. Quay lai")
        print("-" * 30)
        
        choice = input("Chon chuc nang (0-3): ").strip()
        
        if choice == '1':
            show_tong_quan(ql)
        elif choice == '2':
            show_thong_ke_don_hang(ql)
        elif choice == '3':
            show_doanh_thu(ql)
        elif choice == '0':
            break
        else:
            print("Lua chon khong hop le!")
            pause()

def show_tong_quan(ql):
    """Hien thi tong quan"""
    clear_screen()
    print("TONG QUAN HE THONG")
    print("=" * 50)
    
    # Thong ke co ban
    tong_kh = len(ql.khach_hangs)
    tong_dv = len(ql.dich_vus)
    tong_lk = len(ql.linh_kiens)
    tong_dh = len(ql.don_hangs)
    
    print(f"Tong so khach hang: {tong_kh}")
    print(f"Tong so dich vu: {tong_dv}")
    print(f"Tong so linh kien: {tong_lk}")
    print(f"Tong so don hang: {tong_dh}")
    
    # Thong ke don hang theo trang thai
    print(f"\nTHONG KE DON HANG THEO TRANG THAI")
    print("-" * 40)
    for trang_thai in TrangThaiDonHang:
        count = sum(1 for dh in ql.don_hangs if dh.trang_thai == trang_thai)
        print(f"   {trang_thai.value}: {count}")
    
    # Thong ke thanh toan
    print(f"\nTHONG KE THANH TOAN")
    print("-" * 30)
    for tt in TrangThaiThanhToan:
        count = sum(1 for dh in ql.don_hangs if dh.trang_thai_thanh_toan == tt)
        print(f"   {tt.value}: {count}")
    
    # Top 5 khach hang co nhieu don hang nhat
    print(f"\nTOP 5 KHACH HANG NHIEU DON HANG NHAT")
    print("-" * 50)
    kh_stats = {}
    for kh in ql.khach_hangs:
        count = sum(1 for dh in ql.don_hangs if dh.khach_hang_id == kh.id)
        if count > 0:
            kh_stats[kh.ho_ten] = count
    
    sorted_kh = sorted(kh_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (ten, count) in enumerate(sorted_kh, 1):
        print(f"   {i}. {ten}: {count} don hang")
    
    # Tong gia tri kho
    tong_gia_tri_kho = sum(lk.gia_nhap * lk.so_luong_ton for lk in ql.linh_kiens)
    print(f"\nTONG GIA TRI KHO: {tong_gia_tri_kho:,} VNĐ")
    
    # Doanh thu uoc tinh
    doanh_thu = sum(dh.tong_tien for dh in ql.don_hangs if dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN)
    print(f"DOANH THU DA THANH TOAN: {doanh_thu:,} VNĐ")
    
    pause()

def show_thong_ke_don_hang(ql):
    """Thong ke chi tiet don hang"""
    clear_screen()
    print("THONG KE CHI TIET DON HANG")
    print("=" * 50)
    
    # Thong ke theo loai thiet bi
    print("THONG KE THEO LOAI THIET BI")
    print("-" * 40)
    loai_stats = {}
    for loai in LoaiThietBi:
        count = sum(1 for dh in ql.don_hangs if dh.loai_thiet_bi == loai)
        if count > 0:
            loai_stats[loai.value] = count
    
    for loai, count in sorted(loai_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   {loai}: {count}")
    
    # Don hang gan day
    print(f"\n5 DON HANG GAN DAY NHAT")
    print("-" * 50)
    recent_dh = sorted(ql.don_hangs, key=lambda x: x.ngay_tiep_nhan, reverse=True)[:5]
    
    for dh in recent_dh:
        kh = next((k for k in ql.khach_hangs if k.id == dh.khach_hang_id), None)
        print(f"   {dh.ma_don_hang} - {kh.ho_ten if kh else 'Unknown'} - {dh.trang_thai.value}")
    
    pause()

def show_doanh_thu(ql):
    """Hien thi doanh thu"""
    clear_screen()
    print("BAO CAO DOANH THU")
    print("=" * 50)
    
    # Doanh thu theo trang thai thanh toan
    print("DOANH THU THEO TRANG THAI THANH TOAN")
    print("-" * 50)
    for tt in TrangThaiThanhToan:
        don_hangs_tt = [dh for dh in ql.don_hangs if dh.trang_thai_thanh_toan == tt]
        tong_tien = sum(dh.tong_tien for dh in don_hangs_tt)
        print(f"   {tt.value}: {len(don_hangs_tt)} don - {tong_tien:,} VNĐ")
    
    # Doanh thu theo thang
    print(f"\nDOANH THU THEO THANG")
    print("-" * 40)
    thang_stats = {}
    for dh in ql.don_hangs:
        if dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN:
            thang = dh.ngay_tiep_nhan.strftime('%Y-%m')
            if thang not in thang_stats:
                thang_stats[thang] = 0
            thang_stats[thang] += dh.tong_tien
    
    for thang, doanh_thu in sorted(thang_stats.items(), reverse=True):
        print(f"   {thang}: {doanh_thu:,} VNĐ")
    
    pause()

if __name__ == "__main__":
    show_main_menu()
