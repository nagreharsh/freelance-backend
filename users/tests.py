from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile

User = get_user_model()

class AdminTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='password', role='admin')
        self.normal_user = User.objects.create_user(username='user', password='password', role='freelancer')
        self.profile = Profile.objects.create(user=self.normal_user, bio='Bio', skills='Skills')

    def test_admin_can_list_unverified_users(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/admin/unverified/') # Correct URL path
        # I added path('admin/unverified/', ...) in users/urls.py
        # And main urls has path('api/', include('users.urls')) -> so /api/admin/unverified/
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should see normal_user because default verification is False
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user')

    def test_admin_can_verify_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/admin/verify/{self.normal_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_verified)

    def test_normal_user_cannot_access_admin(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get('/api/admin/unverified/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
