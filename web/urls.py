from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name = "index"),
    path('ranking/', views.ranking, name='ranking'), # 유저랭킹화면
    path('riotPage/', views.RiotPageView.as_view(), name='user-index'),
    path('search/', views.SearchPageView.as_view(), name='user-search'), # 유저 검색
    path('matching/', views.MatchingPageView.as_view(), name='user_matching'), 
    path('chat/', views.ChatRoomTemplateView.as_view(), name='chat-room-template'),  # 채팅방 템플릿 추가
    path('article-list/', views.article_list_page, name='list'), #리스트
    path('article-create/', views.article_create_page, name='create'), #생성
]
