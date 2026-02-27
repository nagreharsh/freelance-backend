from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    proposal_id = serializers.IntegerField(source="proposal.id", read_only=True)
    client_username = serializers.CharField(source="client.username", read_only=True)
    freelancer_username = serializers.CharField(source="freelancer.username", read_only=True)

    class Meta:
        model = Contract
        fields = [
            "id",
            "proposal_id",
            "client",
            "client_username",
            "freelancer",
            "freelancer_username",
            "status",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = [
            "client",
            "freelancer",
            "created_at",
        ]