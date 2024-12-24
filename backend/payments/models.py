from django.db import models
from django.db.models import Q, F, CheckConstraint

from reservations.models import Reserve


class Bill(models.Model):
    amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    due_date = models.DateTimeField()
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reserve = models.OneToOneField(Reserve, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            CheckConstraint(condition=Q(due_date__gte=F('created_at')), name='due_date_after_created_at'),
            CheckConstraint(condition=(Q(is_paid=False) & Q(payment_date__isnull=True)) | (Q(is_paid=True) & Q(payment_date__isnull=False)), name='is_paid_xor_payment_date'),
            # TODO: CheckConstraint(condition=Q(due_date__lte=F('reservation__check_in')), name='due_date_before_check_in'),
        ]
    
    def __str__(self):
        return f'{self.amount} - {self.is_paid}'
