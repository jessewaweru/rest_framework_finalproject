# Generated by Django 5.1.3 on 2024-12-02 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_otp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OTP',
        ),
    ]