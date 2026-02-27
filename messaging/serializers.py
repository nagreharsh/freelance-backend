from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    receiver_username = serializers.CharField(source="receiver.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "contract",
            "sender",
            "sender_username",
            "receiver",
            "receiver_username",
            "content",
            "is_read",
            "timestamp",
        ]
        read_only_fields = [
            "sender",
            "receiver",
            "is_read",
            "timestamp",
        ]