from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from projects.models import Project
from proposals.models import Proposal
from contracts.models import Contract


class APIPermissionValidationTests(APITestCase):

    def setUp(self):

        self.client_user = User.objects.create_user(
            username="client_perm",
            password="test123",
            role="client"
        )

        self.freelancer = User.objects.create_user(
            username="freelancer_perm",
            password="test123",
            role="freelancer"
        )

        self.admin = User.objects.create_user(
            username="admin_perm",
            password="test123",
            role="admin",
            is_staff=True
        )

        self.project = Project.objects.create(
            client=self.client_user,
            title="Permission Test Project",
            description="Testing permissions",
            budget=1000,
            duration="2 weeks",
            skills_required="Python"
        )

        self.proposal = Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer,
            bid_amount=900,
            cover_letter="I can do this"
        )

        self.contract = Contract.objects.create(
            proposal=self.proposal,
            client=self.client_user,
            freelancer=self.freelancer,
            status="completed"
        )


    def test_non_admin_cannot_access_admin_contracts(self):

        self.client.force_authenticate(user=self.client_user)

        response = self.client.get("/api/admin/contracts/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_invalid_review_rating(self):

        self.client.force_authenticate(user=self.client_user)

        response = self.client.post(
            "/api/reviews/",
            {
                "contract": self.contract.id,
                "rating": 10,
                "comment": "Invalid rating test"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)