import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from chats.consumers import ChatConsumer


# 환경변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wpgg.settings')

application = get_asgi_application()

# Django 초기화
django.setup()

# ASGI 애플리케이션 설정
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),  # WebSocket 경로 설정
        ])
    ),
})
