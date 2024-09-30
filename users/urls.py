from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('delete/', views.CustomDeleteUserView.as_view(), name='delete_user'),
]