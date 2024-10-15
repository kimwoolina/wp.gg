from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import UserProfileSerializer
from .validators import validate_email, validate_username_length
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.views.decorators.cache import never_cache
from .serializers import UserProfileSerializer

# 디스코드 로그인
from wpgg.settings import DiscordOAuth2
from django.shortcuts import redirect
import requests
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth import get_backends
from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@never_cache
def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def delete_session(request):
    if request.method == 'POST':
        # 세션 삭제
        request.session.flush()  # 모든 세션 데이터 삭제
        logout(request)  # 로그아웃 처리
        return JsonResponse({'message': '세션 삭제 완료'}, status=200)
    return JsonResponse({'error': '잘못된 요청'}, status=400)


# 회원가입
class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        print(f"Received data: {request.data}")
        
        email = request.data.get('email')
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        # 필수 필드가 비어있을 경우 에러 처리
        if not email or not username or not password1:
            return Response({'error': '이메일, 유저네임, 비밀번호를 모두 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # 기본 회원가입 로직 수행
        response = super().create(request, *args, **kwargs)

        # 회원가입 성공 시 로그인 페이지로 리다이렉트
        if response.status_code == status.HTTP_201_CREATED:
            return redirect('login_page')

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
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({"error": "리프레시 토큰이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 리프레시 토큰을 파싱하고 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가
            logout(request)
            return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)
        
        except TokenError:
            # 토큰이 유효하지 않거나 만료된 경우
            return Response({"error": "유효하지 않거나 만료된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
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
        if self.request.user.is_authenticated:
            return redirect("home")

        # URL에 코드가 있는 경우
        elif len(self.request.META['QUERY_STRING']) > 0:
            code = self.request.GET.get('code')
            getUser = self.exchangeCode(code)

            # 디스코드 사용자 정보로 User 검색
            user = User.objects.filter(
                discord_username=getUser['username'], 
                discord_tag=getUser['discriminator']
            ).first()

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

            # 로그인 처리
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend  # 인증 백엔드 설정
            login(request, user)  # Django 인증 시스템에 사용자 로그인 처리

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # JWT 토큰 세션에 저장 (선택 사항)
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token

            # 로그인 성공 후 다른 페이지로 리다이렉트
            return redirect(f"/home/?access={access_token}&refresh={refresh_token}")


        # 코드가 없으면 디스코드 API로 리다이렉트
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
        
        # 사용자 정보 요청 실패 처리
        user_response.raise_for_status()
        return user_response.json()
