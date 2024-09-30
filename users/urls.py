# users/urls.py

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
]
