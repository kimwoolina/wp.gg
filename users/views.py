from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status

class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # 회원가입 완료시 메시지
        if response.status_code == status.HTTP_201_CREATED:
            response.data['message'] = '회원가입이 완료되었습니다😊'
        
        return response
    

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = self.request.user
            username = user.username
            response.data['message'] = f'{username}님 안녕하세요😊'
        return response


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "logout👌"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=response.status_code)
