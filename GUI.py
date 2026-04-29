import customtkinter as ctk
from PIL import Image
import os
import sys
from customtkinter import CTkImage

# 👈 여기서 바로 필요한 기능들을 임포트합니다!
from Finish_Map import get_map
from Finish_Weather import get_weather


# 이미지/폰트 관련 함수들 (기존과 동일)
def get_app_path():
    return sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)


def get_cut_font(size=14):
    font_candidates = ["Noto Sans CJK KR", "Nanum Gothic", "Malgun Gothic"]
    for f in font_candidates:
        try:
            return ctk.CTkFont(family=f, size=size)
        except:
            continue
    return ctk.CTkFont(size=size)


class WeatherAppUI(ctk.CTk):
    def __init__(self):  # 👈 이제 밖에서 도구를 받아올 필요가 없어서 비워둡니다.
        super().__init__()

        # 날씨 아이콘 설정도 그냥 여기서 바로 해버립니다.
        self.weather_icons = {
            "맑음": "sunny.png", "구름 조금": "little_cloud.png",
            "흐림": "blur.png", "비": "rain.png", "눈": "snow.png"
        }

        ctk.set_appearance_mode("light")
        self.title("🌤 날씨 API 정보")
        self.geometry("500x500")
        self.configure(fg_color="#FFFFFF")

        self.app_path = get_app_path()
        self.image_folder = os.path.join(self.app_path, "images")

        self._create_widgets()

    def _create_widgets(self):
        # ... (중략: 기존과 동일한 위젯 생성 코드) ...
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20)
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="분당구 삼평동", text_color="#000000")
        self.entry.pack(side="left", padx=5)
        self.search_btn = ctk.CTkButton(self.input_frame, text="🔍 검색", command=self.실행_조회)
        self.search_btn.pack(side="left")
        self.label_info = ctk.CTkLabel(self,
            text="원하는 지역을 입력해 주세요.\n(예: 성남시, 분당구, 삼평동)",
            text_color="#333333",
            font=get_cut_font(13)  # 글씨를 조금 더 키우면 허전함이 줄어듭니다.
        )
        self.label_info.pack(pady=(150, 0))
        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=10)
        self.label_result = ctk.CTkLabel(self, text="", text_color="#000000")
        self.label_result.pack(pady=10)

    def 실행_조회(self):
        address = self.entry.get()
        if not address: return

        self.label_info.pack_forget()

        try:
            # 👈 위에서 import 했으니 그냥 바로 사용하면 됩니다!
            lat, lon, real_address = get_map(address)

            if lat and lon:
                weather_info = get_weather(lat, lon)
                # ... (이하 날씨 정보 표시 로직은 동일) ...
                temp = weather_info["temperature"]
                weather = weather_info["weather"]

                # 아이콘 처리
                icon_name = self.weather_icons.get(weather, "default.png")
                icon_path = os.path.join(self.image_folder, icon_name)

                if os.path.exists(icon_path):
                    img = Image.open(icon_path).resize((200, 200))
                    ctk_img = CTkImage(light_image=img, size=(300, 300))
                    self.icon_label.configure(image=ctk_img, text="")
                    self.icon_label.image = ctk_img

                self.label_result.configure(text=f"📍 {real_address}\n\n 🌡️ 온도 : {temp}°C\n\n🌤️ 날씨 : {weather}")
        except Exception as e:
            self.label_result.configure(text=f"⚠️ 오류: {str(e)}")