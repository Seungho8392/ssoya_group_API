# main.py
from GUI import WeatherAppUI
from Finish_Map import get_map
from Finish_Weather import get_weather

# 1. 프로그램에서 사용할 고정 데이터(아이콘 매핑)만 정의
WEATHER_ICONS = {
    "맑음": "sunny.png",
    "구름 조금": "little_cloud.png",
    "흐림": "blur.png",
    "비": "rain.png",
    "눈": "snow.png"
}

if __name__ == "__main__":
    # 2. UI라는 거대한 기계를 조립 (외부 함수와 데이터를 부품처럼 끼워넣음)
    app = WeatherAppUI(
        get_map_func=get_map,
        get_weather_func=get_weather,
        weather_icons=WEATHER_ICONS
    )
    app.mainloop()