# Generated by Django 5.1.2 on 2024-10-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0006_rename_school_status_choice_school_school_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="facility",
            field=models.TextField(blank=True),
        ),
    ]
