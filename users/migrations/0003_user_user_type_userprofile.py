# Generated by Django 5.1.2 on 2024-11-06 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_awards_remove_user_contacts_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("parent", "Parent"),
                    ("teacher", "Teacher"),
                    ("student", "Student"),
                    ("other", "Other"),
                ],
                default="parent",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=30)),
                ("last_name", models.CharField(blank=True, max_length=30)),
                ("location", models.CharField(max_length=300)),
                ("city", models.CharField(default="Kenya", max_length=200)),
                ("county", models.CharField(default="Kenya", max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
