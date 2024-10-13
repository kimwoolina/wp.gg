#users/auth.py

from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser

# class DiscordAuthenticationBackend(BaseBackend):
#     def authenticate(self, request, user) -> DiscordUser:
#         findUser = DiscordUser.objects.filter(id=user['id'])
#         if len(findUser) == 0:
#             newUser = DiscordUser.objects.createNewUser(user)
#             return newUser
#         return findUser

#     def get_user(self, user_id):
#         try:
#             return DiscordUser.objects.get(pk=user_id)
#         except DiscordUser.DoesNotExist:
#             return None 
        
from django.contrib.auth import get_user_model

class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        User = get_user_model()  # 현재 설정된 사용자 모델을 가져옵니다.
        findUser = User.objects.filter(id=user['id']).first()  # Discord 사용자 ID로 사용자 검색

        if findUser is None:
            newUser = DiscordUser.objects.createNewUser(user)  # 새로운 사용자 생성
            return newUser
        return findUser  # 기존 사용자 반환

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)  # 사용자 ID로 사용자 반환
        except User.DoesNotExist:
            return None 
