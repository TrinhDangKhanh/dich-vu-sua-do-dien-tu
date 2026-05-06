from app import create_app

app = create_app()

with app.app_context():
    # Test toàn bộ hệ thống đăng nhập
    with app.test_client() as client:
        print("=== TEST HE THONG DANG NHAP ===")
        
        # 1. Test trang chủ
        print("\n1. Test trang chu:")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        
        # 2. Test đăng nhập khách hàng
        print("\n2. Test trang dang nhap khach hang:")
        response = client.get('/dang-nhap-khach-hang')
        print(f"   Status: {response.status_code}")
        
        # 3. Test đăng ký khách hàng
        print("\n3. Test trang dang ky khach hang:")
        response = client.get('/dang-ky-khach-hang')
        print(f"   Status: {response.status_code}")
        
        # 4. Test đăng nhập admin
        print("\n4. Test trang dang nhap admin:")
        response = client.get('/dang-nhap')
        print(f"   Status: {response.status_code}")
        
        # 5. Test đăng ký khách hàng mới
        print("\n5. Test dang ky khach hang moi:")
        response = client.post('/dang-ky-khach-hang', data={
            'ho_ten': 'Test User',
            'so_dien_thoai': '0999999999',
            'email': 'test@example.com',
            'mat_khau': '123456',
            'confirm_mat_khau': '123456',
            'loai_khach_hang': 'ca_nhan'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 6. Test đăng nhập khách hàng mới
        print("\n6. Test dang nhap khach hang moi:")
        response = client.post('/dang-nhap-khach-hang', data={
            'email': 'test@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 7. Test dashboard khách hàng
        print("\n7. Test dashboard khach hang:")
        response = client.get('/dashboard-khach-hang')
        print(f"   Status: {response.status_code}")
        
        # 8. Test đăng xuất
        print("\n8. Test dang xuat:")
        response = client.get('/dang-xuat-khach-hang', follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        print("\n=== TEST HOAN TAT ===")
