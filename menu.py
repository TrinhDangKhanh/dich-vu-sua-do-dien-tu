#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu interface cho PC Care Management System
"""

from main import QuanLyPC, DonHang, KhachHang, DichVu, LinhKien, LoaiThietBi, TrangThaiDonHang, TrangThaiThanhToan
from datetime import datetime
import os
import sys

class PCMenu:
    def __init__(self):
        self.ql = QuanLyPC()
        self.clear_screen()
    
    def clear_screen(self):
        """Xóa màn hình console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pause(self):
        """Dừng màn hình để người dùng đọc"""
        input("\n👆 Nhấn Enter để tiếp tục...")
    
    def show_header(self):
        """Hiển thị header"""
        self.clear_screen()
        print("🔧 PC CARE MANAGEMENT SYSTEM")
        print("📊 Hệ thống Quản lý Dịch vụ Sửa chữa Máy tính")
        print("=" * 60)
    
    def show_main_menu(self):
        """Hiển thị menu chính"""
        while True:
            self.show_header()
            print("📋 MENU CHÍNH")
            print("-" * 30)
            print("1. 👥 Quản lý Khách hàng")
            print("2. 🛠️ Quản lý Dịch vụ")
            print("3. 🔩 Quản lý Linh kiện")
            print("4. 📋 Quản lý Đơn hàng")
            print("5. 📊 Thống kê & Báo cáo")
            print("6. 💾 Lưu dữ liệu")
            print("7. 🔄 Tải lại dữ liệu")
            print("0. 🚪 Thoát")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-7): ").strip()
            
            if choice == '1':
                self.menu_khach_hang()
            elif choice == '2':
                self.menu_dich_vu()
            elif choice == '3':
                self.menu_linh_kien()
            elif choice == '4':
                self.menu_don_hang()
            elif choice == '5':
                self.menu_thong_ke()
            elif choice == '6':
                self.ql.save_data()
                self.pause()
            elif choice == '7':
                self.ql.load_data()
                self.pause()
            elif choice == '0':
                print("👋 Cảm ơn đã sử dụng PC Care Management System!")
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def menu_khach_hang(self):
        """Menu quản lý khách hàng"""
        while True:
            self.show_header()
            print("👥 QUẢN LÝ KHÁCH HÀNG")
            print("-" * 30)
            print("1. 📄 Danh sách khách hàng")
            print("2. ➕ Thêm khách hàng mới")
            print("3. 🔍 Tìm kiếm khách hàng")
            print("4. ✏️ Sửa thông tin khách hàng")
            print("5. 🗑️ Xóa khách hàng")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-5): ").strip()
            
            if choice == '1':
                self.show_khach_hang_list()
            elif choice == '2':
                self.add_khach_hang()
            elif choice == '3':
                self.search_khach_hang()
            elif choice == '4':
                self.edit_khach_hang()
            elif choice == '5':
                self.delete_khach_hang()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def show_khach_hang_list(self):
        """Hiển thị danh sách khách hàng"""
        self.show_header()
        print("👥 DANH SÁCH KHÁCH HÀNG")
        print("-" * 50)
        
        if not self.ql.khach_hangs:
            print("📭 Chưa có khách hàng nào!")
        else:
            print(f"{'ID':<5} {'Họ tên':<25} {'SĐT':<15} {'Email':<25}")
            print("-" * 70)
            for kh in self.ql.khach_hangs:
                print(f"{kh.id:<5} {kh.ho_ten:<25} {kh.so_dien_thoai:<15} {kh.email:<25}")
        
        print(f"\n📊 Tổng số: {len(self.ql.khach_hangs)} khách hàng")
        self.pause()
    
    def add_khach_hang(self):
        """Thêm khách hàng mới"""
        self.show_header()
        print("➕ THÊM KHÁCH HÀNG MỚI")
        print("-" * 30)
        
        try:
            ho_ten = input("👤 Họ tên: ").strip()
            if not ho_ten:
                print("❌ Họ tên không được để trống!")
                self.pause()
                return
            
            so_dien_thoai = input("📱 Số điện thoại: ").strip()
            if not so_dien_thoai:
                print("❌ Số điện thoại không được để trống!")
                self.pause()
                return
            
            # Kiểm tra trùng SĐT
            for kh in self.ql.khach_hangs:
                if kh.so_dien_thoai == so_dien_thoai:
                    print("❌ Số điện thoại đã tồn tại!")
                    self.pause()
                    return
            
            email = input("📧 Email: ").strip()
            dia_chi = input("🏠 Địa chỉ: ").strip()
            
            new_kh = KhachHang(
                self.ql.next_id['khach_hang'],
                ho_ten, so_dien_thoai, email, dia_chi
            )
            
            self.ql.khach_hangs.append(new_kh)
            self.ql.next_id['khach_hang'] += 1
            
            print(f"✅ Đã thêm khách hàng {ho_ten} thành công!")
            self.ql.save_data()
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def search_khach_hang(self):
        """Tìm kiếm khách hàng"""
        self.show_header()
        print("🔍 TÌM KIẾM KHÁCH HÀNG")
        print("-" * 30)
        
        keyword = input("🔎 Nhập từ khóa (Tên, SĐT, Email): ").strip().lower()
        
        if not keyword:
            print("❌ Vui lòng nhập từ khóa tìm kiếm!")
            self.pause()
            return
        
        results = []
        for kh in self.ql.khach_hangs:
            if (keyword in kh.ho_ten.lower() or 
                keyword in kh.so_dien_thoai.lower() or 
                keyword in kh.email.lower()):
                results.append(kh)
        
        self.show_header()
        print(f"🔍 KẾT QUẢ TÌM KIẾM: '{keyword}'")
        print("-" * 50)
        
        if not results:
            print("📭 Không tìm thấy khách hàng nào!")
        else:
            print(f"{'ID':<5} {'Họ tên':<25} {'SĐT':<15} {'Email':<25}")
            print("-" * 70)
            for kh in results:
                print(f"{kh.id:<5} {kh.ho_ten:<25} {kh.so_dien_thoai:<15} {kh.email:<25}")
        
        print(f"\n📊 Tìm thấy {len(results)} kết quả")
        self.pause()
    
    def edit_khach_hang(self):
        """Sửa thông tin khách hàng"""
        self.show_header()
        print("✏️ SỬA THÔNG TIN KHÁCH HÀNG")
        print("-" * 30)
        
        try:
            kh_id = int(input("🆔 Nhập ID khách hàng: "))
            
            kh = None
            for k in self.ql.khach_hangs:
                if k.id == kh_id:
                    kh = k
                    break
            
            if not kh:
                print("❌ Không tìm thấy khách hàng!")
                self.pause()
                return
            
            print(f"📄 Thông tin hiện tại:")
            print(f"   Họ tên: {kh.ho_ten}")
            print(f"   SĐT: {kh.so_dien_thoai}")
            print(f"   Email: {kh.email}")
            print(f"   Địa chỉ: {kh.dia_chi}")
            
            print("\n📝 Nhập thông tin mới (để trống nếu không thay đổi):")
            
            ho_ten = input(f"👤 Họ tên [{kh.ho_ten}]: ").strip()
            so_dien_thoai = input(f"📱 SĐT [{kh.so_dien_thoai}]: ").strip()
            email = input(f"📧 Email [{kh.email}]: ").strip()
            dia_chi = input(f"🏠 Địa chỉ [{kh.dia_chi}]: ").strip()
            
            if ho_ten:
                kh.ho_ten = ho_ten
            if so_dien_thoai:
                kh.so_dien_thoai = so_dien_thoai
            if email:
                kh.email = email
            if dia_chi:
                kh.dia_chi = dia_chi
            
            print("✅ Cập nhật thông tin thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def delete_khach_hang(self):
        """Xóa khách hàng"""
        self.show_header()
        print("🗑️ XÓA KHÁCH HÀNG")
        print("-" * 30)
        
        try:
            kh_id = int(input("🆔 Nhập ID khách hàng: "))
            
            kh = None
            for i, k in enumerate(self.ql.khach_hangs):
                if k.id == kh_id:
                    kh = k
                    index = i
                    break
            
            if not kh:
                print("❌ Không tìm thấy khách hàng!")
                self.pause()
                return
            
            print(f"📄 Thông tin khách hàng:")
            print(f"   Họ tên: {kh.ho_ten}")
            print(f"   SĐT: {kh.so_dien_thoai}")
            
            # Kiểm tra xem có đơn hàng nào không
            don_hang_count = sum(1 for dh in self.ql.don_hangs if dh.khach_hang_id == kh_id)
            if don_hang_count > 0:
                print(f"⚠️ Cảnh báo: Khách hàng có {don_hang_count} đơn hàng!")
                confirm = input("❓ Bạn có chắc muốn xóa? (y/N): ").strip().lower()
            else:
                confirm = input("❓ Bạn có chắc muốn xóa? (y/N): ").strip().lower()
            
            if confirm == 'y':
                self.ql.khach_hangs.pop(index)
                print("✅ Xóa khách hàng thành công!")
                self.ql.save_data()
            else:
                print("❌ Đã hủy xóa!")
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def menu_dich_vu(self):
        """Menu quản lý dịch vụ"""
        while True:
            self.show_header()
            print("🛠️ QUẢN LÝ DỊCH VỤ")
            print("-" * 30)
            print("1. 📄 Danh sách dịch vụ")
            print("2. ➕ Thêm dịch vụ mới")
            print("3. ✏️ Sửa dịch vụ")
            print("4. 🗑️ Xóa dịch vụ")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-4): ").strip()
            
            if choice == '1':
                self.show_dich_vu_list()
            elif choice == '2':
                self.add_dich_vu()
            elif choice == '3':
                self.edit_dich_vu()
            elif choice == '4':
                self.delete_dich_vu()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def show_dich_vu_list(self):
        """Hiển thị danh sách dịch vụ"""
        self.show_header()
        print("🛠️ DANH SÁCH DỊCH VỤ")
        print("-" * 50)
        
        if not self.ql.dich_vus:
            print("📭 Chưa có dịch vụ nào!")
        else:
            print(f"{'ID':<5} {'Tên dịch vụ':<25} {'Giá':<15} {'Bảo hành':<10}")
            print("-" * 65)
            for dv in self.ql.dich_vus:
                gia_str = f"{dv.gia_ban:,} VNĐ"
                bh_str = f"{dv.thoi_gian_bao_hanh} tháng" if dv.thoi_gian_bao_hanh > 0 else "Không"
                print(f"{dv.id:<5} {dv.ten_dich_vu:<25} {gia_str:<15} {bh_str:<10}")
        
        print(f"\n📊 Tổng số: {len(self.ql.dich_vus)} dịch vụ")
        self.pause()
    
    def add_dich_vu(self):
        """Thêm dịch vụ mới"""
        self.show_header()
        print("➕ THÊM DỊCH VỤ MỚI")
        print("-" * 30)
        
        try:
            ten_dich_vu = input("🛠️ Tên dịch vụ: ").strip()
            if not ten_dich_vu:
                print("❌ Tên dịch vụ không được để trống!")
                self.pause()
                return
            
            # Kiểm tra trùng tên
            for dv in self.ql.dich_vus:
                if dv.ten_dich_vu == ten_dich_vu:
                    print("❌ Dịch vụ đã tồn tại!")
                    self.pause()
                    return
            
            gia_ban = float(input("💰 Giá bán: "))
            if gia_ban < 0:
                print("❌ Giá không được âm!")
                self.pause()
                return
            
            thoi_gian_bao_hanh = int(input("⏰ Thời gian bảo hành (tháng, 0 nếu không có): "))
            mo_ta = input("📝 Mô tả: ").strip()
            
            new_dv = DichVu(
                self.ql.next_id['dich_vu'],
                ten_dich_vu, gia_ban, thoi_gian_bao_hanh, mo_ta
            )
            
            self.ql.dich_vus.append(new_dv)
            self.ql.next_id['dich_vu'] += 1
            
            print(f"✅ Đã thêm dịch vụ {ten_dich_vu} thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ Giá hoặc thời gian bảo hành không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def edit_dich_vu(self):
        """Sửa dịch vụ"""
        self.show_header()
        print("✏️ SỬA DỊCH VỤ")
        print("-" * 30)
        
        try:
            dv_id = int(input("🆔 Nhập ID dịch vụ: "))
            
            dv = None
            for d in self.ql.dich_vus:
                if d.id == dv_id:
                    dv = d
                    break
            
            if not dv:
                print("❌ Không tìm thấy dịch vụ!")
                self.pause()
                return
            
            print(f"📄 Thông tin hiện tại:")
            print(f"   Tên dịch vụ: {dv.ten_dich_vu}")
            print(f"   Giá: {dv.gia_ban:,} VNĐ")
            print(f"   Bảo hành: {dv.thoi_gian_bao_hanh} tháng")
            print(f"   Mô tả: {dv.mo_ta}")
            
            print("\n📝 Nhập thông tin mới (để trống nếu không thay đổi):")
            
            ten_dich_vu = input(f"🛠️ Tên dịch vụ [{dv.ten_dich_vu}]: ").strip()
            gia_str = input(f"💰 Giá [{dv.gia_ban}]: ").strip()
            thoi_gian_str = input(f"⏰ Bảo hành (tháng) [{dv.thoi_gian_bao_hanh}]: ").strip()
            mo_ta = input(f"📝 Mô tả [{dv.mo_ta}]: ").strip()
            
            if ten_dich_vu:
                dv.ten_dich_vu = ten_dich_vu
            if gia_str:
                gia = float(gia_str)
                if gia >= 0:
                    dv.gia_ban = gia
                else:
                    print("⚠️ Giá không hợp lệ, giữ nguyên giá cũ")
            if thoi_gian_str:
                thoi_gian = int(thoi_gian_str)
                if thoi_gian >= 0:
                    dv.thoi_gian_bao_hanh = thoi_gian
                else:
                    print("⚠️ Thời gian bảo hành không hợp lệ, giữ nguyên giá trị cũ")
            if mo_ta:
                dv.mo_ta = mo_ta
            
            print("✅ Cập nhật dịch vụ thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID hoặc giá không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def delete_dich_vu(self):
        """Xóa dịch vụ"""
        self.show_header()
        print("🗑️ XÓA DỊCH VỤ")
        print("-" * 30)
        
        try:
            dv_id = int(input("🆔 Nhập ID dịch vụ: "))
            
            dv = None
            for i, d in enumerate(self.ql.dich_vus):
                if d.id == dv_id:
                    dv = d
                    index = i
                    break
            
            if not dv:
                print("❌ Không tìm thấy dịch vụ!")
                self.pause()
                return
            
            print(f"📄 Thông tin dịch vụ:")
            print(f"   Tên: {dv.ten_dich_vu}")
            print(f"   Giá: {dv.gia_ban:,} VNĐ")
            
            confirm = input("❓ Bạn có chắc muốn xóa? (y/N): ").strip().lower()
            
            if confirm == 'y':
                self.ql.dich_vus.pop(index)
                print("✅ Xóa dịch vụ thành công!")
                self.ql.save_data()
            else:
                print("❌ Đã hủy xóa!")
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def menu_linh_kien(self):
        """Menu quản lý linh kiện"""
        while True:
            self.show_header()
            print("🔩 QUẢN LÝ LINH KIỆN")
            print("-" * 30)
            print("1. 📄 Danh sách linh kiện")
            print("2. ➕ Thêm linh kiện mới")
            print("3. ✏️ Sửa linh kiện")
            print("4. 🗑️ Xóa linh kiện")
            print("5. 📦 Nhập hàng")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-5): ").strip()
            
            if choice == '1':
                self.show_linh_kien_list()
            elif choice == '2':
                self.add_linh_kien()
            elif choice == '3':
                self.edit_linh_kien()
            elif choice == '4':
                self.delete_linh_kien()
            elif choice == '5':
                self.nhap_hang()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def show_linh_kien_list(self):
        """Hiển thị danh sách linh kiện"""
        self.show_header()
        print("🔩 DANH SÁCH LINH KIỆN")
        print("-" * 50)
        
        if not self.ql.linh_kiens:
            print("📭 Chưa có linh kiện nào!")
        else:
            print(f"{'ID':<5} {'Tên linh kiện':<20} {'Mã':<12} {'Tồn':<8} {'Giá bán':<15}")
            print("-" * 70)
            for lk in self.ql.linh_kiens:
                gia_str = f"{lk.gia_ban:,} VNĐ"
                ton_str = str(lk.so_luong_ton)
                print(f"{lk.id:<5} {lk.ten_linh_kien:<20} {lk.ma_linh_kien:<12} {ton_str:<8} {gia_str:<15}")
        
        print(f"\n📊 Tổng số: {len(self.ql.linh_kiens)} linh kiện")
        self.pause()
    
    def add_linh_kien(self):
        """Thêm linh kiện mới"""
        self.show_header()
        print("➕ THÊM LINH KIỆN MỚI")
        print("-" * 30)
        
        try:
            ten_linh_kien = input("🔩 Tên linh kiện: ").strip()
            if not ten_linh_kien:
                print("❌ Tên linh kiện không được để trống!")
                self.pause()
                return
            
            ma_linh_kien = input("🏷️ Mã linh kiện: ").strip()
            if not ma_linh_kien:
                print("❌ Mã linh kiện không được để trống!")
                self.pause()
                return
            
            # Kiểm tra trùng mã
            for lk in self.ql.linh_kiens:
                if lk.ma_linh_kien == ma_linh_kien:
                    print("❌ Mã linh kiện đã tồn tại!")
                    self.pause()
                    return
            
            so_luong_ton = int(input("📦 Số lượng tồn kho: "))
            gia_nhap = float(input("💰 Giá nhập: "))
            gia_ban = float(input("💸 Giá bán: "))
            nha_cung_cap = input("🏭 Nhà cung cấp: ").strip()
            thong_so_ky_thuat = input("📐 Thông số kỹ thuật: ").strip()
            
            new_lk = LinhKien(
                self.ql.next_id['linh_kien'],
                ten_linh_kien, ma_linh_kien, so_luong_ton,
                gia_nhap, gia_ban, nha_cung_cap, thong_so_ky_thuat
            )
            
            self.ql.linh_kiens.append(new_lk)
            self.ql.next_id['linh_kien'] += 1
            
            print(f"✅ Đã thêm linh kiện {ten_linh_kien} thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ Số lượng hoặc giá không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def edit_linh_kien(self):
        """Sửa linh kiện"""
        self.show_header()
        print("✏️ SỬA LINH KIỆN")
        print("-" * 30)
        
        try:
            lk_id = int(input("🆔 Nhập ID linh kiện: "))
            
            lk = None
            for l in self.ql.linh_kiens:
                if l.id == lk_id:
                    lk = l
                    break
            
            if not lk:
                print("❌ Không tìm thấy linh kiện!")
                self.pause()
                return
            
            print(f"📄 Thông tin hiện tại:")
            print(f"   Tên: {lk.ten_linh_kien}")
            print(f"   Mã: {lk.ma_linh_kien}")
            print(f"   Tồn kho: {lk.so_luong_ton}")
            print(f"   Giá nhập: {lk.gia_nhap:,} VNĐ")
            print(f"   Giá bán: {lk.gia_ban:,} VNĐ")
            print(f"   Nhà cung cấp: {lk.nha_cung_cap}")
            
            print("\n📝 Nhập thông tin mới (để trống nếu không thay đổi):")
            
            ten_linh_kien = input(f"🔩 Tên linh kiện [{lk.ten_linh_kien}]: ").strip()
            ma_linh_kien = input(f"🏷️ Mã linh kiện [{lk.ma_linh_kien}]: ").strip()
            ton_str = input(f"📦 Tồn kho [{lk.so_luong_ton}]: ").strip()
            gia_nhap_str = input(f"💰 Giá nhập [{lk.gia_nhap}]: ").strip()
            gia_ban_str = input(f"💸 Giá bán [{lk.gia_ban}]: ").strip()
            nha_cung_cap = input(f"🏭 Nhà cung cấp [{lk.nha_cung_cap}]: ").strip()
            thong_so_ky_thuat = input(f"📐 Thông số kỹ thuật [{lk.thong_so_ky_thuat}]: ").strip()
            
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
            
            print("✅ Cập nhật linh kiện thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID hoặc giá trị không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def delete_linh_kien(self):
        """Xóa linh kiện"""
        self.show_header()
        print("🗑️ XÓA LINH KIỆN")
        print("-" * 30)
        
        try:
            lk_id = int(input("🆔 Nhập ID linh kiện: "))
            
            lk = None
            for i, l in enumerate(self.ql.linh_kiens):
                if l.id == lk_id:
                    lk = l
                    index = i
                    break
            
            if not lk:
                print("❌ Không tìm thấy linh kiện!")
                self.pause()
                return
            
            print(f"📄 Thông tin linh kiện:")
            print(f"   Tên: {lk.ten_linh_kien}")
            print(f"   Mã: {lk.ma_linh_kien}")
            print(f"   Tồn kho: {lk.so_luong_ton}")
            
            if lk.so_luong_ton > 0:
                print(f"⚠️ Cảnh báo: Còn {lk.so_luong_ton} sản phẩm trong kho!")
            
            confirm = input("❓ Bạn có chắc muốn xóa? (y/N): ").strip().lower()
            
            if confirm == 'y':
                self.ql.linh_kiens.pop(index)
                print("✅ Xóa linh kiện thành công!")
                self.ql.save_data()
            else:
                print("❌ Đã hủy xóa!")
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def nhap_hang(self):
        """Nhập hàng linh kiện"""
        self.show_header()
        print("📦 NHẬP HÀNG LINH KIỆN")
        print("-" * 30)
        
        try:
            lk_id = int(input("🆔 Nhập ID linh kiện: "))
            
            lk = None
            for l in self.ql.linh_kiens:
                if l.id == lk_id:
                    lk = l
                    break
            
            if not lk:
                print("❌ Không tìm thấy linh kiện!")
                self.pause()
                return
            
            print(f"📄 Thông tin linh kiện:")
            print(f"   Tên: {lk.ten_linh_kien}")
            print(f"   Tồn kho hiện tại: {lk.so_luong_ton}")
            
            so_luong = int(input("📦 Số lượng nhập: "))
            if so_luong <= 0:
                print("❌ Số lượng phải lớn hơn 0!")
                self.pause()
                return
            
            gia_nhap_moi = input(f"💰 Giá nhập mới [{lk.gia_nhap:,}]: ").strip()
            if gia_nhap_moi:
                gia_nhap = float(gia_nhap_moi)
                if gia_nhap >= 0:
                    lk.gia_nhap = gia_nhap
                else:
                    print("⚠️ Giá nhập không hợp lệ, giữ nguyên giá cũ")
            
            lk.so_luong_ton += so_luong
            
            print(f"✅ Nhập thành công {so_luong} {lk.ten_linh_kien}")
            print(f"📊 Tồn kho mới: {lk.so_luong_ton}")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID hoặc số lượng không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def menu_don_hang(self):
        """Menu quản lý đơn hàng"""
        while True:
            self.show_header()
            print("📋 QUẢN LÝ ĐƠN HÀNG")
            print("-" * 30)
            print("1. 📄 Danh sách đơn hàng")
            print("2. ➕ Tạo đơn hàng mới")
            print("3. 👁️ Chi tiết đơn hàng")
            print("4. ✏️ Cập nhật trạng thái")
            print("5. 🗑️ Xóa đơn hàng")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-5): ").strip()
            
            if choice == '1':
                self.show_don_hang_list()
            elif choice == '2':
                self.add_don_hang()
            elif choice == '3':
                self.show_don_hang_detail()
            elif choice == '4':
                self.update_trang_thai_don_hang()
            elif choice == '5':
                self.delete_don_hang()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def show_don_hang_list(self):
        """Hiển thị danh sách đơn hàng"""
        self.show_header()
        print("📋 DANH SÁCH ĐƠN HÀNG")
        print("-" * 50)
        
        if not self.ql.don_hangs:
            print("📭 Chưa có đơn hàng nào!")
        else:
            print(f"{'ID':<5} {'Mã đơn':<15} {'Khách hàng':<20} {'Thiết bị':<20} {'Trạng thái':<15}")
            print("-" * 85)
            for dh in self.ql.don_hangs:
                kh = next((k for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), None)
                kh_ten = kh.ho_ten if kh else "Unknown"
                
                # Cắt tên nếu quá dài
                ten_tb = dh.ten_thiet_bi[:17] + "..." if len(dh.ten_thiet_bi) > 17 else dh.ten_thiet_bi
                ten_kh = kh_ten[:17] + "..." if len(kh_ten) > 17 else kh_ten
                
                print(f"{dh.id:<5} {dh.ma_don_hang:<15} {ten_kh:<20} {ten_tb:<20} {dh.trang_thai.value:<15}")
        
        print(f"\n📊 Tổng số: {len(self.ql.don_hangs)} đơn hàng")
        self.pause()
    
    def add_don_hang(self):
        """Tạo đơn hàng mới"""
        self.show_header()
        print("➕ TẠO ĐƠN HÀNG MỚI")
        print("-" * 30)
        
        try:
            # Chọn khách hàng
            print("👥 Chọn khách hàng:")
            if not self.ql.khach_hangs:
                print("❌ Chưa có khách hàng nào trong hệ thống!")
                self.pause()
                return
            
            for kh in self.ql.khach_hangs:
                print(f"   {kh.id}. {kh.ho_ten} - {kh.so_dien_thoai}")
            
            kh_id = int(input("🆔 Nhập ID khách hàng: "))
            
            kh = None
            for k in self.ql.khach_hangs:
                if k.id == kh_id:
                    kh = k
                    break
            
            if not kh:
                print("❌ Không tìm thấy khách hàng!")
                self.pause()
                return
            
            # Thông tin thiết bị
            ten_thiet_bi = input("🖥️ Tên thiết bị: ").strip()
            if not ten_thiet_bi:
                print("❌ Tên thiết bị không được để trống!")
                self.pause()
                return
            
            print("\n📱 Loại thiết bị:")
            for i, loai in enumerate(LoaiThietBi, 1):
                print(f"   {i}. {loai.value}")
            
            loai_choice = int(input("🆔 Chọn loại thiết bị (1-6): "))
            if 1 <= loai_choice <= 6:
                loai_thiet_bi = list(LoaiThietBi)[loai_choice - 1]
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
                return
            
            nhan_hieu = input("🏷️ Nhãn hiệu: ").strip()
            model = input("📋 Model: ").strip()
            serial_number = input("🔢 Serial number: ").strip()
            mat_khau = input("🔐 Mật khẩu máy tính (nếu có): ").strip()
            mo_ta_loi = input("🐛 Mô tả lỗi: ").strip()
            
            if not mo_ta_loi:
                print("❌ Mô tả lỗi không được để trống!")
                self.pause()
                return
            
            # Tạo mã đơn hàng
            ma_don_hang = f"DH{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            new_dh = DonHang(
                self.ql.next_id['don_hang'],
                ma_don_hang, kh_id, ten_thiet_bi, loai_thiet_bi, mo_ta_loi
            )
            
            new_dh.nhan_hieu = nhan_hieu
            new_dh.model = model
            new_dh.serial_number = serial_number
            new_dh.mat_khau = mat_khau
            
            self.ql.don_hangs.append(new_dh)
            self.ql.next_id['don_hang'] += 1
            
            print(f"✅ Đã tạo đơn hàng {ma_don_hang} thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID hoặc lựa chọn không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def show_don_hang_detail(self):
        """Hiển thị chi tiết đơn hàng"""
        self.show_header()
        print("👁️ CHI TIẾT ĐƠN HÀNG")
        print("-" * 30)
        
        try:
            dh_id = int(input("🆔 Nhập ID đơn hàng: "))
            
            dh = None
            for d in self.ql.don_hangs:
                if d.id == dh_id:
                    dh = d
                    break
            
            if not dh:
                print("❌ Không tìm thấy đơn hàng!")
                self.pause()
                return
            
            kh = next((k for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), None)
            
            print(f"📋 THÔNG TIN ĐƠN HÀNG")
            print("=" * 50)
            print(f"🆔 Mã đơn hàng: {dh.ma_don_hang}")
            print(f"📅 Ngày tiếp nhận: {dh.ngay_tiep_nhan.strftime('%d/%m/%Y %H:%M')}")
            print(f"👤 Khách hàng: {kh.ho_ten if kh else 'Unknown'}")
            print(f"📱 SĐT: {kh.so_dien_thoai if kh else 'N/A'}")
            
            print(f"\n🖥️ THÔNG TIN THIẾT BỊ")
            print("-" * 30)
            print(f"📱 Tên thiết bị: {dh.ten_thiet_bi}")
            print(f"🏷️ Loại: {dh.loai_thiet_bi.value}")
            print(f"🏭 Nhãn hiệu: {dh.nhan_hieu}")
            print(f"📋 Model: {dh.model}")
            print(f"🔢 Serial: {dh.serial_number}")
            
            print(f"\n🐛 MÔ TẢ LỖI")
            print("-" * 30)
            print(dh.mo_ta_loi)
            
            print(f"\n📊 TRẠNG THÁI")
            print("-" * 30)
            print(f"🔄 Trạng thái: {dh.trang_thai.value}")
            print(f"💳 Thanh toán: {dh.trang_thai_thanh_toan.value}")
            print(f"💰 Tổng tiền: {dh.tong_tien:,} VNĐ")
            print(f"💸 Đặt cọc: {dh.tien_dat_coc:,} VNĐ")
            
            if dh.ngay_hoan_thanh:
                print(f"✅ Ngày hoàn thành: {dh.ngay_hoan_thanh.strftime('%d/%m/%Y %H:%M')}")
            
            if dh.ghi_chu_nhan_vien:
                print(f"\n📝 GHI CHÚ NHÂN VIÊN")
                print("-" * 30)
                print(dh.ghi_chu_nhan_vien)
            
            if dh.ghi_chu_khach_hang:
                print(f"\n💬 GHI CHÚ KHÁCH HÀNG")
                print("-" * 30)
                print(dh.ghi_chu_khach_hang)
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def update_trang_thai_don_hang(self):
        """Cập nhật trạng thái đơn hàng"""
        self.show_header()
        print("✏️ CẬP NHẬT TRẠNG THÁI ĐƠN HÀNG")
        print("-" * 30)
        
        try:
            dh_id = int(input("🆔 Nhập ID đơn hàng: "))
            
            dh = None
            for d in self.ql.don_hangs:
                if d.id == dh_id:
                    dh = d
                    break
            
            if not dh:
                print("❌ Không tìm thấy đơn hàng!")
                self.pause()
                return
            
            print(f"📄 Đơn hàng: {dh.ma_don_hang}")
            print(f"🔄 Trạng thái hiện tại: {dh.trang_thai.value}")
            print(f"💳 Thanh toán hiện tại: {dh.trang_thai_thanh_toan.value}")
            
            print("\n🔄 Chọn trạng thái mới:")
            for i, trang_thai in enumerate(TrangThaiDonHang, 1):
                print(f"   {i}. {trang_thai.value}")
            
            trang_thai_choice = int(input("🆔 Chọn trạng thái (1-7): "))
            if 1 <= trang_thai_choice <= 7:
                trang_thai_moi = list(TrangThaiDonHang)[trang_thai_choice - 1]
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
                return
            
            print("\n💳 Chọn trạng thái thanh toán:")
            for i, trang_thai_tt in enumerate(TrangThaiThanhToan, 1):
                print(f"   {i}. {trang_thai_tt.value}")
            
            tt_choice = int(input("🆔 Chọn trạng thái thanh toán (1-3): "))
            if 1 <= tt_choice <= 3:
                tt_moi = list(TrangThaiThanhToan)[tt_choice - 1]
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
                return
            
            # Cập nhật ngày hoàn thành nếu trạng thái là hoàn thành
            if trang_thai_moi == TrangThaiDonHang.HOAN_THANH and dh.trang_thai != TrangThaiDonHang.HOAN_THANH:
                dh.ngay_hoan_thanh = datetime.now()
            
            dh.trang_thai = trang_thai_moi
            dh.trang_thai_thanh_toan = tt_moi
            
            # Cập nhật tổng tiền nếu thanh toán
            if tt_moi == TrangThaiThanhToan.DA_THANH_TOAN:
                try:
                    tong_tien = float(input("💰 Nhập tổng tiền: "))
                    if tong_tien >= 0:
                        dh.tong_tien = tong_tien
                    else:
                        print("⚠️ Tổng tiền không hợp lệ")
                except ValueError:
                    print("⚠️ Tổng tiền không hợp lệ, giữ nguyên giá cũ")
            
            print("✅ Cập nhật trạng thái thành công!")
            self.ql.save_data()
            
        except ValueError:
            print("❌ ID hoặc lựa chọn không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def delete_don_hang(self):
        """Xóa đơn hàng"""
        self.show_header()
        print("🗑️ XÓA ĐƠN HÀNG")
        print("-" * 30)
        
        try:
            dh_id = int(input("🆔 Nhập ID đơn hàng: "))
            
            dh = None
            for i, d in enumerate(self.ql.don_hangs):
                if d.id == dh_id:
                    dh = d
                    index = i
                    break
            
            if not dh:
                print("❌ Không tìm thấy đơn hàng!")
                self.pause()
                return
            
            print(f"📄 Thông tin đơn hàng:")
            print(f"   Mã đơn: {dh.ma_don_hang}")
            print(f"   Khách hàng: {next((k.ho_ten for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), 'Unknown')}")
            print(f"   Thiết bị: {dh.ten_thiet_bi}")
            print(f"   Trạng thái: {dh.trang_thai.value}")
            
            if dh.trang_thai == TrangThaiDonHang.HOAN_THANH:
                print("⚠️ Cảnh báo: Đơn hàng đã hoàn thành!")
            elif dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN:
                print("⚠️ Cảnh báo: Đơn hàng đã thanh toán!")
            
            confirm = input("❓ Bạn có chắc muốn xóa? (y/N): ").strip().lower()
            
            if confirm == 'y':
                self.ql.don_hangs.pop(index)
                print("✅ Xóa đơn hàng thành công!")
                self.ql.save_data()
            else:
                print("❌ Đã hủy xóa!")
            
        except ValueError:
            print("❌ ID không hợp lệ!")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
        
        self.pause()
    
    def menu_thong_ke(self):
        """Menu thống kê"""
        while True:
            self.show_header()
            print("📊 THỐNG KÊ & BÁO CÁO")
            print("-" * 30)
            print("1. 📈 Tổng quan")
            print("2. 📋 Thống kê đơn hàng")
            print("3. 💰 Doanh thu")
            print("4. 🔍 Tìm kiếm")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-4): ").strip()
            
            if choice == '1':
                self.show_tong_quan()
            elif choice == '2':
                self.show_thong_ke_don_hang()
            elif choice == '3':
                self.show_doanh_thu()
            elif choice == '4':
                self.menu_tim_kiem()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def show_tong_quan(self):
        """Hiển thị tổng quan"""
        self.show_header()
        print("📈 TỔNG QUAN HỆ THỐNG")
        print("=" * 50)
        
        # Thống kê cơ bản
        tong_kh = len(self.ql.khach_hangs)
        tong_dv = len(self.ql.dich_vus)
        tong_lk = len(self.ql.linh_kiens)
        tong_dh = len(self.ql.don_hangs)
        
        print(f"👥 Tổng số khách hàng: {tong_kh}")
        print(f"🛠️ Tổng số dịch vụ: {tong_dv}")
        print(f"🔩 Tổng số linh kiện: {tong_lk}")
        print(f"📋 Tổng số đơn hàng: {tong_dh}")
        
        # Thống kê đơn hàng theo trạng thái
        print(f"\n📊 THỐNG KÊ ĐƠN HÀNG THEO TRẠNG THÁI")
        print("-" * 40)
        for trang_thai in TrangThaiDonHang:
            count = sum(1 for dh in self.ql.don_hangs if dh.trang_thai == trang_thai)
            print(f"   {trang_thai.value}: {count}")
        
        # Thống kê thanh toán
        print(f"\n💳 THỐNG KÊ THANH TOÁN")
        print("-" * 30)
        for tt in TrangThaiThanhToan:
            count = sum(1 for dh in self.ql.don_hangs if dh.trang_thai_thanh_toan == tt)
            print(f"   {tt.value}: {count}")
        
        # Top 5 khách hàng có nhiều đơn hàng nhất
        print(f"\n🏆 TOP 5 KHÁCH HÀNG NHIỀU ĐƠN HÀNG NHẤT")
        print("-" * 50)
        kh_stats = {}
        for kh in self.ql.khach_hangs:
            count = sum(1 for dh in self.ql.don_hangs if dh.khach_hang_id == kh.id)
            if count > 0:
                kh_stats[kh.ho_ten] = count
        
        sorted_kh = sorted(kh_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (ten, count) in enumerate(sorted_kh, 1):
            print(f"   {i}. {ten}: {count} đơn hàng")
        
        # Tổng giá trị kho
        tong_gia_tri_kho = sum(lk.gia_nhap * lk.so_luong_ton for lk in self.ql.linh_kiens)
        print(f"\n💰 TỔNG GIÁ TRỊ KHO: {tong_gia_tri_kho:,} VNĐ")
        
        # Doanh thu ước tính
        doanh_thu = sum(dh.tong_tien for dh in self.ql.don_hangs if dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN)
        print(f"💸 DOANH THU ĐÃ THANH TOÁN: {doanh_thu:,} VNĐ")
        
        self.pause()
    
    def show_thong_ke_don_hang(self):
        """Thống kê chi tiết đơn hàng"""
        self.show_header()
        print("📋 THỐNG KÊ CHI TIẾT ĐƠN HÀNG")
        print("=" * 50)
        
        # Thống kê theo loại thiết bị
        print("📱 THỐNG KÊ THEO LOẠI THIẾT BỊ")
        print("-" * 40)
        loai_stats = {}
        for loai in LoaiThietBi:
            count = sum(1 for dh in self.ql.don_hangs if dh.loai_thiet_bi == loai)
            if count > 0:
                loai_stats[loai.value] = count
        
        for loai, count in sorted(loai_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   {loai}: {count}")
        
        # Đơn hàng gần đây
        print(f"\n📅 5 ĐƠN HÀNG GẦN ĐÂY NHẤT")
        print("-" * 50)
        recent_dh = sorted(self.ql.don_hangs, key=lambda x: x.ngay_tiep_nhan, reverse=True)[:5]
        
        for dh in recent_dh:
            kh = next((k for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), None)
            print(f"   {dh.ma_don_hang} - {kh.ho_ten if kh else 'Unknown'} - {dh.trang_thai.value}")
        
        self.pause()
    
    def show_doanh_thu(self):
        """Hiển thị doanh thu"""
        self.show_header()
        print("💰 BÁO CÁO DOANH THU")
        print("=" * 50)
        
        # Doanh thu theo trạng thái thanh toán
        print("💳 DOANH THU THEO TRẠNG THÁI THANH TOÁN")
        print("-" * 50)
        for tt in TrangThaiThanhToan:
            don_hangs_tt = [dh for dh in self.ql.don_hangs if dh.trang_thai_thanh_toan == tt]
            tong_tien = sum(dh.tong_tien for dh in don_hangs_tt)
            print(f"   {tt.value}: {len(don_hangs_tt)} đơn - {tong_tien:,} VNĐ")
        
        # Doanh thu theo tháng
        print(f"\n📅 DOANH THU THEO THÁNG")
        print("-" * 40)
        thang_stats = {}
        for dh in self.ql.don_hangs:
            if dh.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN:
                thang = dh.ngay_tiep_nhan.strftime('%Y-%m')
                if thang not in thang_stats:
                    thang_stats[thang] = 0
                thang_stats[thang] += dh.tong_tien
        
        for thang, doanh_thu in sorted(thang_stats.items(), reverse=True):
            print(f"   {thang}: {doanh_thu:,} VNĐ")
        
        # Dịch vụ được sử dụng nhiều nhất
        print(f"\n🛠️ DỊCH VỤ ĐƯỢC SỬ DỤNG NHIỀU NHẤT")
        print("-" * 45)
        # (Đây là thống kê giả định vì chưa có chi tiết đơn hàng - dịch vụ)
        print("   (Chức năng đang phát triển)")
        
        self.pause()
    
    def menu_tim_kiem(self):
        """Menu tìm kiếm"""
        while True:
            self.show_header()
            print("🔍 TÌM KIẾM")
            print("-" * 30)
            print("1. 👥 Tìm khách hàng")
            print("2. 📋 Tìm đơn hàng")
            print("3. 🔩 Tìm linh kiện")
            print("0. 🔙 Quay lại")
            print("-" * 30)
            
            choice = input("👉 Chọn chức năng (0-3): ").strip()
            
            if choice == '1':
                self.search_khach_hang()
            elif choice == '2':
                self.search_don_hang()
            elif choice == '3':
                self.search_linh_kien()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
                self.pause()
    
    def search_don_hang(self):
        """Tìm kiếm đơn hàng"""
        self.show_header()
        print("🔍 TÌM KIẾM ĐƠN HÀNG")
        print("-" * 30)
        
        keyword = input("🔎 Nhập từ khóa (Mã đơn, tên thiết bị, tên KH): ").strip().lower()
        
        if not keyword:
            print("❌ Vui lòng nhập từ khóa tìm kiếm!")
            self.pause()
            return
        
        results = []
        for dh in self.ql.don_hangs:
            kh = next((k for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), None)
            kh_ten = kh.ho_ten.lower() if kh else ""
            
            if (keyword in dh.ma_don_hang.lower() or 
                keyword in dh.ten_thiet_bi.lower() or 
                keyword in kh_ten):
                results.append(dh)
        
        self.show_header()
        print(f"🔍 KẾT QUẢ TÌM KIẾM: '{keyword}'")
        print("-" * 50)
        
        if not results:
            print("📭 Không tìm thấy đơn hàng nào!")
        else:
            print(f"{'ID':<5} {'Mã đơn':<15} {'Khách hàng':<20} {'Thiết bị':<20} {'Trạng thái':<15}")
            print("-" * 85)
            for dh in results:
                kh = next((k for k in self.ql.khach_hangs if k.id == dh.khach_hang_id), None)
                kh_ten = kh.ho_ten if kh else "Unknown"
                
                ten_tb = dh.ten_thiet_bi[:17] + "..." if len(dh.ten_thiet_bi) > 17 else dh.ten_thiet_bi
                ten_kh = kh_ten[:17] + "..." if len(kh_ten) > 17 else kh_ten
                
                print(f"{dh.id:<5} {dh.ma_don_hang:<15} {ten_kh:<20} {ten_tb:<20} {dh.trang_thai.value:<15}")
        
        print(f"\n📊 Tìm thấy {len(results)} kết quả")
        self.pause()
    
    def search_linh_kien(self):
        """Tìm kiếm linh kiện"""
        self.show_header()
        print("🔍 TÌM KIẾM LINH KIỆN")
        print("-" * 30)
        
        keyword = input("🔎 Nhập từ khóa (Tên, mã, nhà cung cấp): ").strip().lower()
        
        if not keyword:
            print("❌ Vui lòng nhập từ khóa tìm kiếm!")
            self.pause()
            return
        
        results = []
        for lk in self.ql.linh_kiens:
            if (keyword in lk.ten_linh_kien.lower() or 
                keyword in lk.ma_linh_kien.lower() or 
                keyword in lk.nha_cung_cap.lower()):
                results.append(lk)
        
        self.show_header()
        print(f"🔍 KẾT QUẢ TÌM KIẾM: '{keyword}'")
        print("-" * 50)
        
        if not results:
            print("📭 Không tìm thấy linh kiện nào!")
        else:
            print(f"{'ID':<5} {'Tên linh kiện':<20} {'Mã':<12} {'Tồn':<8} {'Giá bán':<15}")
            print("-" * 70)
            for lk in results:
                gia_str = f"{lk.gia_ban:,} VNĐ"
                print(f"{lk.id:<5} {lk.ten_linh_kien:<20} {lk.ma_linh_kien:<12} {lk.so_luong_ton:<8} {gia_str:<15}")
        
        print(f"\n📊 Tìm thấy {len(results)} kết quả")
        self.pause()

if __name__ == "__main__":
    menu = PCMenu()
    menu.show_main_menu()
