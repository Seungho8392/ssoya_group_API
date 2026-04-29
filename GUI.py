import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import os
import config  # 👈 위에서 만든 설정 파일을 가져옵니다.

# 👈 여기서 바로 필요한 기능들을 임포트합니다!
from Finish_Map import get_map
from Finish_Weather import get_weather


class WeatherAppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 설정 파일의 값들을 적용
        self.title(config.APP_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.configure(fg_color=config.BG_COLOR)

        self._create_widgets()

    def _create_widgets(self):
        # ... (중략: 기존과 동일한 위젯 생성 코드) ...
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20)
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="분당구 삼평동", text_color="#000000", fg_color="#FFFFFF")
        self.entry.pack(side="left", padx=5)
        self.search_btn = ctk.CTkButton(self.input_frame, text="🔍 검색", command=self.실행_조회)
        self.search_btn.pack(side="left")
        self.label_info = ctk.CTkLabel(self,
            text="원하는 지역을 입력해 주세요.\n(예: 성남시, 분당구, 삼평동)",
            text_color="#333333",
            font=config.get_cut_font(13)  # 글씨를 조금 더 키우면 허전함이 줄어듭니다.
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
                icon_name = config.WEATHER_ICONS.get(weather, "default.png")
                icon_path = os.path.join(config.IMAGE_FOLDER, icon_name)

                if os.path.exists(icon_path):
                    # config에서 이미지 처리를 도와주는 함수를 따로 안 만드셨다면
                    # 여기서 바로 PIL Image를 써도 무방합니다.
                    img = Image.open(icon_path)
                    ctk_img = CTkImage(light_image=img, size=(300, 300))
                    self.icon_label.configure(image=ctk_img, text="")
                    self.icon_label.image = ctk_img

                self.label_result.configure(text=f"📍 {real_address}\n\n 🌡️ 온도 : {temp}°C\n\n🌤️ 날씨 : {weather}")
        except Exception as e:
            self.label_result.configure(text=f"⚠️ 오류: {str(e)}")