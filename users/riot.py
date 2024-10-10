import sys
import os
import requests
from urllib.parse import quote

# 현재 파일의 경로를 기준으로 상위 디렉토리(프로젝트 루트)를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from wpgg.settings import RIOT_API_KEY

# API 키와 소환사 정보 설정
api_key = RIOT_API_KEY
riot_id = '캣티천사'
tag_line = 'KR1'

# 북미서버 테스트
# riot_id = 'exsmiley'
# tag_line = 'smile'

def get_puuid(api_key, riot_id, tag_line):
    encoded_riot_id = quote(riot_id)
    encoded_tag_line = quote(tag_line)
    #아시아 서버
    url_puuid = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{encoded_tag_line}?api_key={api_key}"

    # 북미서버
    #url_puuid = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{encoded_tag_line}?api_key={api_key}"


    try:
        response_puuid = requests.get(url_puuid, timeout=10)  # 타임아웃 추가
        print(f"Response Status Code: {response_puuid.status_code}")  # 응답 코드 확인

        if response_puuid.status_code == 200:
            data_puuid = response_puuid.json()
            puuid = data_puuid['puuid']
            print(f"PUUID: {puuid}")
            return puuid
        else:
            print(f"Error: Status Code {response_puuid.status_code}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


# 함수 호출
get_puuid(api_key, riot_id, tag_line)
