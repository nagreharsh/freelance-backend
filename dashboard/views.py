from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Count, Max, Q

from common.permissions import IsAdminRole
from users.models import Profile, User

from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract

from projects.serializers import ProjectSerializer
from proposals.serializers import ProposalSerializer
from contracts.serializers import ContractSerializer

from .services import (
    get_client_dashboard_data,
    get_freelancer_dashboard_data,
    get_admin_dashboard_data
)

class ClientDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "client":
            return Response(
                {"detail": "Only clients can access this dashboard."},
                status=403
            )

        data = get_client_dashboard_data(request.user)
        return Response(data)


class FreelancerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "freelancer":
            return Response(
                {"detail": "Only freelancers can access this dashboard."},
                status=403
            )

        data = get_freelancer_dashboard_data(request.user)
        return Response(data)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        data = get_admin_dashboard_data()
        return Response(data)
    

# -----------------------------
# CLIENT PROJECTS LIST
# -----------------------------
class ClientProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "client":
            return Response(
                {"detail": "Only clients can access this endpoint."},
                status=403
            )

        projects = Project.objects.filter(
            client=request.user
        ).exclude(status="completed").order_by("-id")

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)


# -----------------------------
# CLIENT PROPOSALS RECEIVED
# -----------------------------
class ClientProposalsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "client":
            return Response(
                {"detail": "Only clients can access this endpoint."},
                status=403
            )

        proposals = Proposal.objects.filter(
            project__client=request.user
        ).select_related("freelancer", "project").order_by("-id")

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(proposals, request)

        serializer = ProposalSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    
# -----------------------------
# FREELANCER PROPOSALS
# -----------------------------
class FreelancerProposalsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "freelancer":
            return Response(
                {"detail": "Only freelancers can access this endpoint."},
                status=403
            )

        proposals = Proposal.objects.filter(
            freelancer=request.user
        ).select_related("project").order_by("-id")

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(proposals, request)

        serializer = ProposalSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)


# -----------------------------
# FREELANCER ACTIVE CONTRACTS
# -----------------------------
class FreelancerContractsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "freelancer":
            return Response(
                {"detail": "Only freelancers can access this endpoint."},
                status=403
            )

        contracts = Contract.objects.filter(
            freelancer=request.user,
            status="active"
        ).select_related("proposal").order_by("-id")

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(contracts, request)

        serializer = ContractSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)
    
# -----------------------------
# ADMIN VERIFICATION QUEUE
# -----------------------------
class AdminVerificationQueueView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):

        pending_profiles = Profile.objects.filter(
            is_verified=False,
            user__role__in=["client", "freelancer"]
            ).select_related("user")

        data = [
            {
                "user_id": p.user.id,
                "username": p.user.username,
                "email": p.user.email,
                "role": p.user.role,
                "skills": p.skills,
                "hourly_rate": p.hourly_rate,
            }
            for p in pending_profiles
        ]

        return Response(data)
    
# -----------------------------
# CLIENT DEMAND RANKING
# -----------------------------
class AdminClientDemandView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):

        thirty_days_ago = timezone.now() - timedelta(days=30)

        clients = (
            User.objects.filter(role="client")
            .annotate(
                proposals_last_30_days=Count(
                    "posted_projects__proposals",
                    filter=Q(
                        posted_projects__proposals__created_at__gte=thirty_days_ago
                    ),
                    distinct=True
                ),
                active_projects=Count(
                    "posted_projects",
                    filter=Q(posted_projects__status="open"),
                    distinct=True
                ),
                last_project_date=Max("posted_projects__created_at")
            )
        )

        high_demand = []
        low_demand = []

        for c in clients:

            if c.proposals_last_30_days >= 5 or c.active_projects >= 3:
                high_demand.append({
                    "client_id": c.id,
                    "username": c.username,
                    "proposals_last_30_days": c.proposals_last_30_days,
                    "active_projects": c.active_projects
                })

            elif (
                c.proposals_last_30_days <= 2
                or (c.last_project_date and c.last_project_date < thirty_days_ago)
            ):
                low_demand.append({
                    "client_id": c.id,
                    "username": c.username,
                    "proposals_last_30_days": c.proposals_last_30_days,
                    "active_projects": c.active_projects
                })

        return Response({
            "high_demand_clients": high_demand,
            "low_demand_clients": low_demand
        })
    
# -----------------------------
# DISPUTED CONTRACTS
# -----------------------------
class AdminDisputedContractsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):

        contracts = Contract.objects.filter(
            status="disputed"
        ).select_related("client", "freelancer", "proposal")

        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)
    
# -----------------------------
# SLOW CONTRACTS
# -----------------------------
class AdminSlowContractsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):

        threshold = date.today() - timedelta(days=30)

        slow_contracts = Contract.objects.filter(
            status="active",
            start_date__lt=threshold
        ).select_related("client", "freelancer", "proposal")

        serializer = ContractSerializer(slow_contracts, many=True)
        return Response(serializer.data)