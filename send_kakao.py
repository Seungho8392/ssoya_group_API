import requests
import json
import os
from datetime import datetime, timedelta, timezone
from Finish_Map import get_map
from Finish_Weather import get_weather

# 설정값
REST_API_KEY = "32da76349d1c1fe08001a6f3fd317ed1"
TOKEN_FILE = "kakao_token.json"


def load_all_tokens():
    """모든 사용자의 토큰 리스트를 로드"""
    with open(TOKEN_FILE, "r") as fp:
        return json.load(fp)


def update_tokens(refresh_token):
    """특정 사용자의 리프레시 토큰으로 새로운 액세스 토큰 발급"""
    # ⚠️ kapi -> kauth 주소 수정됨
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    return response.json()


def send_weather_kakao(address_query="삼평동"):
    # 1. 토큰 파일에서 모든 사용자 정보 가져오기
    user_list = load_all_tokens()

    # 2. 날씨 데이터는 공통이므로 한 번만 가져오기
    lat, lon, real_address = get_map(address_query)
    weather_data = get_weather(lat, lon)

    # 한국 시간 설정
    KST = timezone(timedelta(hours=9))
    now_str = datetime.now(KST).strftime("%Y-%m-%d %H:%M")

    message = (
        f"📅 [{now_str}] 날씨 리포트\n"
        f"📍 위치: {real_address}\n"
        f"🌡️ 온도: {weather_data['temperature']}°C\n"
        f"🌤️ 상태: {weather_data['weather']}\n\n"
        f"좋은 하루 보내세요! 🍀"
    )

    # 3. 반복문을 돌며 각 사용자에게 발송
    updated = False
    for user in user_list:
        print(f"> {user['name']}에게 전송 시도 중...")

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": f"Bearer {user['access_token']}"}
        payload = {
            "object_type": "text",
            "text": message,
            "link": {"web_url": "https://www.google.com", "mobile_web_url": "https://www.google.com"}
        }

        res = requests.post(url, headers=headers, data={'template_object': json.dumps(payload)})

        # 4. 토큰 만료 시 해당 사용자 토큰만 갱신
        if res.status_code == 401:
            print(f"  - {user['name']} 토큰 만료! 갱신 시도...")
            new_tokens = update_tokens(user['refresh_token'])

            if 'access_token' in new_tokens:
                user['access_token'] = new_tokens['access_token']
                if 'refresh_token' in new_tokens:
                    user['refresh_token'] = new_tokens['refresh_token']

                # 새 토큰으로 재발송
                headers["Authorization"] = f"Bearer {user['access_token']}"
                res = requests.post(url, headers=headers, data={'template_object': json.dumps(payload)})
                updated = True  # 파일 저장을 위해 변경 표시
            else:
                print(f"  - {user['name']} 토큰 갱신 실패: {new_tokens}")

        if res.status_code == 200:
            print(f"  - {user['name']} 전송 성공! 🎉")
        else:
            print(f"  - {user['name']} 전송 실패: {res.text}")

    # 5. 토큰이 하나라도 갱신되었다면 파일 다시 저장
    if updated:
        with open(TOKEN_FILE, "w") as fp:
            json.dump(user_list, fp, indent=2)
            print("새로운 토큰 정보를 저장했습니다.")


if __name__ == "__main__":
    send_weather_kakao("삼평동")