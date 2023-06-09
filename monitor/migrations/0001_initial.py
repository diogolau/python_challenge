# Generated by Django 4.2 on 2023-04-15 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
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
                ("ticker", models.CharField(max_length=10, unique=True)),
                ("sell_value", models.FloatField()),
                ("buy_value", models.FloatField()),
                ("time_period", models.PositiveIntegerField()),
                ("tracked", models.BooleanField(default=True)),
            ],
        ),
    ]
