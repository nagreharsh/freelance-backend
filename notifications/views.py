from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import action


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-timestamp")

    @action(detail=True, methods=["patch"], url_path="read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()

        if notification.user != request.user:
            raise PermissionDenied("You cannot modify this notification.")

        notification.is_read = True
        notification.save()

        return Response({"message": "Notification marked as read"})
    
    @action(detail=False, methods=["get"], url_path="unread-count")
    def unread_count(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
            ).count()
        return Response({"unread_count": count})