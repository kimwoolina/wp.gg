from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from .serializers import UserProfileSerializer

# 디스코드 로그인
from wpgg.settings import DiscordOAuth2
from django.shortcuts import redirect
import requests
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth import get_backends


# 회원가입
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # 회원가입 완료시 메시지
        if response.status_code == status.HTTP_204_NO_CONTENT:
            response = Response({"message": "회원가입이 완료되었습니다😊"}, status=status.HTTP_201_CREATED)
        
        # if response.status_code == status.HTTP_201_CREATED:
        #     response.data['message'] = '회원가입이 완료되었습니다😊'
        
        return response

# 로그인
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            user = self.request.user
            username = user.username

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response.data = {
                'message': f'{username}님 안녕하세요😊',
                'access': access_token,
                'refresh': refresh_token
            }
            
            # access_token, refresh_token 없으면 에러 메시지 
            if not access_token or not refresh_token:
                response.data['error'] = '토큰을 발급받지 못했습니다.'

        return response
    
# 로그아웃
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request) 
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)


# 회원탈퇴
User = get_user_model()

class CustomDeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def delete(self, request, *args, **kwargs):
        user = request.user  
        user.delete() # 유저 정보 아예 삭제할건지 팀원들과 이야기해봐야 함

        logout(request)

        return Response({"message": "회원탈퇴 완료! 그동안 이용해주셔서 감사했습니다👋"}, status=status.HTTP_200_OK)
    
    
# 마이페이지 조회 및 수정
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 변경
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class discordLoginView(generic.View):
    """
    디스코드 oauth2 인증 로그인
    작성자: 김우린
    작성 날짜: 2024.10.10
    """
    
    def get(self, request):
        # if the user is logged in, they will be redirected.
        if self.request.user.is_authenticated:
            return redirect("index")

        # If the 'QUERY_STRING' is > 0, that means the code is in the url ==> oauth2/login?code=********
        elif len(self.request.META['QUERY_STRING']) > 0:
            code = self.request.GET.get('code')
            getUser = self.exchangeCode(code)
            
            # 디스코드 사용자 정보로 User 검색
            user = User.objects.filter(discord_username=getUser['username'], discord_tag=getUser['discriminator']).first()

            # 사용자가 없으면 새로 생성
            if not user:
                user = User.objects.create(
                    username=getUser['username'],
                    discord_username=getUser['username'],
                    discord_tag=getUser['discriminator'],
                    email=getUser.get('email', ''),  # 이메일이 있으면 사용, 없으면 빈 문자열
                )
                user.set_unusable_password()  # 비밀번호를 사용할 수 없게 설정
                user.save()

            # 사용자의 backend 설정
            backend = get_backends()[0]  # 첫 번째 인증 백엔드 사용 (필요 시 수정)
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            
            login(request, user)
            return redirect("user_index")

        # redirects to discord api
        else:
            return redirect(DiscordOAuth2["DISCORD_OAUTH2_URL"])

    # 디스코드 API로부터 사용자 정보를 가져오는 함수
    def exchangeCode(self, code: str):
        data = {
            "client_id": DiscordOAuth2["CLIENT_ID"],
            "client_secret": DiscordOAuth2["CLIENT_SECRET"],
            'grant_type': 'authorization_code',
            "code": code,
            "redirect_uri": DiscordOAuth2["REDIRECT_URI"],
            "scope": "identify"
        }
        
        # 토큰 요청
        response = requests.post(
            f"{DiscordOAuth2['API_ENDPOINT']}/oauth2/token", 
            data=data, 
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # 응답 상태 및 내용 출력 (디버깅 용도)
        print(response.status_code, response.text)
        response.raise_for_status()

        # 토큰 응답을 JSON으로 파싱
        token_response = response.json()
        access_token = token_response.get('access_token')

        # 액세스 토큰이 없는 경우 예외 발생
        if access_token is None:
            raise ValueError("Access token not found in the response")
        
        # 디스코드 사용자 정보를 요청
        user_response = requests.get(
            f"{DiscordOAuth2['API_ENDPOINT']}/users/@me", 
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return user_response.json()
