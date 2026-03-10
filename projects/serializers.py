import bleach
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    client_username = serializers.ReadOnlyField(source='client.username')

    class Meta:
        model = Project
        fields = ['id', 'client', 'client_username', 'title', 'description', 'budget', 'duration', 'skills_required', 'status', 'created_at', 'updated_at']
        read_only_fields = ['client', 'status', 'created_at', 'updated_at']

    def validate_budget(self, value):
        if value < 1000 or value > 500000:
            raise serializers.ValidationError(
                "Budget must be between ₹1000 and ₹500000"
            )
        return value

    def validate_skills_required(self, value):
        value = bleach.clean(value)   # sanitize input

        skills = [s.strip() for s in value.split(",") if s.strip()]
        if len(skills) > 10:
            raise serializers.ValidationError(
                "Maximum 10 skills allowed."
            )
        return value
    
    def validate_description(self, value):
        return bleach.clean(value)