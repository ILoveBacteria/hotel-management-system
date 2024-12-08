# Generated by Django 5.1.3 on 2024-12-08 14:49

import django.core.validators
import django.db.models.deletion
import rooms.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('double_beds', models.PositiveIntegerField()),
                ('single_beds', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('image', models.ImageField(editable=False, upload_to='room_images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), rooms.models.file_size_validator])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_number', models.IntegerField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField()),
                ('status', models.CharField(choices=[('AV', 'Available'), ('OC', 'Occupied'), ('MT', 'Maintenance')], max_length=2)),
                ('last_maintained', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype')),
            ],
        ),
    ]
