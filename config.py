# config.py
import os
import sys
import customtkinter as ctk


class Config:
    # 1. 경로 관련 설정
    @staticmethod  # 👈 '정적 메서드'라고 명시해줍니다.
    def get_app_path():
        return sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

    # 클래스 변수에서 위 함수를 호출할 때 사용
    APP_PATH = get_app_path.__func__() if hasattr(get_app_path, "__func__") else get_app_path()
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

    # 3. 디자인 관련 설정
    APP_TITLE = "🌤 날씨 API 정보"
    WINDOW_SIZE = "500x600"
    BG_COLOR = "#FFFFFF"
    TEXT_COLOR = "#000000"
    INFO_TEXT_COLOR = "#333333"

    # 4. 폰트 설정 로직
    @staticmethod  # 👈 외부에서 Config.get_cut_font(16)으로 바로 쓸 수 있게 함
    def get_cut_font(size=14):
        font_candidates = ["Noto Sans CJK KR", "Nanum Gothic", "Malgun Gothic", "AppleGothic"]
        for f in font_candidates:
            try:
                # 주의: ctk.CTkFont를 생성하려면 ctk.set_appearance_mode 등이 먼저 실행되어야 안전할 수 있습니다.
                return ctk.CTkFont(family=f, size=size)
            except:
                continue
        return ctk.CTkFont(size=size)