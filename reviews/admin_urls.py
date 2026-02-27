from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .admin_views import AdminReviewViewSet

router = DefaultRouter()
router.register(r"", AdminReviewViewSet, basename="admin-reviews")

urlpatterns = [
    path("", include(router.urls)),
]