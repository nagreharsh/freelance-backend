from django.urls import path
from .views import (
    ClientDashboardView,
    FreelancerDashboardView,
    AdminDashboardView,
    ClientProjectsView,
    ClientProposalsView,
    FreelancerProposalsView,
    FreelancerContractsView,
    AdminVerificationQueueView,
    AdminClientDemandView,
    AdminDisputedContractsView,
    AdminSlowContractsView
)

urlpatterns = [

    # CLIENT
    path("client/", ClientDashboardView.as_view()),
    path("client/projects/", ClientProjectsView.as_view()),
    path("client/proposals/", ClientProposalsView.as_view()),

    # FREELANCER
    path("freelancer/", FreelancerDashboardView.as_view()),
    path("freelancer/proposals/", FreelancerProposalsView.as_view()),
    path("freelancer/contracts/", FreelancerContractsView.as_view()),

    # ADMIN
    path("admin/", AdminDashboardView.as_view()),
    path("admin/verifications/", AdminVerificationQueueView.as_view()),
    path("admin/clients/demand/", AdminClientDemandView.as_view()),
    path("admin/contracts/disputed/", AdminDisputedContractsView.as_view()),
    path("admin/contracts/slow/", AdminSlowContractsView.as_view()),
]