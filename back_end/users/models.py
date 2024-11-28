from django.db import models
from django.contrib.auth import get_user_model

# TODO: validators and help_text
class GuestProfile(models.Model):
    phone_number = models.CharField(
        max_length=13, 
        blank=True, 
        help_text='Phone number should be entered in the format: +989123456789. 13 digits allowed',
        )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True,
        help_text='Say cheese! Upload your avatar here',
        )
    national_id = models.CharField(
        max_length=10, 
        blank=True,
        help_text='National ID should be entered in the format: 1234567890. 10 digits allowed',
        )
    address = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='guest_profile')
