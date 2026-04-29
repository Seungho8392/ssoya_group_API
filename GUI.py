import customtkinter as ctk
from PIL import Image
import os
import sys
from customtkinter import CTkImage


# 경로 처리 함수
def get_app_path():
    return sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)


# 폰트 설정 함수
def get_cut_font(size=14):
    font_candidates = ["Noto Sans CJK KR", "Nanum Gothic", "Malgun Gothic", "AppleGothic"]
    for f in font_candidates:
        try:
            return ctk.CTkFont(family=f, size=size)
        except:
            continue
    return ctk.CTkFont(size=size)


class WeatherAppUI(ctk.CTk):
    def __init__(self, get_map_func, get_weather_func, weather_icons):
        super().__init__()

        # 데이터 처리 함수들을 저장
        self.get_map = get_map_func
        self.get_weather = get_weather_func
        self.weather_icons = weather_icons

        # 기본 설정
        ctk.set_appearance_mode("light")
        self.title("🌤 날씨 API 정보")
        self.geometry("500x500")
        self.configure(fg_color="#FFFFFF")

        self.app_path = get_app_path()
        self.image_folder = os.path.join(self.app_path, "images")

        self._create_widgets()

    def _create_widgets(self):
        # 주소 입력 프레임
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="분당구 삼평동",
                                  text_color="#000000", font=get_cut_font(14))
        self.entry.pack(side="left", padx=5)

        # 조회 버튼 (클래스 내부의 실행_조회 메서드 연결)
        self.search_btn = ctk.CTkButton(self.input_frame, text="🔍 검색", width=30,
                                        command=self.실행_조회)
        self.search_btn.pack(side="left")

        # 초기 안내 문구
        self.label_info = ctk.CTkLabel(self, text="원하는 지역을 입력해 주세요.\n(예: 성남시, 분당구, 삼평동)",
                                       text_color="#333333", font=get_cut_font(14))
        self.label_info.pack(pady=100)

        # 날씨 아이콘 라벨
        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=10)

        # 결과 텍스트 라벨
        self.label_result = ctk.CTkLabel(self, text="", text_color="#000000",
                                         font=get_cut_font(14))
        self.label_result.pack(pady=10)

    def 실행_조회(self):
        """메인에 있던 로직이 이 안으로 들어왔습니다."""
        address = self.entry.get()
        if not address:
            self.label_result.configure(text="⚠️ 주소를 입력해주세요.")
            return

        self.label_info.pack_forget()

        try:
            # 전달받은 외부 함수 사용
            lat, lon, real_address = self.get_map(address)

            if lat and lon:
                weather_info = self.get_weather(lat, lon)
                if "error" not in weather_info:
                    temp = weather_info["temperature"]
                    weather = weather_info["weather"]

                    # 아이콘 설정
                    icon_name = self.weather_icons.get(weather, "default.png")
                    icon_path = os.path.join(self.image_folder, icon_name)

                    if os.path.exists(icon_path):
                        img = Image.open(icon_path).resize((200, 200))
                        ctk_img = CTkImage(light_image=img, size=(300, 300))
                        self.icon_label.configure(image=ctk_img, text="")
                        self.icon_label.image = ctk_img
                    else:
                        self.icon_label.configure(image=None, text=weather)

                    # 결과 출력
                    self.label_result.configure(
                        text=f"📍 {real_address}\n\n 🌡️ 온도 : {temp}°C\n\n🌤️ 날씨 : {weather}"
                    )
                else:
                    self.label_result.configure(text="🚫 날씨 정보를 불러올 수 없습니다.")
            else:
                self.label_result.configure(text="❌ 주소를 찾을 수 없습니다.")
        except Exception as e:
            self.label_result.configure(text=f"⚠️ 오류 발생: {str(e)}")