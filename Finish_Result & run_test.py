# main_gui.py
import customtkinter as ctk
from PIL import Image, ImageTk
# geocoding 파일에서 get_map과 get_current_location_ip 함수를 모두 가져옵니다.
from Finish_Map_test import get_map, get_current_location_ip
from Finish_Weather import get_weather
from customtkinter import CTkImage
import os
import sys

# 이미지 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 패키징된 경우
    app_path = sys._MEIPASS  # 실행 파일의 임시 폴더 경로
else:
    # 개발 중인 경우
    app_path = os.path.dirname(__file__)


# 다국어 폰트 설정
def get_cut_font(size=14):
    font_candidates = ["Noto Sans CJK KR", "Nanum Gothic", "Malgun Gothic", "AppleGothic", "Nanum Brush Script"]
    for f in font_candidates:
        try:
            return ctk.CTkFont(family=f, size=size)
        except:
            continue
    return ctk.CTkFont(size=size)


weather_icons = {
    "맑음": "sunny.png",
    "흐림": "blur.png",
    "구름 조금": "little_cloud.png",
    "구름 많음": "many_cloud.png",
    "비": "rain.png",
    "눈": "snow.png"
}

# 기본 설정
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🌤 날씨 API 정보11")
app.geometry("500x500")

# 주소 입력 프레임
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=20)

entry = ctk.CTkEntry(input_frame, placeholder_text="분당구 삼평동", font=get_cut_font(size=14))
entry.pack(side="left", padx=5)

# 이미지 경로
image_folder = os.path.join(app_path, "images")  # images 폴더 경로


# 날씨 아이콘 업데이트 및 결과 출력 공통 로직
def update_weather_display(lat, lon, real_address, location_type="주소"):
    """위도, 경도, 주소를 받아 날씨를 조회하고 GUI를 업데이트하는 공통 함수"""
    label_info.pack_forget()
    label_result.configure(text="날씨 정보를 불러오는 중...")
    app.update_idletasks()  # 로딩 메시지 즉시 표시

    try:
        weather_info = get_weather(lat, lon)

        if "error" not in weather_info:
            temp = weather_info["temperature"]
            weather = weather_info["weather"]

            # 날씨 아이콘 설정
            icon_img_name = os.path.join(image_folder, weather_icons.get(weather, "default.png"))
            if os.path.exists(icon_img_name):
                icon_image = Image.open(icon_img_name).resize((200, 200))
                icon_ctk_image = CTkImage(light_image=icon_image, size=(200, 200))
                icon_label.configure(image=icon_ctk_image, text="")
                icon_label.image = icon_ctk_image
            else:
                icon_label.configure(image=None, text=weather)

            # 결과 출력
            label_result.configure(
                text=f"📍 {location_type}: {real_address}\n\n 🌡️ 온도 : {temp}°C\n\n🌤️ 날씨 : {weather}"
            )
        else:
            label_result.configure(text=f"🚫 날씨 정보를 불러올 수 없습니다.\n{weather_info['error']}")
            icon_label.configure(image=None, text="")

    except Exception as e:
        label_result.configure(text=f"⚠️ 오류 발생: {str(e)}")
        icon_label.configure(image=None, text="")


# 1. 주소 입력 조회 함수
def 조회():
    address = entry.get()
    if not address:
        label_result.configure(text="⚠️ 주소를 입력해주세요.")
        return

    label_result.configure(text="주소 확인 중...")
    app.update_idletasks()

    try:
        lat, lon, real_address = get_map(address)

        if lat and lon:
            update_weather_display(lat, lon, real_address, location_type="검색 지역")
        else:
            label_result.configure(text="❌ 주소를 찾을 수 없습니다.")
            icon_label.configure(image=None, text="")

    except Exception as e:
        label_result.configure(text=f"⚠️ 오류 발생: {str(e)}")
        icon_label.configure(image=None, text="")


# 2. 현재 위치 조회 함수 (새로 추가됨)
def 현재위치_조회():
    """IP 기반으로 현재 위치의 날씨를 조회합니다."""
    label_info.pack_forget()
    label_result.configure(text="현재 위치 확인 중... (IP 기반)")
    icon_label.configure(image=None, text="")
    app.update_idletasks()

    try:
        # Finish_Map (geocoding) 파일의 IP 위치 함수 사용
        lat, lon, real_address = get_current_location_ip()

        if lat and lon:
            update_weather_display(lat, lon, real_address, location_type="현재 위치")
        else:
            label_result.configure(text="❌ 현재 위치를 찾을 수 없습니다. (IP 기반 확인 실패)")
            icon_label.configure(image=None, text="")

    except Exception as e:
        label_result.configure(text=f"⚠️ 오류 발생: {str(e)}")
        icon_label.configure(image=None, text="")


# 돋보기 아이콘 버튼 (검색)
if os.path.exists("search_icon.png"):
    search_img = Image.open("search_icon.png").resize((20, 20))
    search_photo = ImageTk.PhotoImage(search_img)
    search_btn = ctk.CTkButton(input_frame, image=search_photo, text="🔍 검색", width=30, command=조회)
    search_btn.pack(side="left")
else:
    search_btn = ctk.CTkButton(input_frame, text="🔍 검색", command=조회)
    search_btn.pack(side="left")

# 🏠 현재 위치 버튼 (새로 추가됨)
current_location_btn = ctk.CTkButton(
    input_frame,
    text="🏠 현재 위치",
    width=90,
    command=현재위치_조회,
    font=get_cut_font(size=14)
)
current_location_btn.pack(side="left", padx=5)

# 초기 안내 문구 라벨 (결과 라벨 위쪽에)
label_info = ctk.CTkLabel(app, text="원하는 지역을 입력하거나 '현재 위치'를 눌러 주세요.", font=get_cut_font(size=14))
label_info.pack(pady=(150))

# 날씨 아이콘 라벨
icon_label = ctk.CTkLabel(app, text="", font=get_cut_font(size=16))
icon_label.pack(pady=10)

# 결과 텍스트 라벨
label_result = ctk.CTkLabel(app, text="", font=get_cut_font(size=14))
label_result.pack(pady=10)

app.mainloop()