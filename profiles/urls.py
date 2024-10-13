from django.urls import path
from . import views

urlpatterns = [ 
    path('matching/', views.MatchingPageView.as_view(), name='user_matching'),
    path('usrecommendations/', views.UserRecommendationView.as_view(), name='user_recommendations'), # 유저 추천 기능
    path('rankings/', views.MannerRankingView.as_view(), name='user-rankings'), # 매너 랭킹
    path('search/', views.SearchPageView.as_view(), name='user-search'), # 유저 검색
    path('riotPage/', views.RiotPageView.as_view(), name='user-index'),
    path('riot/', views.GetRiotInfoView.as_view(), name='user-profile'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user-detail'), # 특정 유저 검색 기능
]
