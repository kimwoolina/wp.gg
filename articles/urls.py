from django.urls import path
from articles import views

app_name = "articles"
urlpatterns = [
    path('', views.ArticleAPIView.as_view(), name='articles'), #리스트,생성
    path('comment/<int:pk>/', views.CommentAPIView.as_view(), name='comment'), #댓글
    path('search_user/', views.RevieweeSearchView.as_view(), name='search-user'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'), #상세
]