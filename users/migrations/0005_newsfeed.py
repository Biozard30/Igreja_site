# Generated by Django 5.0.10 on 2024-12-22 14:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_userprofile_email_alter_userprofile_address_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsFeed",
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
                ("content", models.TextField(max_length=1000, verbose_name="Conteúdo")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="feed_images/",
                        verbose_name="Imagem",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de criação"
                    ),
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
                "verbose_name": "Notícia",
                "verbose_name_plural": "Notícias",
                "ordering": ["-created_at"],
            },
        ),
    ]