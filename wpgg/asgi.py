import os
from django.core.asgi import get_asgi_application

# 환경변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django ASGI 애플리케이션 초기화
django_asgi_app = get_asgi_application()

# channels 라우팅과 미들웨어는 Django 초기화 이후에 가져와야 합니다.
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chats.routing  # 이제 이 코드는 안전하게 실행될 수 있습니다.


# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application
# from django.urls import path
# from chats.consumers import ChatConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wpgg.settings')

# django.setup()

# # WebSocket 경로 설정
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # HTTP 연결
#     "websocket": AuthMiddlewareStack(  # 웹소켓 연결
#         URLRouter([
#             path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),
#         ])
#     ),
# })

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": 
        AuthMiddlewareStack(
            AllowedHostsOriginValidator(
            URLRouter(
                chats.routing.websocket_urlpatterns
            )     
        ),
    ),
})
