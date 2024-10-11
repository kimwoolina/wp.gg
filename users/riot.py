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
summoner_id = 'lynpeep'

# 북미서버 테스트
# riot_id = 'exsmiley'
# tag_line = 'smile'

# 유저네임, 유저태그로 puuid 얻기
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


def get_profile_by_puuid(api_key, puuid):
    
    #한국 서버
    url_profile = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
    
    # 북미서버
    #url_puuid = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{encoded_tag_line}?api_key={api_key}"

    try:
        response_profile = requests.get(url_profile, timeout=10)  # 타임아웃 추가
        print(f"Response Status Code: {response_profile.status_code}")  # 응답 코드 확인

        if response_profile.status_code == 200:
            data_profile = response_profile.json()
            print(f"profile: {data_profile}")
            return data_profile
        else:
            print(f"Error: Status Code {response_profile.status_code}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        

def get_league_by_uid(api_key, uid):
    
    #한국 서버
    url_league = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{uid}?api_key={api_key}"
    
    try:
        response_league = requests.get(url_league, timeout=10)  # 타임아웃 추가
        print(f"Response Status Code: {response_league.status_code}")  # 응답 코드 확인

        if response_league.status_code == 200:
            data_league = response_league.json()
            print(f"league: {data_league}")
            return data_league
        else:
            print(f"Error: Status Code {response_league.status_code}")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  





# 함수 호출
get_puuid(api_key, riot_id, tag_line)


puuid = 'eLG4Ar5xPfzO_lo7Ganx2dG5YZDxPpi48xuwmHb2YBFH3Ia1RsKJmVGqppIf84fOGFH4zTtMlkP43w'
get_profile_by_puuid(api_key, puuid)

uid = 'dFrpUMMl6KFwwQr9EUWcBk53vReJRE7LspCmW7IEqensew'
get_league_by_uid(api_key, uid)

