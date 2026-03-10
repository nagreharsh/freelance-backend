from django.test import TestCase
from users.models import User
from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract
from messaging.models import Message
from reviews.models import Review


class ModelTests(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client_test",
            password="test123",
            role="client"
        )

        self.freelancer = User.objects.create_user(
            username="freelancer_test",
            password="test123",
            role="freelancer"
        )

        self.project = Project.objects.create(
            client=self.client_user,
            title="Test Project",
            description="Test description",
            budget=1000,
            duration="2 weeks",
            skills_required="Python"
        )

        self.proposal = Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer,
            bid_amount=900,
            cover_letter="I can complete this"
        )

        self.contract = Contract.objects.create(
            proposal=self.proposal,
            client=self.client_user,
            freelancer=self.freelancer,
            status="active"
        )

    def test_user_creation(self):
        self.assertEqual(self.client_user.role, "client")

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Test Project")

    def test_proposal_creation(self):
        self.assertEqual(self.proposal.project, self.project)

    def test_contract_creation(self):
        self.assertEqual(self.contract.client, self.client_user)

    def test_message_creation(self):
        message = Message.objects.create(
            contract=self.contract,
            sender=self.client_user,
            receiver=self.freelancer,
            content="Hello"
        )
        self.assertEqual(message.content, "Hello")

    def test_review_creation(self):
        review = Review.objects.create(
            contract=self.contract,
            reviewer=self.client_user,
            reviewee=self.freelancer,
            rating=5,
            comment="Great work"
        )
        self.assertEqual(review.rating, 5)