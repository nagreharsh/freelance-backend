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

    # If detail view (like /1/read/)
        if self.kwargs.get("pk"):
            return Message.objects.filter(
                sender=user
                ) | Message.objects.filter(
                    receiver=user
                    )

    # If list view (chat history)
        contract_id = self.request.query_params.get("contract")
        
        if not contract_id:
            return Message.objects.none()
        
        try:
            contract = Contract.objects.get(id=contract_id)
        except Contract.DoesNotExist:
            return Message.objects.none()
        
        if user not in [contract.client, contract.freelancer]:
            
            raise PermissionDenied("You are not part of this contract.")
        return Message.objects.filter(contract=contract).order_by("timestamp")

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

        return Response({"message": "Message marked as read"})