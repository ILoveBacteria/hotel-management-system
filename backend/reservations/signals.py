from django.db.models.signals import post_save
from django.dispatch import receiver
from reservations.models import Reserve
from payments.models import Bill


@receiver(post_save, sender=Reserve)
def update_bill_status(sender, instance, **kwargs):
    if instance.status == Reserve.CANCELED and instance.bill.status == Bill.WAITING:
        instance.bill.status = Bill.OVERDUE
        instance.bill.save()
        