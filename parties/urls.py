from django.urls import path
from . import views

app_name = "parties"
urlpatterns = [
    path('', views.PartyView.as_view(), name="create_party"),
    path('<int:party_pk>/', views.PartyDetailView.as_view(), name="delete_party"),
    path('<int:party_pk>/<str:position>', views.PartyExileView.as_view()),# 파티 추방
    # path('napi/', views.PurePartyView.as_view()),
    # path('napi/<int:party_pk>/', views.PurePartyDetailView.as_view()),
    # path('napi/<int:party_pk>/<str:position>', views.PurePartyExileView.as_view()),# 파티 추방
]