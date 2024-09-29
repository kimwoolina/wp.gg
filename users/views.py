from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

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
            response.data['message'] = '로그인 성공😊'
        
        return response
