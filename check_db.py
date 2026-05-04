from app import create_app
from database_improved import KhachHang

app = create_app()
with app.app_context():
    print('So khach hang:', KhachHang.query.count())
    kh = KhachHang.query.first()
    if kh:
        print('Khach hang dau tien:', kh.ma_khach_hang, kh.ho_ten)
    else:
        print('Khong co khach hang nao')
