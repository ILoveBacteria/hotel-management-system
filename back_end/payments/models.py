from django.db import models


class Bill(models.Model):
    amount = models.PositiveIntegerField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reserve = models.ForeignKey('reservations.Reserve', on_delete=models.CASCADE)
