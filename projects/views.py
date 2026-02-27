from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project
from .serializers import ProjectSerializer
from users.models import Profile

class IsClientOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'client'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client == request.user

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()  # required by DRF router for basename resolution
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'budget': ['gte', 'lte'],
        'duration': ['exact', 'icontains'],
        'status': ['exact'],
    }
    search_fields = ['title', 'description', 'skills_required']
    ordering_fields = ['created_at', 'budget']

    def get_queryset(self):
        qs = Project.objects.all().order_by('-created_at')

        user = self.request.user

        # Admin sees all projects
        if user.role == "admin":
            return qs

        # Client sees only their own projects
        if user.role == "client":
            return qs.filter(client=user)

        # Freelancer sees only open projects
        if user.role == "freelancer":
            return qs.filter(status="open")

        # ?mine=true → return only current user's own projects (for client dashboard)
        if self.request.query_params.get('mine', '').lower() == 'true':
            return qs.filter(client=user)

        return qs.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'client':
            raise PermissionDenied("Only clients can post projects.")
        serializer.save(client=self.request.user)
        # Update client stats
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        profile.projects_posted_count += 1
        profile.save()