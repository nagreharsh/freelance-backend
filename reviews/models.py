from django.db import models
from django.conf import settings


class Review(models.Model):
    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_given"
    )

    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews_received"
    )

    rating = models.IntegerField()

    comment = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("contract", "reviewer")

    def __str__(self):
        return f"Review {self.id} - Contract {self.contract.id}"