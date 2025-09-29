# geocoding.py
import requests

def get_map(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&addressdetails=1"

    headers = {
        "User-Agent": "YourAppName/1.0 (your-email@example.com)"  # 이메일을 User-Agent에 추가
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"[ERROR] 요청 실패 - 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
            return None, None, None

        try:
            data = response.json()
        except ValueError as ve:
            print("[ERROR] JSON 파싱 실패")
            print(f"응답 텍스트: {response.text}")
            return None, None, None

        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            full_address = data[0]["display_name"]
            return lat, lon, full_address
        else:
            print("주소 검색 결과 없음")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 요청 중 예외 발생: {e}")
        return None, None, None


def get_current_location_ip():
    """
    IP 주소를 기반으로 현재 위치의 위도, 경도, 주소(도시)를 가져옵니다.
    """
    try:
        # ipinfo.io와 같은 IP Geo API 사용
        # 응답 예: {"ip": "...", "city": "Seoul", "region": "Seoul", "country": "KR", "loc": "37.5665,126.9780", ...}
        response = requests.get('https://ipinfo.io/json', timeout=5)
        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
        data = response.json()

        # 'loc' 필드에서 위도, 경도 추출 (예: "37.5665,126.9780")
        if 'loc' in data:
            lat, lon = data['loc'].split(',')

            city = data.get('city', '알 수 없는 지역')  # 예: 강남구, 성남시
            region = data.get('region', '')  # 예: 서울, 경기도
            country = data.get('country', '')

            # 한국인 경우 주소 조합 로직 개선
            if country == 'KR':
                # 1. region과 city가 같은 경우 (예: 서울, 서울) -> city만 사용
                if region == city:
                    real_address = city  # 예: "Seoul"만 표시. (만약 '구' 정보가 다른 필드에 있다면 해당 필드를 찾아야 함)

                # 2. region과 city가 다르고, city에 이미 '구' 정보가 포함된 경우
                #   (예: region='Gyeonggi-do', city='Seongnam-si') -> '경기도 성남시' 형태로 조합
                elif region and city:
                    real_address = f"{region} {city}"

                # 3. 그 외 (둘 중 하나만 있는 경우 등)
                else:
                    real_address = f"{region} {city}".strip()

            # 기타 국가: 지역, 도시 형태로 표시
            else:
                # 셋(region, city, country) 모두 표시하여 최소한의 정보 제공
                address_parts = [p for p in [region, city, country] if p]
                real_address = ", ".join(address_parts)

            return lat, lon, real_address

        else:
            print("IP 위치 정보에서 'loc' 필드를 찾을 수 없습니다.")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] IP 위치 정보 로드 중 오류 발생: {e}")
        return None, None, None
    except Exception as e:
        print(f"[ERROR] IP 위치 정보 처리 중 알 수 없는 오류: {e}")
        return None, None, None
