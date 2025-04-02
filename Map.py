# geocoding.py
import requests


def get_map(address):
    # Nominatim API의 URL
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&addressdetails=1"

    headers = {
        "User-Agent": "YourAppName/1.0 (your-email@example.com)"  # 이메일을 User-Agent에 추가
    }

    # API 요청 보내기
    response = requests.get(url, headers=headers)

    # JSON 데이터 파싱
    data = response.json()

    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        full_address = data[0]["display_name"]  # 주소를 함께 반환
        return lat, lon, full_address
    else:
        return None, None, None
