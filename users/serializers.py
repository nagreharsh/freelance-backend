from rest_framework import serializers
from .models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'skills', 'portfolio_url', 'hourly_rate', 'availability', 'projects_posted_count', 'proposals_received_count', 'is_verified']
        read_only_fields = ['projects_posted_count', 'proposals_received_count', 'is_verified']