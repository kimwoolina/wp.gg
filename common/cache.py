import json
from django.core.cache import cache


# 캐시 가져오기
def cache_get(key):
    # 캐시에서 값을 가져오기
    cached_value = cache.get(key)  # 캐시에서 값 가져오기
    if cached_value:
        # 캐시된 값이 있을 경우, 값이 문자열이면 JSON으로 변환, 이미 딕셔너리면 그대로 반환
        return json.loads(cached_value) if not isinstance(cached_value, dict) else cached_value
    return None

# 캐시 저장
def cache_set(key, value):
    cache.set(key, json.dumps(value), timeout=3600)  # 1시간 동안 캐시 저장
    