from app import create_app

app = create_app()

with app.app_context():
    # Test đăng ký nhanh
    with app.test_client() as client:
        print("=== TEST DANG KY NHANH ===")
        
        # Test trang chủ
        print("\n1. Test trang chu (co form dang ky nhanh):")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        
        # Test đăng ký nhanh thành công
        print("\n2. Test dang ky nhanh thanh cong:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick User',
            'so_dien_thoai': '0988776655',
            'email': 'quick@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # Test đăng ký nhanh với email trùng
        print("\n3. Test dang ky nhanh email trung:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick User 2',
            'so_dien_thoai': '0998877665',
            'email': 'quick@example.com',  # Email trùng
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # Test đăng ký nhanh với SĐT trùng
        print("\n4. Test dang ky nhanh SDT trung:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick User 3',
            'so_dien_thoai': '0988776655',  # SĐT trùng
            'email': 'quick3@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        # Test đăng ký nhanh thiếu thông tin
        print("\n5. Test dang ky nhanh thieu thong tin:")
        response = client.post('/dang-ky-nhanh', data={
            'ho_ten': 'Quick User 4',
            'so_dien_thoai': '',  # Thiếu SĐT
            'email': 'quick4@example.com',
            'mat_khau': '123456'
        }, follow_redirects=True)
        print(f"   Status: {response.status_code}")
        
        print("\n=== TEST HOAN TAT ===")
