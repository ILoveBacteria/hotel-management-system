# Generated by Django 5.1.3 on 2024-12-09 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0003_alter_room_room_type_alter_roomimage_room_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('status', models.CharField(choices=[('RE', 'Registered'), ('CA', 'Canceled'), ('PA', 'Paid'), ('CI', 'Check-in'), ('CO', 'Check-out')], default='RE', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserves', to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CancelledReserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reserve', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cancelled_reserve', to='reservations.reserve')),
            ],
        ),
    ]
