# Generated by Django 5.1.3 on 2024-11-25 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0015_school_performance_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='performance_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
