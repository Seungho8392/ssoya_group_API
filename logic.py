import os
from PIL import Image
from customtkinter import CTkImage
from datetime import datetime
# 필요한 모듈들 가져오기
from Finish_Map import get_map
from Finish_Weather import get_weather
from config import Config  # 👈 Config 클래스만 가져오면 끝!


class WeatherController:
    def __init__(self, app_instance):
        self.app = app_instance

    def get_initial_settings(self):
        # 초기에 필요한 설정값들을 딕셔너리로 묶어서 던져줌
        return {
            "title": Config.APP_TITLE,
            "geometry": Config.WINDOW_SIZE,
            "bg_color": Config.BG_COLOR,
            "info_text": "원하는 지역을 입력해 주세요.\n(예: 성남시, 분당구, 삼평동)",
            "info_color": Config.INFO_TEXT_COLOR,
            "info_font": Config.get_cut_font(16),
            "text_color": Config.TEXT_COLOR,
            "result_font": Config.get_cut_font(14)
        }

    def 실행_조회(self, address):
        """데이터 처리만 담당하고 결과 데이터 세트를 반환"""
        if not address: return None

        try:
            # 1. 위치 및 날씨 데이터 가져오기
            lat, lon, real_address = get_map(address)
            if not (lat and lon): return None

            weather_info = get_weather(lat, lon)
            temp = weather_info["temperature"]
            weather = weather_info["weather"]

            # 2. 현재 시간 정보 생성
            now = datetime.now().strftime("%p %I:%M")

            # 3. 이미지(아이콘) 처리 로직
            icon_name = Config.WEATHER_ICONS.get(weather, Config.WEATHER_ICONS["기본"])
            icon_path = os.path.join(Config.IMAGE_FOLDER, icon_name)

            ctk_img = None
            if os.path.exists(icon_path):
                img = Image.open(icon_path).resize((200, 200))
                ctk_img = CTkImage(light_image=img, size=(300, 300))
            # 4. 최종 텍스트 조립 (여기에 모든 정보를 모읍니다)
            display_text = (
                f"🕒 조회 시간 : {now}\n\n"
                f"📍 {real_address}\n\n"
                f"🌡️ 온도 : {temp}°C\n\n"
                f"🌤️ 날씨 : {weather}"
            )
            # 5. 마지막에 딱 한 번만 반환!
            return {"text": display_text, "image": ctk_img}
        except Exception as e:
            # 에러 발생 시 에러 메시지 반환
            return {"error": str(e)}