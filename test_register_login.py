from app import create_app

app = create_app()

with app.app_context():
    # Test đăng ký nhanh trên trang đăng nhập
    with app.test_client() as client:
        print("=== TEST DANG KY NHANH TREN TRANG DANG NHAP ===")
        
        # 1. Test trang đăng nhập khách hàng
        print("\n1. Test trang dang nhap khach hang:")
        response = client.get('/dang-nhap-khach-hang')
        print(f"   Status: {response.status_code}")
        
        # 2. Test đăng ký nhanh thành công
        print("\n2. Test dang ky nhanh thanh cong:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick Test User',
            'so_dien_thoai': '0991234567',
            'email': 'quicktest@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 3. Test đăng ký nhanh với email trùng
        print("\n3. Test dang ky nhanh email trung:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick Test User 2',
            'so_dien_thoai': '0999876543',
            'email': 'quicktest@example.com',  # Email trùng
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 4. Test đăng ký nhanh với SĐT trùng
        print("\n4. Test dang ky nhanh SDT trung:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick Test User 3',
            'so_dien_thoai': '0991234567',  # SĐT trùng
            'email': 'quicktest3@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 5. Test đăng ký nhanh thiếu thông tin
        print("\n5. Test dang ky nhanh thieu thong tin:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick Test User 4',
            'so_dien_thoai': '',  # Thiếu SĐT
            'email': 'quicktest4@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # 6. Test đăng ký nhanh mật khẩu ngắn
        print("\n6. Test dang ky nhanh mat khau ngan:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick Test User 5',
            'so_dien_thoai': '0995556667',
            'email': 'quicktest5@example.com',
            'mat_khau': '123'  # Mật khẩu ngắn
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        print("\n=== TEST HOAN TAT ===")
