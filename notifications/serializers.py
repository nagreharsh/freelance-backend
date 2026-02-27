from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(source="contract.id", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "message",
            "contract",
            "contract_id",
            "is_read",
            "timestamp",
        ]
        read_only_fields = [
            "type",
            "message",
            "contract",
            "timestamp",
        ]