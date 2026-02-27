from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .admin_views import AdminContractViewSet

router = DefaultRouter()
router.register(r"", AdminContractViewSet, basename="admin-contracts")

urlpatterns = [
    path("", include(router.urls)),
]