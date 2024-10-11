from django.urls import path
from articles import views

app_name = "articles"
urlpatterns = [
    path('', views.ArticleAPIView.as_view(), name='articles'), #리스트,생성
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'), #상세
    path('comment/<int:pk>/', views.CommentAPIView.as_view(), name='comment'), #댓글

    #FE
    path('article-list-page/', views.article_list_page, name='list'),
    path('create-page/', views.article_create_page, name='create'),
]