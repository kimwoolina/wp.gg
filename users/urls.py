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
    path('profile/', login_required(views.profile), name='profile'), # 마이페이지(조회)
    path('users/rankings/', views.MannerRankingView().as_view(), name='user-rankings'), # 매너 랭킹
    path('users/<str:username>/', views.UserDetailView().as_view(), name='user_detail'), # 특정 유저 검색 기능
]