from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationListView, ReportsViewSet

router = DefaultRouter()
router.register(r'reports', ReportsViewSet)

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('', include(router.urls)),
]
