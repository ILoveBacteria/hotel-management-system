from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator


def file_size_validator(value):
    if value.size > 1*1024*1024:
        raise ValidationError('File size should be less than 1MB')
    

class Room(models.Model):
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'
    MAINTENANCE = 'maintenance'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (OCCUPIED, 'Occupied'),
        (MAINTENANCE, 'Maintenance'),
    ]
    
    room_number = models.IntegerField(primary_key=True)
    is_active = models.BooleanField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)
    last_maintained = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, related_name='rooms')
    
    def __str__(self):
        return self.room_number
    

class RoomType(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    double_beds = models.PositiveIntegerField()
    single_beds = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class RoomImage(models.Model):
    caption = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='room_images/', 
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            file_size_validator,
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, related_name='images')
    
    def __str__(self):
        return self.caption
    
