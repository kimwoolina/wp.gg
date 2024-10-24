from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'chats'

urlpatterns = [
    # path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    # path('', include(router.urls)),
    # path('', views.index, name="index"),
    path('chatrooms/', views.PrivateChatRoomListView.as_view(), name='chat-room-list'),
    path('private-chat/', views.PrivateChatRoomCreateView.as_view(), name='create-private-chat-room'),
    path('private-chats/<int:room_id>/messages/', views.PrivateChatMessageList.as_view(), name='private-chat-message-list'),  # GET: 1:1 채팅방의 메시지 리스트

    # Group chat (단체 채팅) 관련 URL
    path('group-chat/', views.GroupChatRoomCreateView.as_view(), name='create-group-chat-room'),  # 그룹 채팅방 생성
    path('group-chats/<int:group_chat_id>/messages/', views.GroupChatMessageList.as_view(), name='group-chat-message-list'),  # GET: 그룹 채팅방의 메시지 리스트
    path('group-chats/<int:group_chat_id>/messages/create/', views.GroupChatMessageCreate.as_view(), name='create-group-chat-message'),  # POST: 그룹 채팅 메시지 생성
]
