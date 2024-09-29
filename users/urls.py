from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    path('auth/login/', views.CustomLoginView.as_view(), name='custom_login'),
]