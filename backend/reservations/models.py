from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, CheckConstraint, F


class Reserve(models.Model):
    REGISTERED = 'registered'
    CANCELED = 'canceled'
    PAID = 'paid'
    CHECK_IN = 'check-in'
    CHECK_OUT = 'check-out'
    STATUS_CHOICES = [
        (REGISTERED, 'Registered'),
        (CANCELED, 'Canceled'),
        (PAID, 'Paid'),
        (CHECK_IN, 'Check-in'),
        (CHECK_OUT, 'Check-out'),
    ]
    
    price = models.PositiveIntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=REGISTERED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reserves')
    room = models.ForeignKey('rooms.Room', on_delete=models.PROTECT, related_name='reserves')
    
    class Meta:
        constraints = [
            CheckConstraint(condition=Q(check_in__lt=F('check_out')), name='check_in_before_check_out'),
        ]
    
    def __str__(self):
        return f'{self.id} - {self.status}'


class CancelledReserve(models.Model):
    reserve = models.OneToOneField(Reserve, on_delete=models.CASCADE, related_name='cancelled_reserve')
    penalty = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
