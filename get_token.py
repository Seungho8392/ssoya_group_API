import requests
import json

# 1. 정보 설정 (본인의 REST API 키를 꼭 넣어주세요!)
rest_api_key = "32da76349d1c1fe08001a6f3fd317ed1"
redirect_uri = "http://localhost"
authorize_code = "페이지 링크 code 입력"

# 2. 카카오 서버에 토큰 요청
url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": rest_api_key,
    "redirect_uri": redirect_uri,
    "code": authorize_code,
}

response = requests.post(url, data=data)
tokens = response.json()

# 3. 결과 확인 및 파일 저장
if "access_token" in tokens:
    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)
    print("✅ 성공! 토큰이 kakao_token.json 파일에 저장되었습니다.")
    print(f"Access Token: {tokens['access_token']}")
else:
    print("❌ 실패! 에러 메시지를 확인하세요:")
    print(tokens)