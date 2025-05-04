import requests
import json

def get_weather(lat, lon):
    url = f"http://api.weatherapi.com/v1/current.json?key=0b54164b5cac4d88b6281309250405&q={lat},{lon}&aqi=no"

    try:
        response = requests.get(url)

        # 상태 코드 확인
        if response.status_code != 200:
            print(f"HTTP Error {response.status_code}")
            return {"error": f"HTTP Error {response.status_code}"}

        # 응답 내용 확인
        print("Response Text:", response.text)

        # JSON 응답 파싱
        data = response.json()  # JSONDecodeError 발생할 수 있음
        return data

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return {"error": "Request failed"}
    except json.decoder.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {"error": "Invalid JSON response"}