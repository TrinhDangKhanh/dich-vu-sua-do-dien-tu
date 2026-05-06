from app import create_app

app = create_app()

with app.app_context():
    # Test route exists
    with app.test_client() as client:
        response = client.get('/dang-nhap-khach-hang')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Route dang-nhap-khach-hang works!")
        else:
            print(f"Error: {response.status_code}")
