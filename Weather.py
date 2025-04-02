# weather_api.py
import requests

# WeatherAPI 키
API_KEY = "5977b9b52a0a429889f235438253103"  # 발급받은 API 키 입력

# 날씨 상태에 대한 한글 번역 딕셔너리
weather_translation = {
    "sunny": "맑음",
    "clear": "맑음",
    "partly cloudy": "가끔 구름 많음",
    "cloudy": "구름 많음",
    "overcast": "흐림",
    "mist": "안개",
    "fog": "안개",
    "haze": "연무",
    "dust": "먼지",
    "sand": "모래 바람",
    "smoke": "연기",
    "tornado": "토네이도",
    "hurricane": "허리케인",
    "storm": "폭풍",
    "thunderstorm": "천둥번개",
    "drizzle": "이슬비",
    "light rain": "약한 비",
    "rain": "비",
    "moderate rain": "보통 비",
    "heavy rain": "강한 비",
    "showers": "소나기",
    "freezing rain": "얼음 비",
    "sleet": "진눈깨비",
    "light snow": "약한 눈",
    "snow": "눈",
    "moderate snow": "보통 눈",
    "heavy snow": "강한 눈",
    "blizzard": "눈보라"
}

# 날씨 정보를 가져오는 함수
def get_weather(lat, lon):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}&aqi=no"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        # 데이터에서 온도와 날씨 상태 추출
        temp = data["current"]["temp_c"]  # 섭씨 온도
        weather_code = data["current"]["condition"]["text"].lower()  # 날씨 상태 (소문자로 변환)

        # 날씨 상태를 한글로 변환
        weather_korean = weather_translation.get(weather_code, weather_code)  # 매핑된 값 없으면 그대로 출력
        return {"temperature": temp, "weather": weather_korean}
    else:
        return {"error": "API 요청 실패", "details": data}
