from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

from database import db, KhachHang, DichVu, LinhKien, DonHang, ChiTietDonHang, ChiTietLinhKien, NhanVien, TrangThaiDonHang, TrangThaiThanhToan, LoaiThietBi
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
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này!'
    
    @login_manager.user_loader
    def load_user(user_id):
        return NhanVien.query.get(int(user_id))
    
    # Tạo database và admin mặc định
    with app.app_context():
        db.create_all()
        
        # Tạo admin mặc định nếu chưa có
        admin = NhanVien.query.filter_by(tai_khoan='admin').first()
        if not admin:
            admin = NhanVien(
                ho_ten='Quản trị viên',
                tai_khoan='admin',
                mat_khau=generate_password_hash('admin123'),
                email='admin@pccare.com',
                vai_tro='admin'
            )
            db.session.add(admin)
            
            # Thêm một số dịch vụ mẫu
            dich_vus = [
                DichVu(ten_dich_vu='Cài đặt Windows', gia_ban=200000, thoi_gian_bao_hanh=1, mo_ta='Cài đặt Windows 10/11, driver và phần mềm cơ bản'),
                DichVu(ten_dich_vu='Vệ sinh máy tính', gia_ban=150000, thoi_gian_bao_hanh=0, mo_ta='Vệ sinh tổng quát, tản nhiệt, keo tản nhiệt'),
                DichVu(ten_dich_vu='Thay keo tản nhiệt', gia_ban=250000, thoi_gian_bao_hanh=3, mo_ta='Thay keo tản nhiệt cho CPU/GPU'),
                DichVu(ten_dich_vu='Nâng cấp RAM', gia_ban=100000, thoi_gian_bao_hanh=36, mo_ta='Nâng cấp RAM laptop, PC'),
                DichVu(ten_dich_vu='Thay SSD', gia_ban=100000, thoi_gian_bao_hanh=36, mo_ta='Thay SSD, cài đặt hệ điều hành'),
                DichVu(ten_dich_vu='Thay màn hình Laptop', gia_ban=1500000, thoi_gian_bao_hanh=6, mo_ta='Thay màn hình LCD, LED cho laptop'),
                DichVu(ten_dich_vu='Sửa chữa Mainboard', gia_ban=500000, thoi_gian_bao_hanh=3, mo_ta='Sửa chữa các lỗi mainboard, chipset'),
                DichVu(ten_dich_vu='Cứu dữ liệu', gia_ban=800000, thoi_gian_bao_hanh=0, mo_ta='Cứu dữ liệu từ ổ cứng hỏng, format'),
            ]
            
            for dv in dich_vus:
                if not DichVu.query.filter_by(ten_dich_vu=dv.ten_dich_vu).first():
                    db.session.add(dv)
            
            # Thêm khách hàng mẫu
            khach_hangs = [
                KhachHang(ho_ten='Nguyễn Văn An', so_dien_thoai='0912345678', email='an.nguyen@email.com', dia_chi='Hà Nội'),
                KhachHang(ho_ten='Trần Thị Bình', so_dien_thoai='0987654321', email='binh.tran@email.com', dia_chi='TP. Hồ Chí Minh'),
                KhachHang(ho_ten='Lê Văn Cường', so_dien_thoai='0934567890', email='cuong.le@email.com', dia_chi='Đà Nẵng'),
                KhachHang(ho_ten='Phạm Thị Dung', so_dien_thoai='0967890123', email='dung.pham@email.com', dia_chi='Hải Phòng'),
                KhachHang(ho_ten='Hoàng Văn Em', so_dien_thoai='0978901234', email='em.hoang@email.com', dia_chi='Cần Thơ'),
                KhachHang(ho_ten='Đặng Thị Fan', so_dien_thoai='0901234567', email='fan.dang@email.com', dia_chi='Hà Nội'),
                KhachHang(ho_ten='Ngô Văn Giàu', so_dien_thoai='0923456789', email='giau.ngo@email.com', dia_chi='TP. Hồ Chí Minh'),
                KhachHang(ho_ten='Bùi Thị Hương', so_dien_thoai='0945678901', email='huong.bui@email.com', dia_chi='Huế'),
            ]
            
            for kh in khach_hangs:
                if not KhachHang.query.filter_by(so_dien_thoai=kh.so_dien_thoai).first():
                    db.session.add(kh)
            
            # Thêm linh kiện mẫu
            linh_kiens = [
                LinhKien(ten_linh_kien='RAM DDR4 8GB', ma_linh_kien='RAM8G01', so_luong_ton=50, gia_nhap=800000, gia_ban=1200000, nha_cung_cap='Kingston'),
                LinhKien(ten_linh_kien='RAM DDR4 16GB', ma_linh_kien='RAM16G01', so_luong_ton=30, gia_nhap=1500000, gia_ban=2200000, nha_cung_cap='Corsair'),
                LinhKien(ten_linh_kien='SSD 240GB SATA', ma_linh_kien='SSD24001', so_luong_ton=25, gia_nhap=600000, gia_ban=950000, nha_cung_cap='Samsung'),
                LinhKien(ten_linh_kien='SSD 480GB SATA', ma_linh_kien='SSD48001', so_luong_ton=20, gia_nhap=1000000, gia_ban=1650000, nha_cung_cap='Crucial'),
                LinhKien(ten_linh_kien='SSD NVMe 500GB', ma_linh_kien='SSD50001', so_luong_ton=15, gia_nhap=1500000, gia_ban=2400000, nha_cung_cap='Western Digital'),
                LinhKien(ten_linh_kien='Màn hình Laptop 14"', ma_linh_kien='LCD14001', so_luong_ton=10, gia_nhap=2000000, gia_ban=3200000, nha_cung_cap='LG'),
                LinhKien(ten_linh_kien='Màn hình Laptop 15.6"', ma_linh_kien='LCD15601', so_luong_ton=8, gia_nhap=2500000, gia_ban=3800000, nha_cung_cap='AU Optronics'),
                LinhKien(ten_linh_kien='Keo tản nhiệt', ma_linh_kien='GEL001', so_luong_ton=100, gia_nhap=50000, gia_ban=100000, nha_cung_cap='Arctic Silver'),
                LinhKien(ten_linh_kien='Pin Laptop 6 Cell', ma_linh_kien='BAT6C01', so_luong_ton=20, gia_nhap=300000, gia_ban=550000, nha_cung_cap='Battery Pro'),
                LinhKien(ten_linh_kien='Sạc Laptop 65W', ma_linh_kien='ADP65W01', so_luong_ton=30, gia_nhap=150000, gia_ban=280000, nha_cung_cap='Anker'),
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
                    ten_thiet_bi='Dell XPS 15',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='Dell',
                    model='XPS 9570',
                    serial_number='DLXPS957001',
                    mo_ta_loi='Máy chạy chậm, nóng, cần vệ sinh và nâng cấp',
                    trang_thai=TrangThaiDonHang.DANG_XU_LY,
                    tong_tien=1350000
                ),
                DonHang(
                    ma_don_hang='DH20240501002',
                    khach_hang_id=2,
                    ten_thiet_bi='Macbook Pro 13"',
                    loai_thiet_bi=LoaiThietBi.MACBOOK,
                    nhan_hieu='Apple',
                    model='Macbook Pro 2020',
                    serial_number='MBP2020001',
                    mo_ta_loi='Màn hình bị sọc, cần thay màn hình mới',
                    trang_thai=TrangThaiDonHang.CHO_LINH_KIEN,
                    tong_tien=3200000
                ),
                DonHang(
                    ma_don_hang='DH20240501003',
                    khach_hang_id=3,
                    ten_thiet_bi='PC Gaming',
                    loai_thiet_bi=LoaiThietBi.PC_DESKTOP,
                    nhan_hieu='Custom',
                    model='Gaming PC',
                    serial_number='PCG001',
                    mo_ta_loi='Máy không lên nguồn, cần kiểm tra main',
                    trang_thai=TrangThaiDonHang.HOAN_THANH,
                    tong_tien=500000,
                    ngay_hoan_thanh=datetime.utcnow()
                ),
                DonHang(
                    ma_don_hang='DH20240501004',
                    khach_hang_id=4,
                    ten_thiet_bi='HP Envy 13',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='HP',
                    model='Envy 13-ad001',
                    serial_number='HPENV13001',
                    mo_ta_loi='Cần cài đặt lại Windows và phần mềm văn phòng',
                    trang_thai=TrangThaiDonHang.DANG_XU_LY,
                    tong_tien=200000
                ),
                DonHang(
                    ma_don_hang='DH20240501005',
                    khach_hang_id=5,
                    ten_thiet_bi='Asus ROG Strix',
                    loai_thiet_bi=LoaiThietBi.LAPTOP,
                    nhan_hieu='Asus',
                    model='ROG Strix G15',
                    serial_number='ASUSROG001',
                    mo_ta_loi='Nâng cấp RAM từ 8GB lên 16GB',
                    trang_thai=TrangThaiDonHang.HOAN_THANH,
                    tong_tien=1100000,
                    ngay_hoan_thanh=datetime.utcnow()
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
            return redirect(url_for('dashboard'))
        return redirect(url_for('dang_nhap'))
    
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
    @login_required
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
                khach_hang = KhachHang(
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
            
            # Tạo đơn hàng
            don_hang = DonHang(
                ma_don_hang=ma_don_hang,
                khach_hang_id=khach_hang.id,
                ten_thiet_bi=ten_thiet_bi,
                loai_thiet_bi=LoaiThietBi(loai_thiet_bi),
                nhan_hieu=nhan_hieu,
                model=model,
                serial_number=serial_number,
                mat_khau=mat_khau,
                mo_ta_loi=mo_ta_loi,
                trang_thai=TrangThaiDonHang.CHO_TIEP_NHAN
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
        csv_content = "Báo cáo PC Care\n"
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
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)