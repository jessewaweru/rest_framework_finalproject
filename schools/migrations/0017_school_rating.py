# Generated by Django 5.1.3 on 2024-11-30 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0016_school_performance_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]