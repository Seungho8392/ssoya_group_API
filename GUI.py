import customtkinter as ctk


class WeatherAppUI(ctk.CTk):
    def __init__(self, controller_class):
        super().__init__()
        # 1. 로직 컨트롤러 연결 (나 자신을 조종권으로 넘겨줌)
        self.controller = controller_class(self)

        # 2. 로직에서 설정값 받아오기
        settings = self.controller.get_initial_settings()

        # 3. 창 기본 설정
        self.title(settings["title"])
        self.geometry(settings["geometry"])
        self.configure(fg_color=settings["bg_color"])

        # 4. 위젯 그리기
        self._create_widgets(settings)

    def _create_widgets(self, s):
        # [입력 영역] 프레임 생성
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20)

        # 주소 입력창
        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="분당구 삼평동",
            text_color="#FFFFFF"
        )
        self.entry.pack(side="left", padx=5)

        # 검색 버튼 (클릭 시 아래의 '화면_업데이트' 함수 실행)
        self.search_btn = ctk.CTkButton(
            self.input_frame,
            text="🔍 검색",
            command=self.화면_업데이트
        )
        self.search_btn.pack(side="left")

        # [출력 영역] 안내 라벨
        self.label_info = ctk.CTkLabel(
            self,
            text=s["info_text"],
            text_color=s["info_color"],
            font=s["info_font"]
        )
        self.label_info.pack(pady=(150, 0))

        # 날씨 아이콘 표시 라벨
        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=(10, 5))

        # 날씨 상세 정보 표시 라벨
        self.label_result = ctk.CTkLabel(
            self,
            text="",
            text_color=s["text_color"],
            font=s["result_font"],
            wraplength = 450,
            justify="center"
        )
        self.label_result.pack(pady=(15, 20))

    def 화면_업데이트(self):
        """버튼 클릭 시 실행: 로직에서 데이터(텍스트, 이미지)를 받아와서 직접 그림"""
        # 1. 로직에게 주소를 주고 결과 데이터를 받아옴
        data = self.controller.실행_조회(self.entry.get())
        if not data: return

        # 2. 안내 문구 숨기기
        self.label_info.pack_forget()
        # 3. 결과에 따른 화면 업데이트
        if "error" in data:
            self.label_result.configure(text=f"⚠️ 오류: {data['error']}")
        else:
            # 이미지 업데이트 (로직에서 생성된 이미지 객체 사용)
            if data["image"]:
                self.icon_label.configure(image=data["image"], text="")
                self.icon_label.image = data["image"]
            # 텍스트 업데이트
            self.label_result.configure(text=data["text"])