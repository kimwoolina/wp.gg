from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reports', views.ReportsViewSet)

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('', include(router.urls)),
    path('', views.index, name="index"),
]
