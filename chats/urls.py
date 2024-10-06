from django.urls import path
from . import views


urlpatterns = [
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat_rooms'),
    path('<int:room_id>/messages', views.MessageListView.as_view(), name='chat_messages'),
    path('group-chats/', views.GroupChatListCreateView.as_view(), name='group-chat-list-create'),
    path('group-chats/<int:group_chat_id>/messages/', views.GroupChatMessageListView.as_view(), name='group-chat-message-list-create'),
    path('', views.TemplateView.as_view(template_name='chat.html'), name='chat'),
    path('message/<str:username>', views.SendMessageView.as_view(), name='send_message'),
]