from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project

User = get_user_model()

class ProjectTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(username='client', password='password', role='client')
        self.freelancer_user = User.objects.create_user(username='freelancer', password='password', role='freelancer')
        self.project_data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'budget': 100.00,
            'duration': '1 week',
            'skills_required': 'Python'
        }

    def test_create_project_as_client(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post('/api/projects/', self.project_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().client, self.client_user)

    def test_create_project_as_freelancer(self):
        self.client.force_authenticate(user=self.freelancer_user)
        response = self.client.post('/api/projects/', self.project_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
