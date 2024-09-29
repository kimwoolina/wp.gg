from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomRegisterView.as_view(), name='register'), 
]
