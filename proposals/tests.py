from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from projects.models import Project
from .models import Proposal

User = get_user_model()

class ProposalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(username='client', password='password', role='client')
        self.freelancer_user = User.objects.create_user(username='freelancer', password='password', role='freelancer')
        self.project = Project.objects.create(
            client=self.client_user,
            title='Test Project',
            description='Test Description',
            budget=100.00,
            duration='1 week',
            skills_required='Python'
        )
        self.proposal_data = {
            'project': self.project.id,
            'cover_letter': 'I can do this',
            'bid_amount': 90.00
        }

    def test_create_proposal_as_freelancer(self):
        self.client.force_authenticate(user=self.freelancer_user)
        response = self.client.post('/api/proposals/', self.proposal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proposal.objects.count(), 1)
        
        # Verify stats update
        self.client_user.refresh_from_db()
        # Note: Stats are on Profile, need to ensure profile exists
        # In this test setup, profile might not be created automatically unless signal exists
        # But our view creates it if missing?
        # Let's check if views.py logic handles it. Yes, perform_create calls get_or_create logic on Profile.
        
        # But wait, perform_create for Project created it for project_client.
        # perform_create for Proposal created it for project_client (receiver).
        
        # We need to manually create profiles for users in setUp?
        # Actually, let's see if the view logic works.
        
        from users.models import Profile
        profile = Profile.objects.get(user=self.client_user)
        self.assertEqual(profile.proposals_received_count, 1)

    def test_client_can_accept_proposal(self):
        proposal = Proposal.objects.create(
            project=self.project,
            freelancer=self.freelancer_user,
            cover_letter='Hire me',
            bid_amount=100
        )
        
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(f'/api/proposals/{proposal.id}/accept/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        proposal.refresh_from_db()
        self.assertEqual(proposal.status, 'accepted')
