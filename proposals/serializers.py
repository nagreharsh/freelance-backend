import bleach
from rest_framework import serializers
from .models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    freelancer_username = serializers.ReadOnlyField(source='freelancer.username')
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Proposal
        fields = ['id', 'project', 'project_title', 'freelancer', 'freelancer_username', 'cover_letter', 'bid_amount', 'status', 'created_at']
        read_only_fields = ['freelancer', 'status', 'created_at']

    def validate_cover_letter(self, value):
        return bleach.clean(value)