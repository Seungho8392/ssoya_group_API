import customtkinter as ctk
from PIL import Image
import os
from customtkinter import CTkImage

# 1. 외부 모듈 및 설정값 가져오기
from Finish_Map import get_map
from Finish_Weather import get_weather
# config.py에서 미리 만든 것들을 몽땅 가져옵니다.
from config import APP_TITLE, WINDOW_SIZE, BG_COLOR, TEXT_COLOR, \
    INFO_TEXT_COLOR, WEATHER_ICONS, IMAGE_FOLDER, get_cut_font


class WeatherAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 2. config.py에 있는 값으로 앱 설정
        ctk.set_appearance_mode("light")
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.configure(fg_color=BG_COLOR)

        # 3. 경로와 아이콘 설정도 config에서 가져온 값 사용
        self.image_folder = IMAGE_FOLDER
        self.weather_icons = WEATHER_ICONS

        self._create_widgets()

    def _create_widgets(self):
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="분당구 삼평동", text_color=TEXT_COLOR)
        self.entry.pack(side="left", padx=5)

        self.search_btn = ctk.CTkButton(self.input_frame, text="🔍 검색", command=self.실행_조회)
        self.search_btn.pack(side="left")

        self.label_info = ctk.CTkLabel(
            self,
            text="원하는 지역을 입력해 주세요.\n(예: 성남시, 분당구, 삼평동)",
            text_color=INFO_TEXT_COLOR,
            font=get_cut_font(16)  # config에서 가져온 함수 사용
        )
        self.label_info.pack(pady=(150, 0))

        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=10)

        self.label_result = ctk.CTkLabel(self, text="", text_color=TEXT_COLOR, font=get_cut_font(14))
        self.label_result.pack(pady=10)

    def 실행_조회(self):
        address = self.entry.get()
        if not address: return

        self.label_info.pack_forget()

        try:
            lat, lon, real_address = get_map(address)

            if lat and lon:
                weather_info = get_weather(lat, lon)
                temp = weather_info["temperature"]
                weather = weather_info["weather"]

                # config의 WEATHER_ICONS를 사용하여 아이콘 찾기
                icon_name = self.weather_icons.get(weather, self.weather_icons["기본"])
                icon_path = os.path.join(self.image_folder, icon_name)

                if os.path.exists(icon_path):
                    img = Image.open(icon_path).resize((200, 200))
                    ctk_img = CTkImage(light_image=img, size=(300, 300))
                    self.icon_label.configure(image=ctk_img, text="")
                    self.icon_label.image = ctk_img

                self.label_result.configure(
                    text=f"📍 {real_address}\n\n 🌡️ 온도 : {temp}°C\n\n🌤️ 날씨 : {weather}"
                )
        except Exception as e:
            self.label_result.configure(text=f"⚠️ 오류: {str(e)}")