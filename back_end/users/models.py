from django.db import models
from django.contrib.auth import get_user_model

# TODO: validators and help_text
class GuestProfile(models.Model):
    phone_number = models.CharField(max_length=13, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    national_id = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='guest_profile')
