from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateDeleteView,

    ProposalCreateView,
    ProjectProposalListView,
    ProposalUpdateView,
)

urlpatterns = [
    path("create/", ProjectCreateView.as_view()),
    path("", ProjectListView.as_view()),
    path("<int:pk>/", ProjectDetailView.as_view()),
    path("<int:pk>/edit/", ProjectUpdateDeleteView.as_view()),
    path("proposals/create/", ProposalCreateView.as_view()),
    path("<int:project_id>/proposals/", ProjectProposalListView.as_view()),
    path("proposals/<int:pk>/update/", ProposalUpdateView.as_view()),
]