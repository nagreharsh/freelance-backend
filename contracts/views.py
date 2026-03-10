import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Contract
from .serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]  # Prevent delete/create via API

    def get_queryset(self):
        user = self.request.user

        # Admin can see all contracts
        if user.role == "admin":
            return Contract.objects.all()

        # Client sees their contracts
        if user.role == "client":
            return Contract.objects.filter(client=user)

        # Freelancer sees their contracts
        if user.role == "freelancer":
            return Contract.objects.filter(freelancer=user)

        return Contract.objects.none()

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        contract = self.get_object()
        user = request.user
        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = ["active", "completed", "disputed"]

        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prevent same status update
        if contract.status == new_status:
            return Response(
                {"error": "Contract is already in this status."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Draft → Active (Only client can activate)
        if contract.status == "draft" and new_status == "active":
            if user != contract.client:
                raise PermissionDenied("Only client can activate contract.")

            contract.status = "active"
            contract.start_date = timezone.now()
            contract.save()

            logger.info(
                f"Contract activated id={contract.id} client={contract.client.username} "
                f"freelancer={contract.freelancer.username}"
            )

            return Response(
                {
                    "message": "Contract activated",
                    "contract_id": contract.id,
                    "new_status": contract.status,
                }
            )

        # Active → Completed (Only participants)
        if contract.status == "active" and new_status == "completed":
            if user not in [contract.client, contract.freelancer]:
                raise PermissionDenied(
                    "Only participants can complete contract."
                )

            contract.status = "completed"
            contract.end_date = timezone.now()
            contract.save()

            logger.info(
                f"Contract completed id={contract.id} by user={user.username}"
            )

            return Response(
                {
                    "message": "Contract completed",
                    "contract_id": contract.id,
                    "new_status": contract.status,
                }
            )

        # Active → Disputed (Only participants)
        if contract.status == "active" and new_status == "disputed":
            if user not in [contract.client, contract.freelancer]:
                raise PermissionDenied(
                    "Only participants can dispute contract."
                )

            contract.status = "disputed"
            contract.save()

            logger.warning(
                f"Contract disputed id={contract.id} by user={user.username}"
            )

            return Response(
                {
                    "message": "Contract disputed",
                    "contract_id": contract.id,
                    "new_status": contract.status,
                }
            )

        return Response(
            {"error": "Invalid status transition."},
            status=status.HTTP_400_BAD_REQUEST,
        )