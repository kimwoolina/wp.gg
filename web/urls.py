from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path("", views.index, name = "index"),
    path('register-page/', views.register_page, name='register_page'),  # 회원가입
    path('login-page/', views.login_page, name='login_page'), # 로그인
    path('home/', views.home, name='home'), # 기본 홈 화면
    path('gamechoice/', views.gamechoice, name='gamechoice'), # 게임 선택 페이지
    path('login_selection/', views.login_selection, name='login_selection'), # 게임 선택 페이지
    path('profile/', login_required(views.profile), name='profile'), # 마이페이지(조회)
    path('ranking/', views.ranking, name='ranking'), # 유저랭킹화면
    path('riotPage/', views.RiotPageView.as_view(), name='user-index'),
    path('search/', views.SearchPageView.as_view(), name='user-search'), # 유저 검색
    path('matching/', views.MatchingPageView.as_view(), name='user_matching'), 
    path('chat/', views.ChatRoomTemplateView.as_view(), name='chat-room-template'),  # 채팅방 템플릿 추가
    path('article_list/', views.article_list_page, name='article-list'), #리스트
    path('article_create/', views.article_create_page, name='article-create'), #생성
    path('', views.home, name='home'), # 기본 홈 화면
    # path('', views.indexView.as_view(), name='user_index'),
]
