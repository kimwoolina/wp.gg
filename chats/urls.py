from django.urls import path, include
from . import views


urlpatterns = [
    # path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    # path('', include(router.urls)),
    # path('', views.index, name="index"),
    path('', views.ChatRoomTemplateView.as_view(), name='chat-room-template'),  # 채팅방 템플릿 추가
    path('chatrooms/', views.PrivateChatRoomListView.as_view(), name='chat-room-list'),
    path('private-chat/', views.PrivateChatRoomCreateView.as_view(), name='create-private-chat-room'),
    path('private-chats/<int:room_id>/messages/', views.PrivateChatMessageList.as_view(), name='private-chat-message-list'),  # GET: 1:1 채팅방의 메시지 리스트
    path('private-chats/<int:room_id>/messages/create/', views.PrivateChatMessageCreate.as_view(), name='create-private-chat-message'),  # POST: 1:1 채팅 메시지 생성

    # Group chat (단체 채팅) 관련 URL
    path('group-chat/', views.GroupChatRoomCreateView.as_view(), name='create-group-chat-room'),  # 그룹 채팅방 생성
    path('group-chats/<int:group_chat_id>/messages/', views.GroupChatMessageList.as_view(), name='group-chat-message-list'),  # GET: 그룹 채팅방의 메시지 리스트
    path('group-chats/<int:group_chat_id>/messages/create/', views.GroupChatMessageCreate.as_view(), name='create-group-chat-message'),  # POST: 그룹 채팅 메시지 생성

    ]
