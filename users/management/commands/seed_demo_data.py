from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Profile
from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract
from messaging.models import Message
from reviews.models import Review

import random
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

SKILLS = [
    "Django", "React", "Node.js", "Python",
    "AWS", "Docker", "PostgreSQL", "Vue"
]

PROJECT_TITLES = [
    "Ecommerce Website",
    "REST API Development",
    "Company Portfolio",
    "AI Chatbot",
    "Job Portal",
    "Learning Platform",
    "SaaS Dashboard",
    "Real Estate Website",
    "Mobile App Backend",
    "Marketplace Platform"
]

DURATIONS = [
    "1 week",
    "2 weeks",
    "3 weeks",
    "1 month",
    "2 months"
]


class Command(BaseCommand):
    help = "Seed demo data for freelancing platform"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **options):

        if options["reset"]:
            self.stdout.write("Resetting old data...")

            Review.objects.all().delete()
            Message.objects.all().delete()
            Contract.objects.all().delete()
            Proposal.objects.all().delete()
            Project.objects.all().delete()
            Profile.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()

        password = "Test1234!"

        clients = []
        freelancers = []

        # CREATE CLIENTS
        self.stdout.write("Creating clients...")

        for i in range(10):
            user = User.objects.create_user(
                username=f"client{i}",
                email=f"client{i}@demo.com",
                password=password,
                role="client"
            )

            verified = i < 5

            profile = user.profile
            profile.bio = "Startup founder looking for developers"
            profile.skills = ""
            profile.is_verified = verified
            profile.save()

            clients.append(user)

        # CREATE FREELANCERS
        self.stdout.write("Creating freelancers...")

        for i in range(10):
            user = User.objects.create_user(
                username=f"freelancer{i}",
                email=f"freelancer{i}@demo.com",
                password=password,
                role="freelancer"
            )

            profile = user.profile
            profile.bio = "Full stack developer"
            profile.skills = ", ".join(random.sample(SKILLS, 3))
            profile.portfolio_url = "https://portfolio.example.com"
            profile.hourly_rate = random.randint(20, 80)
            profile.availability = "30 hrs/week"
            profile.is_verified = True
            profile.save()

            freelancers.append(user)

        self.stdout.write(self.style.SUCCESS("Users created"))

        # CREATE PROJECTS
        self.stdout.write("Creating projects...")

        projects = []

        for i in range(15):
            client = random.choice(clients)

            project = Project.objects.create(
                client=client,
                title=random.choice(PROJECT_TITLES),
                description="Looking for an experienced developer.",
                budget=random.randint(500, 5000),
                duration=random.choice(DURATIONS),
                skills_required=", ".join(random.sample(SKILLS, 3)),
                status="open"
            )

            projects.append(project)

        self.stdout.write(self.style.SUCCESS("Projects created"))

        # CREATE PROPOSALS
        self.stdout.write("Creating proposals...")

        proposals = []

        for project in projects:
            bidders = random.sample(freelancers, random.randint(2, 5))

            for freelancer in bidders:
                proposal = Proposal.objects.create(
                    project=project,
                    freelancer=freelancer,
                    bid_amount=random.randint(500, 5000),
                    cover_letter="I have built similar systems before."
                )

                proposals.append(proposal)

        self.stdout.write(self.style.SUCCESS(f"{len(proposals)} proposals created"))

        # CREATE CONTRACTS
        self.stdout.write("Creating contracts...")

        active_contracts = []
        completed_contracts = []

        selected = random.sample(proposals, 13)

        for i, proposal in enumerate(selected):

            contract = Contract.objects.create(
                proposal=proposal,
                client=proposal.project.client,
                freelancer=proposal.freelancer
            )

            start_date = timezone.now() - timedelta(days=random.randint(3, 10))

            if i < 8:
                contract.status = "active"
                contract.started_at = start_date
                active_contracts.append(contract)
            else:
                contract.status = "completed"
                contract.started_at = start_date
                contract.completed_at = start_date + timedelta(days=3)
                completed_contracts.append(contract)

            contract.save()

        self.stdout.write(self.style.SUCCESS("Contracts created"))

        # CREATE MESSAGES
        self.stdout.write("Creating messages...")

        for contract in active_contracts:
            for i in range(random.randint(4, 8)):

                if i % 2 == 0:
                    sender = contract.client
                    receiver = contract.freelancer
                else:
                    sender = contract.freelancer
                    receiver = contract.client

                Message.objects.create(
                    contract=contract,
                    sender=sender,
                    receiver=receiver,
                    content=random.choice([
                        "Hi, let's start working.",
                        "Sharing progress update.",
                        "Please check latest commit.",
                        "Deployment in progress.",
                        "Will deliver soon."
                    ])
                )

        self.stdout.write(self.style.SUCCESS("Messages created"))

        # CREATE REVIEWS
        self.stdout.write("Creating reviews...")

        for contract in completed_contracts[:5]:

            Review.objects.create(
                contract=contract,
                reviewer=contract.client,
                reviewee=contract.freelancer,
                rating=random.randint(4, 5),
                comment="Great freelancer, delivered quality work!"
            )

            Review.objects.create(
                contract=contract,
                reviewer=contract.freelancer,
                reviewee=contract.client,
                rating=random.randint(4, 5),
                comment="Excellent client, clear requirements."
            )

        self.stdout.write(self.style.SUCCESS("Reviews created"))
        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully!"))