import logging

logger = logging.getLogger(__name__)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db import transaction
from .models import Proposal
from .serializers import ProposalSerializer
from users.models import Profile
from contracts.models import Contract


class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "client":
            return Proposal.objects.filter(project__client=user)

        elif user.role == "freelancer":
            return Proposal.objects.filter(freelancer=user)

        return Proposal.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != "freelancer":
            raise PermissionDenied("Only freelancers can submit proposals.")

        profile = Profile.objects.get(user=self.request.user)
        if not profile.is_verified:
            raise PermissionDenied("Only verified freelancers can submit proposals.")

        project = serializer.validated_data["project"]

        if project.status != "open":
            raise PermissionDenied(
                "Cannot submit proposal to a non-open project."
            )
        
        if Proposal.objects.filter(project=project, freelancer=self.request.user).exists():
            raise PermissionDenied("You have already submitted a proposal for this project.")

        serializer.save(freelancer=self.request.user)

        logger.info(
            f"Proposal submitted by freelancer={self.request.user.username} "
            f"for project={project.title}"
        )

        # Update client stats (client receiving the proposal)
        client_profile, _ = Profile.objects.get_or_create(
            user=project.client
        )
        client_profile.proposals_received_count += 1
        client_profile.save()

    @action(detail=True, methods=["post"], url_path="accept")
    def accept_proposal(self, request, pk=None):
        with transaction.atomic():
            proposal = Proposal.objects.select_for_update().get(pk=pk)

            if request.user != proposal.project.client:
                return Response(
                    {"error": "You are not the client of this project"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            client_profile = Profile.objects.get(user=request.user)
            if not client_profile.is_verified:
                return Response(
                    {"error": "Only verified clients can accept proposals"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Prevent accepting twice
            if proposal.status == "accepted":
                return Response(
                    {"error": "Proposal already accepted"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prevent accepting rejected proposal
            if proposal.status == "rejected":
                return Response(
                    {"error": "Cannot accept a rejected proposal"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prevent accepting if project already in progress
            if proposal.project.status != "open":
                return Response(
                    {"error": "Project is not open for acceptance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            proposal.status = "accepted"
            proposal.save()

            logger.info(
                f"Proposal id={proposal.id} accepted by client={request.user.username} "
                f"for project={proposal.project.title}"
            )

            # Create contract safely (avoid duplicates)
            contract, created = Contract.objects.get_or_create(
                proposal=proposal,
                defaults={
                    "client": proposal.project.client,
                    "freelancer": proposal.freelancer,
                    "status": "draft",
                },
            )

            if created:
                logger.info(
                    f"Contract created id={contract.id} "
                    f"client={contract.client.username} "
                    f"freelancer={contract.freelancer.username}"
                )

            # Ideally, close the project or mark it as in progress?
            project = proposal.project
            project.status = "in_progress"
            project.save()

        return Response(
            {
                "message": "Proposal accepted",
                "contract_id": contract.id,
                "contract_status": contract.status,
            }
        )

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_proposal(self, request, pk=None):
        proposal = self.get_object()

        if request.user != proposal.project.client:
            return Response(
                {"error": "You are not the client of this project"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Prevent rejecting accepted proposal
        if proposal.status == "accepted":
            return Response(
                {"error": "Cannot reject an already accepted proposal"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        proposal.status = "rejected"
        proposal.save()

        logger.info(
            f"Proposal id={proposal.id} rejected by client={request.user.username}"
        )

        return Response({"status": "Proposal rejected"})