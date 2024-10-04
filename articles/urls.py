from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleListAPIView.as_view(), name='article_list'),
]