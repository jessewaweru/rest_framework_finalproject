# Generated by Django 5.1.2 on 2024-10-28 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="awards",
        ),
        migrations.RemoveField(
            model_name="user",
            name="contacts",
        ),
        migrations.RemoveField(
            model_name="user",
            name="description",
        ),
        migrations.RemoveField(
            model_name="user",
            name="image",
        ),
        migrations.RemoveField(
            model_name="user",
            name="location",
        ),
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="website",
        ),
    ]
