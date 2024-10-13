from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [ 
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Access와 Refresh 토큰 발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh 토큰 갱신
    path('delete/', views.CustomDeleteUserView.as_view(), name='delete_user'), 
    path('api/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('discordlogin/', views.discordLoginView.as_view(), name='discord-login'), #디스코드로 로그인
    # Riot 로그인 관련 URL
    # path('riot/', views.login_with_riot, name='login_with_riot'),  # auth/riot/
    # path('riot/callback/', views.riot_callback, name='riot_callback'),  # auth/riot/callback/
]