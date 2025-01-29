from django.utils import timezone
from django.db import models, transaction
from django.db.models import Q, F, CheckConstraint

from reservations.models import Reserve


class OverdueManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        for i in queryset.filter(due_date__lt=timezone.now(), status=Bill.WAITING):
            i.overdue()
        return queryset


class Bill(models.Model):
    WAITING = 'waiting'
    PAID = 'paid'
    OVERDUE = 'overdue'
    
    status_choices = [
        (WAITING, 'Waiting'),
        (PAID, 'Paid'),
        (OVERDUE, 'Overdue'),
    ]
    
    objects = OverdueManager()
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=status_choices, default=WAITING)
    due_date = models.DateTimeField()
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reserve = models.OneToOneField(Reserve, on_delete=models.CASCADE, related_name='bill')
    
    class Meta:
        constraints = [
            CheckConstraint(condition=Q(due_date__gte=F('created_at')), name='due_date_after_created_at'),
            CheckConstraint(condition=((Q(status='waiting') | Q(status='overdue')) & Q(payment_date__isnull=True)) | (Q(status='paid') & Q(payment_date__isnull=False)), name='is_paid_xor_payment_date'),
        ]
        
    @transaction.atomic
    def overdue(self):
        self.status = self.OVERDUE
        self.save()
        if self.reserve.status == Reserve.REGISTERED:
            self.reserve.status = Reserve.CANCELED
            self.reserve.save()
        
    
    def __str__(self):
        return f'{self.amount} - {self.is_paid}'


class CreditCard(models.Model):
    number = models.CharField(max_length=19)
    cvv2 = models.CharField(max_length=4)
    expire_month = models.CharField(max_length=2)
    expire_year = models.CharField(max_length=2)
    password = models.CharField(max_length=255)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='credit_card')
    
    def __str__(self):
        return f'{self.number}'
