from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, consumers

router = DefaultRouter()
router.register(r'reports', views.ReportsViewSet)

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('', include(router.urls)),
    # WebSocket URL    # 단체 채팅방 WebSocket 경로
    path('ws/group-chat/', consumers.PresenceConsumer.as_asgi(), name='group_chat_ws'),
    # 개인 채팅방 WebSocket 경로
    path('ws/private-chat/', consumers.ChatConsumer.as_asgi(), name='private_chat_ws'),
    path('', views.index, name="index"),
]
