from rest_framework.test import APITestCase
from users.models import User
from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract
from reviews.models import Review


class IntegrationFlowTest(APITestCase):

    def setUp(self):

        self.client_user = User.objects.create_user(
            username="client_flow",
            password="test123",
            role="client"
        )

        self.freelancer = User.objects.create_user(
            username="freelancer_flow",
            password="test123",
            role="freelancer"
        )

    def test_full_platform_flow(self):

        # Client login
        self.client.login(username="client_flow", password="test123")

        # Client creates project
        project = Project.objects.create(
            client=self.client_user,
            title="Integration Project",
            description="Testing full flow",
            budget=1500,
            duration="3 weeks",
            skills_required="Django"
        )

        self.assertIsNotNone(project.id)

        # Freelancer submits proposal
        proposal = Proposal.objects.create(
            project=project,
            freelancer=self.freelancer,
            bid_amount=1400,
            cover_letter="Experienced developer"
        )

        self.assertEqual(proposal.project, project)

        # Contract created
        contract = Contract.objects.create(
            proposal=proposal,
            client=self.client_user,
            freelancer=self.freelancer,
            status="active"
        )

        self.assertEqual(contract.status, "active")

        # Contract completed
        contract.status = "completed"
        contract.save()

        self.assertEqual(contract.status, "completed")

        # Client submits review
        review = Review.objects.create(
            contract=contract,
            reviewer=self.client_user,
            reviewee=self.freelancer,
            rating=5,
            comment="Excellent work"
        )

        self.assertEqual(review.rating, 5)