# Generated by Django 5.0.10 on 2024-12-22 14:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_newsfeed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ministerio",
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
                ("title", models.CharField(max_length=200, verbose_name="Título")),
                (
                    "content",
                    models.TextField(max_length=1000, verbose_name="Descrição"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de criação"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(default=True, verbose_name="É público?"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Autor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ministério",
                "verbose_name_plural": "Ministérios",
                "ordering": ["-created_at"],
            },
        ),
    ]