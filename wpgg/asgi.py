import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chats.consumers import ChatConsumer
from django.urls import path
from django.core.asgi import get_asgi_application

# 환경변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wp.gg.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),  # WebSocket 경로 설정
        ])
    ),
})