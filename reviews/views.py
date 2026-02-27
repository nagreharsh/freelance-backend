from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from notifications.models import Notification
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        contract_id = self.request.query_params.get("contract")

        if contract_id:
            return Review.objects.filter(contract_id=contract_id)

        return Review.objects.none()

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

    # 4️⃣ Create notification
        Notification.objects.create(
            user=reviewee,
            message=f"You received a new review from {user.username}."
            )