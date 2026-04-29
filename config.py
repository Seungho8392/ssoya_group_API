# config.py
import os
import sys
import customtkinter as ctk

# 1. 경로 관련 설정
def get_app_path():
    return sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

APP_PATH = get_app_path()
IMAGE_FOLDER = os.path.join(APP_PATH, "images")

# 2. 날씨 아이콘 매핑 데이터
WEATHER_ICONS = {
    "맑음": "sunny.png",
    "구름 조금": "little_cloud.png",
    "흐림": "blur.png",
    "비": "rain.png",
    "눈": "snow.png",
    "기본": "default.png"
}

# 3. 디자인 관련 설정 (매직 넘버 제거)
APP_TITLE = "🌤 날씨 API 정보"
WINDOW_SIZE = "500x500"
BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"
INFO_TEXT_COLOR = "#333333"

# 4. 폰트 설정 로직
def get_cut_font(size=14):
    font_candidates = ["Noto Sans CJK KR", "Nanum Gothic", "Malgun Gothic", "AppleGothic"]
    for f in font_candidates:
        try:
            return ctk.CTkFont(family=f, size=size)
        except:
            continue
    return ctk.CTkFont(size=size)