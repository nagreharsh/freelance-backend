from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(
        source="reviewer.username",
        read_only=True
    )
    reviewee_username = serializers.CharField(
        source="reviewee.username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "contract",
            "reviewer",
            "reviewer_username",
            "reviewee",
            "reviewee_username",
            "rating",
            "comment",
            "timestamp",
        ]
        read_only_fields = [
            "reviewer",
            "reviewee",
            "timestamp",
        ]

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        contract = data.get("contract")

        if contract.status != "completed":
            raise serializers.ValidationError(
                "You can only review a completed contract."
            )

        if user not in [contract.client, contract.freelancer]:
            raise serializers.ValidationError(
                "You are not part of this contract."
            )

        return data

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value