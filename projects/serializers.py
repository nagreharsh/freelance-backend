from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    client_username = serializers.ReadOnlyField(source='client.username')

    class Meta:
        model = Project
        fields = ['id', 'client', 'client_username', 'title', 'description', 'budget', 'duration', 'skills_required', 'status', 'created_at', 'updated_at']
        read_only_fields = ['client', 'status', 'created_at', 'updated_at']
