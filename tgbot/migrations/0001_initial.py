# Generated by Django 4.2 on 2024-04-14 05:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Admin",
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
                ("UUID", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name": "админа",
                "verbose_name_plural": "ТГ бот - админы",
            },
        ),
        migrations.CreateModel(
            name="News",
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
                ("title", models.CharField(max_length=100)),
                ("text", models.TextField()),
                ("photo", models.ImageField(blank=True, null=True, upload_to="")),
            ],
            options={
                "verbose_name": "новость",
                "verbose_name_plural": "Новости",
            },
        ),
        migrations.CreateModel(
            name="UserBot",
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
                (
                    "user_id",
                    models.BigIntegerField(unique=True, verbose_name="USER ID"),
                ),
                ("username", models.CharField(blank=True, max_length=256, null=True)),
                ("first_name", models.CharField(max_length=256, verbose_name="Name")),
                ("last_name", models.CharField(blank=True, max_length=256, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "тг-юзер",
                "verbose_name_plural": "тг-юзеры",
            },
        ),
    ]