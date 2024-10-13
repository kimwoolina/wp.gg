from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [ 
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Access와 Refresh 토큰 발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh 토큰 갱신
    path('delete/', views.CustomDeleteUserView.as_view(), name='delete_user'), 
    path('api/profile/', views.UserProfileView.as_view(), name='user_profile'),

    # 프론트엔드용 경로
    path('register-page/', views.register_page, name='register_page'),  # 회원가입
    path('login-page/', views.login_page, name='login_page'), # 로그인
    path('home/', views.home, name='home'), # 기본 홈 화면
    path('gamechoice/', views.gamechoice, name='gamechoice'), # 게임 선택 페이지
    path('login_selection/', views.login_selection, name='login_selection'), # 게임 선택 페이지
    path('profile/', login_required(views.profile), name='profile'), # 마이페이지(조회)
    # 디스코드 경로
    path('discordlogin/', views.discordLoginView.as_view(), name='discord-login'), #디스코드로 로그인
    path('', views.indexView.as_view(), name='user_index'),
    
    # Riot 로그인 관련 URL
    # path('riot/', views.login_with_riot, name='login_with_riot'),  # auth/riot/
    # path('riot/callback/', views.riot_callback, name='riot_callback'),  # auth/riot/callback/
]