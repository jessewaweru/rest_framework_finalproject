# Generated by Django 5.1.3 on 2024-11-24 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0014_school_award'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='performance_file',
            field=models.FileField(blank=True, null=True, upload_to='performance_files/'),
        ),
    ]