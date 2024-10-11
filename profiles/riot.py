"""
description:
라이엇 API 활용해
라이엇 유저네임, 유저태그 입력하면
해당 유저가 존재한다면
프로필 아이콘, 레벨, 최근 수정일, 티어, 랭크, 승패 수, 선호 포지션 등을 반환.

작성자: 김우린
작성일: 2024-10-12
"""
import sys
import os
import requests
from urllib.parse import quote

# 현재 파일의 경로를 기준으로 상위 디렉토리(프로젝트 루트)를 PYTHONPATH에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from wpgg.settings import RIOT_API_KEY

# API 키 설정
api_key = RIOT_API_KEY

def get_user_puuid(api_key, riot_id, tag_line):
    """주어진 리그 ID와 태그라인으로 유저의 PUUID를 조회합니다."""
    encoded_riot_id = quote(riot_id)
    encoded_tag_line = quote(tag_line)

    url_puuid = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{encoded_riot_id}/{encoded_tag_line}?api_key={api_key}"

    try:
        response = requests.get(url_puuid, timeout=10)
        if response.status_code == 404:
            return None  # 유저가 존재하지 않음

        response.raise_for_status()  # HTTPError가 발생하면 예외 발생
        return response.json()['puuid']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching PUUID: {e}")
        return None

def get_user_profile(api_key, puuid):
    """PUUID로부터 유저의 프로필 정보를 조회합니다."""
    url_profile = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"

    try:
        response = requests.get(url_profile, timeout=10)
        response.raise_for_status()  # HTTPError가 발생하면 예외 발생
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile: {e}")
        return None

def get_user_league(api_key, summoner_id):
    """소환사 ID로부터 유저의 리그 정보를 조회합니다."""
    url_league = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"

    try:
        response = requests.get(url_league, timeout=10)
        response.raise_for_status()  # HTTPError가 발생하면 예외 발생
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching league info: {e}")
        return None

def get_match_ids(api_key, puuid):
    """PUUID로부터 유저의 매치 ID 목록을 조회합니다."""
    url_match_ids = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={api_key}"

    try:
        response = requests.get(url_match_ids, timeout=10)
        response.raise_for_status()  # HTTPError가 발생하면 예외 발생
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching match IDs: {e}")
        return None

def get_match_info(api_key, match_id):
    """매치 ID로부터 매치 정보를 조회합니다."""
    url_match_info = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"

    try:
        response = requests.get(url_match_info, timeout=10)
        response.raise_for_status()  # HTTPError가 발생하면 예외 발생
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching match info: {e}")
        return None

def get_user_preferred_position(api_key, puuid):
    """PUUID로부터 유저의 선호 포지션을 조회합니다."""
    match_ids = get_match_ids(api_key, puuid)
    if not match_ids:
        return "해당 유저의 매치 기록이 없습니다."

    last_match_id = match_ids[0]  # 가장 최근 매치 ID
    match_info = get_match_info(api_key, last_match_id)

    if not match_info:
        return "매치 정보 조회 실패."

    participants = match_info['info']['participants']
    for player in participants:
        if player['puuid'] == puuid:
            return player.get('teamPosition', '포지션 정보 없음')

    return "포지션 정보 없음"

def get_user_info(api_key, riot_id, tag_line):
    """유저의 정보를 종합적으로 조회합니다."""
    puuid = get_user_puuid(api_key, riot_id, tag_line)
    if not puuid:
        return {"error": "해당 유저는 존재하지 않습니다."}

    profile_data = get_user_profile(api_key, puuid)
    if not profile_data:
        return {"error": "프로필 정보를 가져오는 데 실패했습니다."}

    summoner_id = profile_data['id']
    league_data = get_user_league(api_key, summoner_id)
    preferred_position = get_user_preferred_position(api_key, puuid)

    # profileIconId를 기반으로 프로필 아이콘 URL 생성
    profile_icon_link = f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{profile_data['profileIconId']}.png"

    # 리턴할 정보 구성
    user_info = {
        "profileIconId": profile_data['profileIconId'],
        "profileIconLink": profile_icon_link,
        "summonerLevel": profile_data['summonerLevel'],
        "revisionDate": profile_data['revisionDate'],
        "league": [],
        "preferredPosition": preferred_position  # 유저의 선호 포지션 추가
    }

    # 리그 정보에서 'RANKED_SOLO_5x5' 큐 타입만 필터링하여 추가
    if league_data:
        for entry in league_data:
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

# 함수 호출 예시
riot_id = '미밀면'  # 유저 이름
tag_line = 'KR1'      # 태그라인

user_info = get_user_info(api_key, riot_id, tag_line)
print(user_info)
