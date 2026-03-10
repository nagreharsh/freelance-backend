import logging
logger = logging.getLogger(__name__)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from notifications.models import Notification
from rest_framework.exceptions import ValidationError, PermissionDenied
from contracts.models import Contract


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        contract_id = self.request.query_params.get("contract")

        if contract_id:
            return Review.objects.filter(contract_id=contract_id)

        return Review.objects.none()

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

        reviews = Review.objects.filter(contract=contract)
        serializer = self.get_serializer(reviews, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        contract = serializer.validated_data['contract']

    # 1️⃣ Contract must be completed
        if contract.status != "completed":
            raise ValidationError("Cannot review an incomplete contract.")

    # 2️⃣ Prevent duplicate review (IMPORTANT FIX)
        if Review.objects.filter(contract=contract, reviewer=user).exists():
            raise ValidationError("You have already reviewed this contract.")

    # 3️⃣ Determine reviewee
        reviewee = (
            contract.freelancer
            if user == contract.client
            else contract.client
        )
        
        serializer.save(
            reviewer=user,
            reviewee=reviewee
        )

        logger.info(
            f"Review submitted contract={contract.id} reviewer={user.username} reviewee={reviewee.username}"
        )

    # 4️⃣ Create notification
        Notification.objects.create(
            user=reviewee,
            message=f"You received a new review from {user.username}."
        )