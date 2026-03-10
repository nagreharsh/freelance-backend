from django.db.models import Count, Sum, Avg
from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract
from reviews.models import Review
from users.models import User, Profile


# -----------------------------
# CLIENT DASHBOARD SERVICE
# -----------------------------
def get_client_dashboard_data(user):

    active_projects = Project.objects.filter(
        client=user
    ).exclude(status="completed").count()

    proposals_received = Proposal.objects.filter(
        project__client=user
    ).count()

    active_contracts = Contract.objects.filter(
        client=user,
        status="active"
    ).count()

    completed_contracts = Contract.objects.filter(
        client=user,
        status="completed"
    ).count()

    total_spent = Contract.objects.filter(
        client=user,
        status="completed"
    ).aggregate(
        total=Sum("proposal__bid_amount")
    )["total"] or 0

    return {
        "active_projects": active_projects,
        "proposals_received": proposals_received,
        "active_contracts": active_contracts,
        "completed_contracts": completed_contracts,
        "total_spent": total_spent,
    }


# -----------------------------
# FREELANCER DASHBOARD SERVICE
# -----------------------------
def get_freelancer_dashboard_data(user):

    applied_proposals = Proposal.objects.filter(
        freelancer=user
    ).count()

    active_contracts = Contract.objects.filter(
        freelancer=user,
        status="active"
    ).count()

    completed_contracts = Contract.objects.filter(
        freelancer=user,
        status="completed"
    ).count()

    total_earned = Contract.objects.filter(
        freelancer=user,
        status="completed"
    ).aggregate(
        total=Sum("proposal__bid_amount")
    )["total"] or 0

    average_rating = Review.objects.filter(
        reviewee=user
    ).aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    return {
        "applied_proposals": applied_proposals,
        "active_contracts": active_contracts,
        "completed_contracts": completed_contracts,
        "total_earned": total_earned,
        "average_rating": round(average_rating, 2) if average_rating else 0,
    }


# -----------------------------
# ADMIN DASHBOARD SERVICE
# -----------------------------
def get_admin_dashboard_data():

    total_users = User.objects.count()
    total_clients = User.objects.filter(role="client").count()
    total_freelancers = User.objects.filter(role="freelancer").count()

    total_projects = Project.objects.count()
    total_contracts = Contract.objects.count()

    active_contracts = Contract.objects.filter(status="active").count()
    completed_contracts = Contract.objects.filter(status="completed").count()

    average_rating = Review.objects.aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    return {
        "total_users": total_users,
        "total_clients": total_clients,
        "total_freelancers": total_freelancers,
        "total_projects": total_projects,
        "total_contracts": total_contracts,
        "active_contracts": active_contracts,
        "completed_contracts": completed_contracts,
        "average_rating": round(average_rating, 2) if average_rating else 0,
    }