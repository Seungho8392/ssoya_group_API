import requests
import json
import os


# 1. 토큰 갱신 함수
def refresh_kakao_token(rest_api_key, refresh_token):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    return response.json()


# 2. 메인 실행 부분
def send_weather_msg():
    # 저장된 토큰 정보 읽기
    with open("kakao_token.json", "r") as fp:
        tokens = json.load(fp)

    rest_api_key = "32da76349d1c1fe08001a6f3fd317ed1"

    # 메시지 전송 시도
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # (여기에 사용자님의 날씨 데이터 생성 코드 포함)
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": "☀️ [자동알림] 오늘의 날씨입니다...",
            "link": {"web_url": "https://localhost", "mobile_web_url": "https://localhost"}
        })
    }

    res = requests.post(url, headers=headers, data=data)

    # 만약 토큰이 만료되었다면 (401 에러) 갱신 후 재전송
    if res.status_code == 401:
        print("토큰 만료! 갱신을 시도합니다...")
        new_tokens = refresh_kakao_token(rest_api_key, tokens['refresh_token'])

        # 새로운 access_token으로 업데이트
        tokens['access_token'] = new_tokens.get('access_token', tokens['access_token'])
        if 'refresh_token' in new_tokens:  # refresh_token도 갱신될 수 있음
            tokens['refresh_token'] = new_tokens['refresh_token']

        with open("kakao_token.json", "w") as fp:
            json.dump(tokens, fp)

        # 재전송
        headers["Authorization"] = f"Bearer {tokens['access_token']}"
        res = requests.post(url, headers=headers, data=data)

    print(f"결과: {res.status_code}")


send_weather_msg()