from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator


def file_size_validator(value):
    if value.size > 5*1024*1024:
        raise ValidationError('File size should be less than 5MB')


class GuestProfile(models.Model):
    phone_number = models.CharField(
        max_length=13, 
        blank=True, 
        help_text='Phone number should be entered in the format: +989123456789. 13 digits allowed',
        validators=[
            RegexValidator(
                regex=r'^\+98\d{10}$',
                message='Phone number should be entered in the format: +989123456789. 13 digits allowed',
            ),
        ],
        )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True,
        help_text='Say cheese! Maximum file size allowed is 5MB. Allowed formats: jpg, jpeg, png',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            file_size_validator,
        ],
        )
    national_id = models.CharField(
        max_length=10, 
        blank=True,
        help_text='National ID should be entered in the format: 1234567890. 10 digits allowed',
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='National ID should be entered in the format: 1234567890. 10 digits allowed',
            ),
        ],
        )
    address = models.TextField(max_length=500, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='guest_profile')
