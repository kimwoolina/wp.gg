from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleAPIView.as_view(), name='articles'), #리스트, 생성
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'), #상세
    path('comment/<int:pk>/', views.CommentAPIView.as_view(), name='comment'), #댓글
]