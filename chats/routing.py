from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # 단체 채팅방 WebSocket 경로
    path('ws/group-chat/<str:room_name>/', consumers.ChatConsumer.as_asgi(), name='group_chat_ws'),
    # 개인 채팅방 WebSocket 경로
    path('ws/private-chat/<str:room_name>/', consumers.ChatConsumer.as_asgi(), name='private_chat_ws'),
]
