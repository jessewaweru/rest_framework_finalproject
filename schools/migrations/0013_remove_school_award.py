# Generated by Django 5.1.3 on 2024-11-23 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0012_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='award',
        ),
    ]