import sys
import os
import requests
from urllib.parse import quote

# 현재 파일의 경로를 기준으로 상위 디렉토리(프로젝트 루트)를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from wpgg.settings import RIOT_API_KEY

# API 키 설정
api_key = RIOT_API_KEY

# 유저네임과 태그로 유저 존재 여부 확인 후 프로필과 리그 정보를 얻는 함수
def get_user_info(api_key, riot_id, tag_line):
    encoded_riot_id = quote(riot_id)
    encoded_tag_line = quote(tag_line)

    # 아시아 서버 URL 설정 (유저 존재 여부 확인)
    url_puuid = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{encoded_tag_line}?api_key={api_key}"

    try:
        # 유저 PUUID 조회
        response_puuid = requests.get(url_puuid, timeout=10)
        if response_puuid.status_code == 404:
            return {"error": "해당 유저는 존재하지 않습니다."}

        if response_puuid.status_code != 200:
            return {"error": f"Error: Status Code {response_puuid.status_code}"}

        # 유저가 존재하는 경우 PUUID를 얻음
        data_puuid = response_puuid.json()
        puuid = data_puuid['puuid']

        # 한국 서버 프로필 정보 조회
        url_profile = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
        response_profile = requests.get(url_profile, timeout=10)
        
        if response_profile.status_code != 200:
            return {"error": f"Error: Status Code {response_profile.status_code}"}

        data_profile = response_profile.json()
        summoner_id = data_profile['id']  # 리그 정보 조회를 위한 소환사 ID

        # profileIconId를 기반으로 프로필 아이콘 URL 생성
        profile_icon_link = f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{data_profile['profileIconId']}.png"

        # 한국 서버 리그 정보 조회
        url_league = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
        response_league = requests.get(url_league, timeout=10)
        
        if response_league.status_code != 200:
            return {"error": f"Error: Status Code {response_league.status_code}"}

        data_league = response_league.json()

        # 리턴할 정보 구성
        user_info = {
            "profileIconId": data_profile['profileIconId'],
            "profileIconLink": profile_icon_link,  # 프로필 아이콘 URL 추가
            "summonerLevel": data_profile['summonerLevel'],
            "revisionDate": data_profile['revisionDate'],
            "league": []
        }

        # 리그 정보에서 'RANKED_SOLO_5x5' 큐 타입만 필터링하여 추가
        for entry in data_league:
            if entry['queueType'] == 'RANKED_SOLO_5x5':
                league_info = {
                    "tier": entry['tier'],
                    "rank": entry['rank'],
                    "leaguePoints": entry['leaguePoints'],
                    "wins": entry['wins'],
                    "losses": entry['losses'],
                    "veteran": entry['veteran'],
                    "inactive": entry['inactive'],
                    "freshBlood": entry['freshBlood'],
                    "hotStreak": entry['hotStreak']
                }
                user_info["league"].append(league_info)

        return user_info

    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}


# 함수 호출 예시
riot_id = '미밀면'  # 유저 이름
tag_line = 'KR1'      # 태그라인

user_info = get_user_info(api_key, riot_id, tag_line)
print(user_info)
