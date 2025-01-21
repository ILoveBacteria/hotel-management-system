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
        
    def pay(self):
        if self.status == self.PAID:
            return
        if self.status == self.OVERDUE or self.due_date < timezone.now():
            self.status = self.OVERDUE
            raise ValueError('Cannot pay overdue bill')
        self.is_paid = True
        self.payment_date = timezone.now()
        self.save()
        
    @transaction.atomic
    def overdue(self):
        self.status = self.OVERDUE
        self.save()
        if self.reserve.status == Reserve.REGISTERED:
            self.reserve.status = Reserve.CANCELED
            self.reserve.save()
        
    
    def __str__(self):
        return f'{self.amount} - {self.is_paid}'
