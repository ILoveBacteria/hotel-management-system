# Generated by Django 5.1.3 on 2024-12-10 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='due_date',
        ),
    ]