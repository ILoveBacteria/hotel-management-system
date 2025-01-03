# Generated by Django 5.1.3 on 2024-11-27 18:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestprofile',
            name='address',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='', upload_to='avatars/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='national_id',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=13),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guestprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='guest_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
