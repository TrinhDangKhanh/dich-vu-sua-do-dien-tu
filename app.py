from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

from database_improved import db, KhachHang, DichVu, LinhKien, DonHang, ChiTietDonHang, ChiTietLinhKien, NhanVien, TrangThaiDonHang, TrangThaiThanhToan, LoaiThietBi, NhapKho, LichSuDonHang, BaoCao, CaiDat, LichSuHoatDong, PhanQuyen
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Khởi tạo database
    db.init_app(app)
    
    # Khởi tạo login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'dang_nhap'
    
    @login_manager.user_loader
    def load_user(user_id):
        # Thử tìm admin/nhân viên trước
        user = NhanVien.query.get(int(user_id))
        if user:
            return user
        # Nếu không tìm thấy, thử tìm khách hàng
        return KhachHang.query.get(int(user_id))
    
    # Tạo database và admin mặc định
    with app.app_context():
        db.create_all()
        
        # Tạo admin mặc định nếu chưa có
        admin = NhanVien.query.filter_by(tai_khoan='admin').first()
        if not admin:
            admin = NhanVien(
                ho_ten='Quản trị viên',
                tai_khoan='admin',
                email='admin@pccare.com',
                vai_tro=PhanQuyen.ADMIN
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Thêm một số dịch vụ mẫu
            dich_vus = [
                DichVu(ma_dich_vu='DV001', ten_dich_vu='Cài đặt Windows', gia_ban=200000, thoi_gian_bao_hanh=1, mo_ta='Cài đặt Windows 10/11, driver và phần mềm cơ bản', loai_dich_vu='sua_chua'),
                DichVu(ma_dich_vu='DV002', ten_dich_vu='Vệ sinh máy tính', gia_ban=150000, thoi_gian_bao_hanh=0, mo_ta='Vệ sinh tổng quát, tản nhiệt, keo tản nhiệt', loai_dich_vu='bao_trih'),
                DichVu(ma_dich_vu='DV003', ten_dich_vu='Thay keo tản nhiệt', gia_ban=250000, thoi_gian_bao_hanh=3, mo_ta='Thay keo tản nhiệt cho CPU/GPU', loai_dich_vu='sua_chua'),
                DichVu(ma_dich_vu='DV004', ten_dich_vu='Nâng cấp RAM', gia_ban=100000, thoi_gian_bao_hanh=36, mo_ta='Nâng cấp RAM laptop, PC', loai_dich_vu='cap_nhat'),
                DichVu(ma_dich_vu='DV005', ten_dich_vu='Thay SSD', gia_ban=100000, thoi_gian_bao_hanh=36, mo_ta='Thay SSD, cài đặt hệ điều hành', loai_dich_vu='cap_nhat'),
                DichVu(ma_dich_vu='DV006', ten_dich_vu='Thay màn hình Laptop', gia_ban=1500000, thoi_gian_bao_hanh=6, mo_ta='Thay màn hình LCD, LED cho laptop', loai_dich_vu='sua_chua'),
                DichVu(ma_dich_vu='DV007', ten_dich_vu='Sửa chữa Mainboard', gia_ban=500000, thoi_gian_bao_hanh=3, mo_ta='Sửa chữa các lỗi mainboard, chipset', loai_dich_vu='sua_chua'),
                DichVu(ma_dich_vu='DV008', ten_dich_vu='Cứu dữ liệu', gia_ban=800000, thoi_gian_bao_hanh=0, mo_ta='Cứu dữ liệu từ ổ cứng hỏng, format', loai_dich_vu='sua_chua'),
            ]
            
            for dv in dich_vus:
                if not DichVu.query.filter_by(ten_dich_vu=dv.ten_dich_vu).first():
                    db.session.add(dv)
            
            # Thêm khách hàng mẫu
            khach_hangs = [
                KhachHang(ma_khach_hang='KH001', ho_ten='Nguyễn Văn An', so_dien_thoai='0912345678', email='an.nguyen@email.com', dia_chi='Hà Nội', gioi_tinh='Nam', cong_ty='Công ty ABC'),
                KhachHang(ma_khach_hang='KH002', ho_ten='Trần Thị Bình', so_dien_thoai='0987654321', email='binh.tran@email.com', dia_chi='TP. Hồ Chí Minh', gioi_tinh='Nữ', cong_ty='Công ty XYZ'),
                KhachHang(ma_khach_hang='KH003', ho_ten='Lê Văn Cường', so_dien_thoai='0934567890', email='cuong.le@email.com', dia_chi='Đà Nẵng', gioi_tinh='Nam', cong_ty='Công ty DEF'),
                KhachHang(ma_khach_hang='KH004', ho_ten='Phạm Thị Dung', so_dien_thoai='0967890123', email='dung.pham@email.com', dia_chi='Hải Phòng', gioi_tinh='Nữ', loai_khach_hang='doanh_nghiep'),
                KhachHang(ma_khach_hang='KH005', ho_ten='Hoàng Văn Em', so_dien_thoai='0978901234', email='em.hoang@email.com', dia_chi='Cần Thơ', gioi_tinh='Nam', loai_khach_hang='ca_nhan'),
                KhachHang(ma_khach_hang='KH006', ho_ten='Đặng Thị Fan', so_dien_thoai='0901234567', email='fan.dang@email.com', dia_chi='Hà Nội', gioi_tinh='Nữ', cong_ty='Freelancer'),
                KhachHang(ma_khach_hang='KH007', ho_ten='Ngô Văn Giàu', so_dien_thoai='0923456789', email='giau.ngo@email.com', dia_chi='TP. Hồ Chí Minh', gioi_tinh='Nam', loai_khach_hang='doanh_nghiep'),
                KhachHang(ma_khach_hang='KH008', ho_ten='Bùi Thị Hương', so_dien_thoai='0945678901', email='huong.bui@email.com', dia_chi='Huế', gioi_tinh='Nữ', loai_khach_hang='ca_nhan'),
            ]
            
            for kh in khach_hangs:
                if not KhachHang.query.filter_by(so_dien_thoai=kh.so_dien_thoai).first():
                    db.session.add(kh)
            
            # Thêm linh kiện mẫu
            linh_kiens = [
                LinhKien(ma_linh_kien='LK001', ten_linh_kien='RAM DDR4 8GB', so_luong_ton=50, gia_nhap=800000, gia_ban=1200000, nha_cung_cap='Kingston', loai_linh_kien='RAM'),
                LinhKien(ma_linh_kien='LK002', ten_linh_kien='RAM DDR4 16GB', so_luong_ton=30, gia_nhap=1500000, gia_ban=2200000, nha_cung_cap='Corsair', loai_linh_kien='RAM'),
                LinhKien(ma_linh_kien='LK003', ten_linh_kien='SSD 240GB SATA', so_luong_ton=25, gia_nhap=600000, gia_ban=950000, nha_cung_cap='Samsung', loai_linh_kien='SSD'),
                LinhKien(ma_linh_kien='LK004', ten_linh_kien='SSD 480GB SATA', so_luong_ton=20, gia_nhap=1000000, gia_ban=1650000, nha_cung_cap='Crucial', loai_linh_kien='SSD'),
                LinhKien(ma_linh_kien='LK005', ten_linh_kien='SSD NVMe 500GB', so_luong_ton=15, gia_nhap=1500000, gia_ban=2400000, nha_cung_cap='Western Digital', loai_linh_kien='SSD'),
                LinhKien(ma_linh_kien='LK006', ten_linh_kien='Màn hình Laptop 14"', so_luong_ton=10, gia_nhap=2000000, gia_ban=3200000, nha_cung_cap='LG', loai_linh_kien='Man_hinh'),
                LinhKien(ma_linh_kien='LK007', ten_linh_kien='Màn hình Laptop 15.6"', so_luong_ton=8, gia_nhap=2500000, gia_ban=3800000, nha_cung_cap='AU Optronics', loai_linh_kien='Man_hinh'),
                LinhKien(ma_linh_kien='LK008', ten_linh_kien='Keo tản nhiệt', so_luong_ton=100, gia_nhap=50000, gia_ban=100000, nha_cung_cap='Arctic Silver', loai_linh_kien='Phu_kien'),
                LinhKien(ma_linh_kien='LK009', ten_linh_kien='Pin Laptop 6 Cell', so_luong_ton=20, gia_nhap=300000, gia_ban=550000, nha_cung_cap='Battery Pro', loai_linh_kien='Pin'),
                LinhKien(ma_linh_kien='LK010', ten_linh_kien='Sạc Laptop 65W', so_luong_ton=30, gia_nhap=150000, gia_ban=280000, nha_cung_cap='Anker', loai_linh_kien='Sac'),
            ]
            
            for lk in linh_kiens:
                if not LinhKien.query.filter_by(ma_linh_kien=lk.ma_linh_kien).first():
                    db.session.add(lk)
            
            db.session.flush()  # Lấy ID của các đối tượng vừa thêm
            
            # Thêm một số đơn hàng mẫu
            don_hang_mau = [
                DonHang(
                    ma_don_hang='DH20240501001',
                    khach_hang_id=1,
                    nhan_vien_id=1,  # admin xử lý
                    ten_thiet_bi='Dell XPS 15',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='Dell',
                    model='XPS 9570',
                    serial_number='DLXPS957001',
                    mo_ta_loi='Máy chạy chậm, nóng, cần vệ sinh và nâng cấp',
                    trang_thai=TrangThaiDonHang.DANG_XU_LY,
                    trang_thai_thanh_toan=TrangThaiThanhToan.CHUA_THANH_TOAN,
                    tong_tien=1350000,
                    ngay_hen_tra=datetime.utcnow() + timedelta(days=3)
                ),
                DonHang(
                    ma_don_hang='DH20240501002',
                    khach_hang_id=2,
                    nhan_vien_id=1,
                    ten_thiet_bi='Macbook Pro 13"',
                    loai_thiet_bi=LoaiThietBi.MACBOOK,
                    nhan_hieu='Apple',
                    model='Macbook Pro 2020',
                    serial_number='MBP2020001',
                    mo_ta_loi='Màn hình bị sọc, cần thay màn hình mới',
                    trang_thai=TrangThaiDonHang.CHO_LINH_KIEN,
                    trang_thai_thanh_toan=TrangThaiThanhToan.DA_DAT_COC,
                    tong_tien=3200000,
                    tien_dat_coc=1600000,
                    ngay_hen_tra=datetime.utcnow() + timedelta(days=7)
                ),
                DonHang(
                    ma_don_hang='DH20240501003',
                    khach_hang_id=3,
                    nhan_vien_id=1,
                    ten_thiet_bi='PC Gaming',
                    loai_thiet_bi=LoaiThietBi.PC_DESKTOP,
                    nhan_hieu='Custom',
                    model='Gaming PC',
                    serial_number='PCG001',
                    mo_ta_loi='Máy không lên nguồn, cần kiểm tra main',
                    trang_thai=TrangThaiDonHang.HOAN_THANH,
                    trang_thai_thanh_toan=TrangThaiThanhToan.DA_THANH_TOAN,
                    tong_tien=500000,
                    ngay_hoan_thanh=datetime.utcnow() - timedelta(days=2),
                    ngay_giao_hang=datetime.utcnow() - timedelta(days=1),
                    ghi_chu_nhan_vien='Sửa thành công mainboard, khách hàng hài lòng',
                    danh_gia_khach_hang=5
                ),
                DonHang(
                    ma_don_hang='DH20240501004',
                    khach_hang_id=4,
                    nhan_vien_id=1,
                    ten_thiet_bi='HP Envy 13',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='HP',
                    model='Envy 13-ad001',
                    serial_number='HPENV13001',
                    mo_ta_loi='Cần cài đặt lại Windows và phần mềm văn phòng',
                    trang_thai=TrangThaiDonHang.DANG_XU_LY,
                    trang_thai_thanh_toan=TrangThaiThanhToan.CHUA_THANH_TOAN,
                    tong_tien=200000,
                    ngay_hen_tra=datetime.utcnow() + timedelta(days=2)
                ),
                DonHang(
                    ma_don_hang='DH20240501005',
                    khach_hang_id=5,
                    nhan_vien_id=1,
                    ten_thiet_bi='Asus ROG Strix',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='Asus',
                    model='ROG Strix G15',
                    serial_number='ASUSROG001',
                    mo_ta_loi='Nâng cấp RAM từ 8GB lên 16GB',
                    trang_thai=TrangThaiDonHang.HOAN_THANH,
                    trang_thai_thanh_toan=TrangThaiThanhToan.DA_THANH_TOAN,
                    tong_tien=1100000,
                    ngay_hoan_thanh=datetime.utcnow() - timedelta(days=5),
                    ngay_giao_hang=datetime.utcnow() - timedelta(days=4),
                    ghi_chu_nhan_vien='Nâng cấp RAM thành công, máy chạy nhanh hơn',
                    danh_gia_khach_hang=4
                ),
            ]
            
            for dh in don_hang_mau:
                if not DonHang.query.filter_by(ma_don_hang=dh.ma_don_hang).first():
                    db.session.add(dh)
            
            db.session.commit()
    
    # Routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            # Kiểm tra xem là admin/nhân viên hay khách hàng
            if current_user.__class__.__name__ == 'NhanVien':  # Admin/nhân viên
                return redirect(url_for('dashboard'))
            else:  # Khách hàng
                return redirect(url_for('dashboard_khach_hang'))
        
        # Hiển thị trang chủ với hero section
        return render_template('base.html')
    
    @app.route('/dang-nhap', methods=['GET', 'POST'])
    def dang_nhap():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        if request.method == 'POST':
            tai_khoan = request.form.get('tai_khoan')
            mat_khau = request.form.get('mat_khau')
            
            user = NhanVien.query.filter_by(tai_khoan=tai_khoan).first()
            
            if user and check_password_hash(user.mat_khau, mat_khau):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Tài khoản hoặc mật khẩu không đúng!', 'danger')
        
        return render_template('dang_nhap.html')
    
    @app.route('/dang-xuat')
    @login_required
    def dang_xuat():
        logout_user()
        return redirect(url_for('dang_nhap'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Thống kê tổng quan
        tong_don_hang = DonHang.query.count()
        don_hang_dang_xu_ly = DonHang.query.filter_by(trang_thai=TrangThaiDonHang.DANG_XU_LY).count()
        don_hang_cho_lin_kien = DonHang.query.filter_by(trang_thai=TrangThaiDonHang.CHO_LINH_KIEN).count()
        don_hang_hoan_thanh = DonHang.query.filter_by(trang_thai=TrangThaiDonHang.HOAN_THANH).count()
        
        # Doanh thu tháng này
        thang_hien_tai = datetime.now().month
        nam_hien_tai = datetime.now().year
        doanh_thu_thang = db.session.query(db.func.sum(DonHang.tong_tien)).filter(
            db.extract('month', DonHang.ngay_tiep_nhan) == thang_hien_tai,
            db.extract('year', DonHang.ngay_tiep_nhan) == nam_hien_tai,
            DonHang.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN
        ).scalar() or 0
        
        # Đơn hàng gần đây
        don_hang_gan_day = DonHang.query.order_by(DonHang.ngay_tiep_nhan.desc()).limit(6).all()
        
        return render_template('dashboard.html',
                             tong_don_hang=tong_don_hang,
                             don_hang_dang_xu_ly=don_hang_dang_xu_ly,
                             don_hang_cho_lin_kien=don_hang_cho_lin_kien,
                             don_hang_hoan_thanh=don_hang_hoan_thanh,
                             doanh_thu_thang=doanh_thu_thang,
                             don_hang_gan_day=don_hang_gan_day)
    
    @app.route('/don-hang')
    @login_required
    def danh_sach_don_hang():
        page = request.args.get('page', 1, type=int)
        trang_thai = request.args.get('trang_thai', '')
        
        query = DonHang.query
        
        if trang_thai:
            query = query.filter_by(trang_thai=trang_thai)
        
        don_hang = query.order_by(DonHang.ngay_tiep_nhan.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        return render_template('don_hang/danh_sach.html', don_hang=don_hang, trang_thai=trang_thai)
    
    @app.route('/don-hang/tao-moi', methods=['GET', 'POST'])
    def tao_don_hang():
        if request.method == 'POST':
            # Lấy thông tin khách hàng
            ho_ten = request.form.get('ho_ten')
            so_dien_thoai = request.form.get('so_dien_thoai')
            email = request.form.get('email')
            dia_chi = request.form.get('dia_chi')
            
            # Kiểm tra khách hàng đã tồn tại
            khach_hang = KhachHang.query.filter_by(so_dien_thoai=so_dien_thoai).first()
            if not khach_hang:
                # Tạo mã khách hàng tự động
                so_khach_hang = KhachHang.query.count() + 1
                ma_khach_hang = f"KH{so_khach_hang:03d}"
                
                khach_hang = KhachHang(
                    ma_khach_hang=ma_khach_hang,
                    ho_ten=ho_ten,
                    so_dien_thoai=so_dien_thoai,
                    email=email,
                    dia_chi=dia_chi
                )
                db.session.add(khach_hang)
                db.session.flush()  # Lấy ID khách hàng
            
            # Tạo mã đơn hàng
            ma_don_hang = f"DH{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Lấy thông tin thiết bị
            ten_thiet_bi = request.form.get('ten_thiet_bi')
            loai_thiet_bi = request.form.get('loai_thiet_bi')
            nhan_hieu = request.form.get('nhan_hieu')
            model = request.form.get('model')
            serial_number = request.form.get('serial_number')
            mat_khau = request.form.get('mat_khau')
            mo_ta_loi = request.form.get('mo_ta_loi')
            
            # Map form values to enum values
            loai_thiet_bi_mapping = {
                'Laptop': LoaiThietBi.LAPTOP,
                'PC Desktop': LoaiThietBi.PC_DESKTOP,
                'Macbook': LoaiThietBi.MACBOOK,
                'Máy in': LoaiThietBi.MAY_IN,
                'Màn hình': LoaiThietBi.MAN_HINH,
                'Khác': LoaiThietBi.KHAC
            }
            
            # Get the enum value for device type
            loai_thiet_bi_enum = loai_thiet_bi_mapping.get(loai_thiet_bi, LoaiThietBi.KHAC)
            
            # Tạo đơn hàng
            don_hang = DonHang(
                ma_don_hang=ma_don_hang,
                khach_hang_id=khach_hang.id,
                ten_thiet_bi=ten_thiet_bi,
                loai_thiet_bi=loai_thiet_bi_enum,
                nhan_hieu=nhan_hieu,
                model=model,
                serial_number=serial_number,
                mat_khau=mat_khau,
                mo_ta_loi=mo_ta_loi,
                trang_thai=TrangThaiDonHang.DANG_XU_LY
            )
            
            db.session.add(don_hang)
            db.session.commit()
            
            flash('Tạo đơn hàng thành công!', 'success')
            return redirect(url_for('danh_sach_don_hang'))
        
        return render_template('don_hang/tao_moi.html')
    
    @app.route('/don-hang/<int:id>')
    @login_required
    def chi_tiet_don_hang(id):
        don_hang = DonHang.query.get_or_404(id)
        return render_template('don_hang/chi_tiet.html', don_hang=don_hang)
    
    @app.route('/don-hang/<int:id>/cap-nhat-trang-thai', methods=['POST'])
    @login_required
    def cap_nhat_trang_thai_don_hang(id):
        don_hang = DonHang.query.get_or_404(id)
        trang_thai_moi = request.form.get('trang_thai')
        
        don_hang.trang_thai = TrangThaiDonHang(trang_thai_moi)
        
        if trang_thai_moi == TrangThaiDonHang.HOAN_THANH.value:
            don_hang.ngay_hoan_thanh = datetime.utcnow()
        
        db.session.commit()
        flash('Cập nhật trạng thái thành công!', 'success')
        return redirect(url_for('chi_tiet_don_hang', id=id))
    
    @app.route('/khach-hang')
    @login_required
    def danh_sach_khach_hang():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        
        query = KhachHang.query
        
        if search:
            query = query.filter(
                KhachHang.ho_ten.contains(search) |
                KhachHang.so_dien_thoai.contains(search) |
                KhachHang.email.contains(search)
            )
        
        khach_hang = query.order_by(KhachHang.ngay_tao.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        
        return render_template('khach_hang/danh_sach.html', khach_hang=khach_hang, search=search)
    
    @app.route('/dich-vu')
    @login_required
    def danh_sach_dich_vu():
        dich_vu = DichVu.query.order_by(DichVu.ten_dich_vu).all()
        return render_template('dich_vu/danh_sach.html', dich_vu=dich_vu)
    
    @app.route('/dich-vu/tao-moi', methods=['GET', 'POST'])
    @login_required
    def tao_dich_vu():
        if request.method == 'POST':
            ten_dich_vu = request.form.get('ten_dich_vu')
            mo_ta = request.form.get('mo_ta')
            gia_ban = float(request.form.get('gia_ban', 0))
            thoi_gian_bao_hanh = int(request.form.get('thoi_gian_bao_hanh', 0))
            
            dich_vu = DichVu(
                ten_dich_vu=ten_dich_vu,
                mo_ta=mo_ta,
                gia_ban=gia_ban,
                thoi_gian_bao_hanh=thoi_gian_bao_hanh
            )
            
            db.session.add(dich_vu)
            db.session.commit()
            
            flash('Tạo dịch vụ thành công!', 'success')
            return redirect(url_for('danh_sach_dich_vu'))
        
        return render_template('dich_vu/tao_moi.html')
    
    @app.route('/linh-kien')
    @login_required
    def danh_sach_linh_kien():
        linh_kien = LinhKien.query.order_by(LinhKien.ten_linh_kien).all()
        return render_template('linh_kien/danh_sach.html', linh_kien=linh_kien)
    
    @app.route('/linh-kien/tao-moi', methods=['GET', 'POST'])
    @login_required
    def tao_linh_kien():
        if request.method == 'POST':
            ten_linh_kien = request.form.get('ten_linh_kien')
            ma_linh_kien = request.form.get('ma_linh_kien')
            so_luong_ton = int(request.form.get('so_luong_ton', 0))
            gia_nhap = float(request.form.get('gia_nhap', 0))
            gia_ban = float(request.form.get('gia_ban', 0))
            nha_cung_cap = request.form.get('nha_cung_cap')
            thong_so_ky_thuat = request.form.get('thong_so_ky_thuat')
            
            linh_kien = LinhKien(
                ten_linh_kien=ten_linh_kien,
                ma_linh_kien=ma_linh_kien,
                so_luong_ton=so_luong_ton,
                gia_nhap=gia_nhap,
                gia_ban=gia_ban,
                nha_cung_cap=nha_cung_cap,
                thong_so_ky_thuat=thong_so_ky_thuat
            )
            
            db.session.add(linh_kien)
            db.session.commit()
            
            flash('Tạo linh kiện thành công!', 'success')
            return redirect(url_for('danh_sach_linh_kien'))
        
        return render_template('linh_kien/tao_moi.html')
    
    @app.route('/bao-cao')
    @login_required
    def bao_cao():
        # Lấy tham số lọc
        thang = request.args.get('thang', datetime.now().month, type=int)
        nam = request.args.get('nam', datetime.now().year, type=int)
        
        # Thống kê doanh thu theo tháng
        doanh_thu = db.session.query(
            db.func.sum(DonHang.tong_tien)
        ).filter(
            db.extract('month', DonHang.ngay_tiep_nhan) == thang,
            db.extract('year', DonHang.ngay_tiep_nhan) == nam,
            DonHang.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN
        ).scalar() or 0
        
        # Thống kê số đơn hàng theo trạng thái
        thong_ke_trang_thai = db.session.query(
            DonHang.trang_thai,
            db.func.count(DonHang.id)
        ).filter(
            db.extract('month', DonHang.ngay_tiep_nhan) == thang,
            db.extract('year', DonHang.ngay_tiep_nhan) == nam
        ).group_by(DonHang.trang_thai).all()
        
        # Top dịch vụ mẫu (vì không có bảng ChiTietDonHang)
        top_dich_vu = [
            ('Cài đặt Windows', 5),
            ('Vệ sinh máy tính', 4),
            ('Thay keo tản nhiệt', 3),
            ('Nâng cấp RAM', 2),
            ('Thay SSD', 2)
        ]
        
        return render_template('bao_cao/index.html',
                             doanh_thu=doanh_thu,
                             thang=thang,
                             nam=nam,
                             thong_ke_trang_thai=thong_ke_trang_thai,
                             top_dich_vu=top_dich_vu)
    
    @app.route('/bao-cao/excel')
    @login_required
    def bao_cao_excel():
        # Lấy tham số lọc
        thang = request.args.get('thang', datetime.now().month, type=int)
        nam = request.args.get('nam', datetime.now().year, type=int)
        
        # Lấy dữ liệu thống kê
        doanh_thu = db.session.query(
            db.func.sum(DonHang.tong_tien)
        ).filter(
            db.extract('month', DonHang.ngay_tiep_nhan) == thang,
            db.extract('year', DonHang.ngay_tiep_nhan) == nam,
            DonHang.trang_thai_thanh_toan == TrangThaiThanhToan.DA_THANH_TOAN
        ).scalar() or 0
        
        thong_ke_trang_thai = db.session.query(
            DonHang.trang_thai,
            db.func.count(DonHang.id)
        ).filter(
            db.extract('month', DonHang.ngay_tiep_nhan) == thang,
            db.extract('year', DonHang.ngay_tiep_nhan) == nam
        ).group_by(DonHang.trang_thai).all()
        
        # Tạo CSV content
        csv_content = "Báo cáo CSKH PC\n"
        csv_content += f"Tháng: {thang}\n"
        csv_content += f"Năm: {nam}\n\n"
        csv_content += "Chỉ tiêu,Giá trị,Ghi chú\n"
        csv_content += f"Doanh thu,{doanh_thu},VNĐ\n"
        csv_content += f"Tổng đơn hàng,{len(thong_ke_trang_thai)},\n"
        
        for trang_thai, so_luong in thong_ke_trang_thai:
            csv_content += f"{trang_thai.value},{so_luong},\n"
        
        # Tạo response
        response = Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=bao_cao_thang_{thang}_{nam}.csv'}
        )
        return response
    
    # Routes cho khách hàng
    @app.route('/dang-nhap-khach-hang', methods=['GET', 'POST'])
    def dang_nhap_khach_hang():
        if current_user.is_authenticated:
            # Nếu đã đăng nhập, chuyển hướng đến dashboard phù hợp
            if current_user.__class__.__name__ == 'NhanVien':  # Admin/nhân viên
                return redirect(url_for('dashboard'))
            else:  # Khách hàng
                return redirect(url_for('dashboard_khach_hang'))
        
        if request.method == 'POST':
            email_or_sdt = request.form.get('email')
            mat_khau = request.form.get('mat_khau')
            
            # Tìm khách hàng theo email hoặc SĐT
            khach_hang = KhachHang.query.filter(
                (KhachHang.email == email_or_sdt) | 
                (KhachHang.so_dien_thoai == email_or_sdt)
            ).first()
            
            if khach_hang and khach_hang.check_password(mat_khau):
                if khach_hang.trang_thai == 'hoat_dong':
                    login_user(khach_hang)
                    flash('Đăng nhập thành công!', 'success')
                    return redirect(url_for('dashboard_khach_hang'))
                else:
                    flash('Tài khoản của bạn đã bị khóa!', 'danger')
            else:
                flash('Email/SĐT hoặc mật khẩu không đúng!', 'danger')
        
        return render_template('khach_hang/dang_nhap.html')
    
    @app.route('/dang-ky-khach-hang', methods=['GET', 'POST'])
    def dang_ky_khach_hang():
        if request.method == 'POST':
            # Lấy dữ liệu từ form
            ho_ten = request.form.get('ho_ten')
            so_dien_thoai = request.form.get('so_dien_thoai')
            email = request.form.get('email')
            mat_khau = request.form.get('mat_khau')
            confirm_mat_khau = request.form.get('confirm_mat_khau')
            
            # Validation
            if not all([ho_ten, so_dien_thoai, email, mat_khau, confirm_mat_khau]):
                flash('Vui lòng điền đầy đủ thông tin!', 'danger')
                return redirect(url_for('dang_ky_khach_hang'))
            
            if mat_khau != confirm_mat_khau:
                flash('Mật khẩu xác nhận không khớp!', 'danger')
                return redirect(url_for('dang_ky_khach_hang'))
            
            if len(mat_khau) < 6:
                flash('Mật khẩu phải có ít nhất 6 ký tự!', 'danger')
                return redirect(url_for('dang_ky_khach_hang'))
            
            # Kiểm tra trùng email hoặc SĐT
            if KhachHang.query.filter_by(email=email).first():
                flash('Email đã tồn tại!', 'danger')
                return redirect(url_for('dang_ky_khach_hang'))
            
            if KhachHang.query.filter_by(so_dien_thoai=so_dien_thoai).first():
                flash('Số điện thoại đã tồn tại!', 'danger')
                return redirect(url_for('dang_ky_khach_hang'))
            
            # Tạo mã khách hàng
            so_khach_hang = KhachHang.query.count() + 1
            ma_khach_hang = f"KH{so_khach_hang:03d}"
            
            # Tạo khách hàng mới
            khach_hang = KhachHang(
                ma_khach_hang=ma_khach_hang,
                ho_ten=ho_ten,
                so_dien_thoai=so_dien_thoai,
                email=email,
                ngay_sinh=datetime.strptime(request.form.get('ngay_sinh'), '%Y-%m-%d').date() if request.form.get('ngay_sinh') else None,
                gioi_tinh=request.form.get('gioi_tinh'),
                dia_chi=request.form.get('dia_chi'),
                cong_ty=request.form.get('cong_ty'),
                loai_khach_hang=request.form.get('loai_khach_hang', 'ca_nhan')
            )
            khach_hang.set_password(mat_khau)
            
            db.session.add(khach_hang)
            db.session.commit()
            
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('dang_nhap_khach_hang'))
        
        return render_template('khach_hang/dang_ky.html')
    
    @app.route('/dang-ky-nhanh', methods=['POST'])
    def dang_ky_nhanh():
        # Lấy dữ liệu từ form đăng ký nhanh
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        email = request.form.get('email')
        mat_khau = request.form.get('mat_khau')
        
        # Validation cơ bản
        if not all([ho_ten, so_dien_thoai, email, mat_khau]):
            flash('Vui lòng điền đầy đủ thông tin!', 'danger')
            return redirect(url_for('dang_nhap_khach_hang'))
        
        if len(mat_khau) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự!', 'danger')
            return redirect(url_for('dang_nhap_khach_hang'))
        
        # Kiểm tra trùng email hoặc SĐT
        if KhachHang.query.filter_by(email=email).first():
            flash('Email đã tồn tại! Vui lòng dùng email khác.', 'danger')
            return redirect(url_for('dang_nhap_khach_hang'))
        
        if KhachHang.query.filter_by(so_dien_thoai=so_dien_thoai).first():
            flash('Số điện thoại đã tồn tại! Vui lòng dùng SĐT khác.', 'danger')
            return redirect(url_for('dang_nhap_khach_hang'))
        
        # Tạo mã khách hàng
        so_khach_hang = KhachHang.query.count() + 1
        ma_khach_hang = f"KH{so_khach_hang:03d}"
        
        # Tạo khách hàng mới với thông tin cơ bản
        khach_hang = KhachHang(
            ma_khach_hang=ma_khach_hang,
            ho_ten=ho_ten,
            so_dien_thoai=so_dien_thoai,
            email=email,
            loai_khach_hang='ca_nhan'
        )
        khach_hang.set_password(mat_khau)
        
        db.session.add(khach_hang)
        db.session.commit()
        
        # Tự động đăng nhập sau khi đăng ký thành công
        login_user(khach_hang)
        flash('🎉 Đăng ký thành công! Chào mừng bạn đến với CSKH PC!', 'success')
        
        return redirect(url_for('dashboard_khach_hang'))
    
    @app.route('/dang-xuat-khach-hang')
    def dang_xuat_khach_hang():
        logout_user()
        flash('Đăng xuất thành công!', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dashboard-khach-hang')
    @login_required
    def dashboard_khach_hang():
        # Kiểm tra xem là khách hàng hay admin
        if current_user.__class__.__name__ == 'NhanVien':  # Là admin/nhân viên
            return redirect(url_for('dashboard'))
        
        # Lấy thống kê cho khách hàng
        so_don_hang = DonHang.query.filter_by(khach_hang_id=current_user.id).count()
        tong_chi_ti = db.session.query(db.func.sum(DonHang.tong_tien)).filter_by(
            khach_hang_id=current_user.id,
            trang_thai_thanh_toan=TrangThaiThanhToan.DA_THANH_TOAN
        ).scalar() or 0
        
        don_hang_gan_nhat = DonHang.query.filter_by(khach_hang_id=current_user.id).order_by(
            DonHang.ngay_tiep_nhan.desc()
        ).first()
        
        don_hang_moi = DonHang.query.filter_by(khach_hang_id=current_user.id).order_by(
            DonHang.ngay_tiep_nhan.desc()
        ).limit(5).all()
        
        return render_template('khach_hang/dashboard.html',
                             so_don_hang=so_don_hang,
                             tong_chi_ti=tong_chi_ti,
                             don_hang_gan_nhat=don_hang_gan_nhat,
                             don_hang_moi=don_hang_moi)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)