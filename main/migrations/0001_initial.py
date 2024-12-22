# Generated by Django 5.1.3 on 2024-11-29 00:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Culto",
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
                ("tipo", models.CharField(max_length=100)),
                ("descricao", models.TextField()),
                ("horario", models.TimeField()),
                ("data", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Evento",
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
                ("titulo", models.CharField(max_length=100)),
                ("data", models.DateField()),
                ("texto", models.TextField()),
                ("foto", models.ImageField(upload_to="eventos/")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Noticia",
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
                ("tema", models.CharField(max_length=100)),
                ("local", models.CharField(max_length=100)),
                ("foto", models.ImageField(upload_to="noticias/")),
                ("data", models.DateField()),
                ("hora", models.TimeField()),
                ("texto", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="PedidoOracao",
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
                ("nome", models.CharField(max_length=100)),
                ("telefone", models.CharField(max_length=15)),
                ("texto", models.TextField()),
                ("data", models.DateField(auto_now_add=True)),
            ],
        ),
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
                ("nome", models.CharField(max_length=100)),
                ("foto", models.ImageField(upload_to="ministerios/")),
                ("descricao", models.TextField()),
                (
                    "membros",
                    models.ManyToManyField(
                        related_name="ministerio_membros", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Igreja",
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
                ("nome", models.CharField(max_length=100)),
                ("rua", models.CharField(max_length=100)),
                ("numero", models.CharField(max_length=10)),
                ("bairro", models.CharField(max_length=100)),
                ("cidade", models.CharField(max_length=100)),
                ("cep", models.CharField(max_length=20)),
                ("estado", models.CharField(max_length=50)),
                ("pais", models.CharField(max_length=50)),
                ("cultos", models.ManyToManyField(blank=True, to="main.culto")),
                ("eventos", models.ManyToManyField(blank=True, to="main.evento")),
                (
                    "lideres",
                    models.ManyToManyField(
                        related_name="lideres", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "membros",
                    models.ManyToManyField(
                        related_name="membros", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "pastor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pastor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("ministerios", models.ManyToManyField(to="main.ministerio")),
                ("noticias", models.ManyToManyField(blank=True, to="main.noticia")),
                (
                    "pedidos_oracao",
                    models.ManyToManyField(blank=True, to="main.pedidooracao"),
                ),
            ],
        ),
    ]
