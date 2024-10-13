from django.urls import path
from . import views

# app_name = 'profile'

urlpatterns = [ 
    path('recommendation/', views.UserRecommendationView.as_view(), name='user-recommendation'), # 유저 추천 기능
    path('rankings/', views.MannerRankingView.as_view(), name='user-rankings'), # 매너 랭킹
    path('riot/', views.GetRiotInfoView.as_view(), name='user-profile'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user-detail'), # 특정 유저 검색 기능
]
