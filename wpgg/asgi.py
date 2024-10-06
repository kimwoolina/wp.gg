import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from chats.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wpgg.settings')

django.setup()

# WebSocket 경로 설정
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP 연결
    "websocket": AuthMiddlewareStack(  # 웹소켓 연결
        URLRouter([
            path('ws/chat/<str:room_id>/', ChatConsumer.as_asgi()),
        ])
    ),
})
