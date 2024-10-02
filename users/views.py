from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import PasswordChangeForm


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