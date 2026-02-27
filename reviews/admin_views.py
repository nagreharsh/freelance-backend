from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .serializers import ReviewSerializer
from common.permissions import IsAdminRole


class AdminReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all().order_by("-timestamp")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]