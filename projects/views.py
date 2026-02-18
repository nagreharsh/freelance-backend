from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Project
from .serializers import ProjectSerializer

from .models import Proposal
from .serializers import ProposalSerializer

from rest_framework.response import Response
from .models import Project, Proposal

#Project API (Client only)
class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "client":
            raise PermissionDenied("Only clients can create projects")

        serializer.save(client=self.request.user)

        # Increment projects_posted counter
        self.request.user.projects_posted += 1
        self.request.user.save()

#Project List API
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()

        skill = self.request.query_params.get("skill")
        min_budget = self.request.query_params.get("min_budget")
        max_budget = self.request.query_params.get("max_budget")
        duration = self.request.query_params.get("duration")

        if skill:
            queryset = queryset.filter(skills__icontains=skill)

        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)

        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)

        if duration:
            queryset = queryset.filter(duration__icontains=duration)

        return queryset

#Project Detail API
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

#Update + Delete API
class ProjectUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.client:
            raise PermissionDenied("Not your project")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.client:
            raise PermissionDenied("Not your project")
        instance.delete()

#Submit Proposal (Freelancer only)
class ProposalCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "freelancer":
            raise PermissionDenied("Only freelancers can submit proposals")

        proposal = serializer.save(freelancer=self.request.user)

        # Increment proposals_received counter for project owner
        client = proposal.project.client
        client.proposals_received += 1
        client.save()

#List proposals
class ProjectProposalListView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs["project_id"]
        project = Project.objects.get(id=project_id)

        # Only project owner can view proposals
        if project.client != self.request.user:
            raise PermissionDenied("You cannot view proposals for this project")

        return Proposal.objects.filter(project=project)

#Update proposal status
class ProposalUpdateView(generics.UpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        proposal = self.get_object()

        if proposal.project.client != request.user:
            return Response(
                {"error": "Only the project owner can update proposal status"},
                status=403
            )

        serializer = self.get_serializer(
            proposal,
            data=request.data,
            partial=True   # ← THIS FIXES IT
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)