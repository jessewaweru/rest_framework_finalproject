# Generated by Django 5.1.2 on 2024-11-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0007_alter_school_facility"),
    ]

    operations = [
        migrations.AddField(
            model_name="school",
            name="views",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
