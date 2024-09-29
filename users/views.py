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
