import logging
logger = logging.getLogger(__name__)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Message
from .serializers import MessageSerializer
from contracts.models import Contract
from notifications.models import Notification


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def retrieve(self, request, pk=None):
        user = request.user

        try:
            contract = Contract.objects.get(id=pk)
        except Contract.DoesNotExist:
            return Response(
                {"detail": "Contract not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if user not in [contract.client, contract.freelancer]:
            raise PermissionDenied("You are not part of this contract.")

        messages = Message.objects.filter(contract=contract).order_by("timestamp")
        serializer = self.get_serializer(messages, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        contract = serializer.validated_data["contract"]

    # Only participants can send message
        if user not in [contract.client, contract.freelancer]:
            raise PermissionDenied("You are not part of this contract.")

    # Determine receiver automatically
        receiver = (
            contract.freelancer
            if user == contract.client
            else contract.client
        )

        message = serializer.save(sender=user, receiver=receiver)

        logger.info(
            f"Message sent contract={contract.id} sender={user.username} receiver={receiver.username}"
        )

    # Notification for receiver
        Notification.objects.create(
            user=receiver,
            contract=contract,
            type="message",
            message=f"New message from {user.username}"
        )

    @action(detail=True, methods=["patch"], url_path="read")
    def mark_as_read(self, request, pk=None):
        message = self.get_object()

        if request.user != message.receiver:
            raise PermissionDenied("Only receiver can mark as read.")

        message.is_read = True
        message.save()

        logger.info(
            f"Message read id={message.id} by user={request.user.username}"
        )

        return Response({"message": "Message marked as read"})