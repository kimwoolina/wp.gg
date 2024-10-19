import json
from django.core.cache import cache


# 캐시 가져오기
def cache_get(key):
    data = cache.get(key)
    return json.loads(data) if data else None

# 캐시 저장
def cache_set(key, value):
    cache.set(key, json.dumps(value), timeout=3600)  # 1시간 동안 캐시 저장
    