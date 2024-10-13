from django.urls import path
from . import views

# app_name = 'profile'

urlpatterns = [ 
    # 랜더링
    path('ranking/', views.ranking, name='ranking'), # 유저랭킹화면
    path('riotPage/', views.RiotPageView.as_view(), name='user-index'),
    path('search/', views.SearchPageView.as_view(), name='user-search'), # 유저 검색
    path('matching/', views.MatchingPageView.as_view(), name='user_matching'), 
    
    path('recommendation/', views.UserRecommendationView.as_view(), name='user-recommendation'), # 유저 추천 기능
    path('rankings/', views.MannerRankingView.as_view(), name='user-rankings'), # 매너 랭킹
    path('riot/', views.GetRiotInfoView.as_view(), name='user-profile'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user-detail'), # 특정 유저 검색 기능
]
