# Generated by Django 4.1.1 on 2022-09-26 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("full_name", models.CharField(max_length=50)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("address1", models.CharField(max_length=250)),
                ("address2", models.CharField(max_length=250)),
                ("city", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("country_code", models.CharField(blank=True, max_length=4)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("total_paid", models.DecimalField(decimal_places=2, max_digits=5)),
                ("order_key", models.CharField(max_length=200)),
                ("payment_option", models.CharField(blank=True, max_length=200)),
                ("billing_status", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="catalogue.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
    ]
