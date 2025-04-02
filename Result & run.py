from Map import get_map
from Weather import get_weather

def main():
    address = input("주소를 입력하세요: ")  # 여기서 원하는 주소를 입력하세요
    lat, lon, address = get_map(address)  # 주소도 반환받기

    if lat and lon:
        print(f"주소: {address}")  # 주소 출력

        # 날씨 정보를 가져옵니다
        weather_info = get_weather(lat, lon)
        if "error" not in weather_info:
            print(f"온도: {weather_info['temperature']}°C")
            print(f"날씨: {weather_info['weather']}")
        else:
            print("날씨 정보를 가져올 수 없습니다.")
    else:
        print("위도와 경도를 찾을 수 없습니다.")


if __name__ == "__main__":
    main()