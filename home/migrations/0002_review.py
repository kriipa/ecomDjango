# Generated by Django 4.2.2 on 2023-06-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
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
                ("customer_name", models.CharField(max_length=500)),
                ("image", models.ImageField(upload_to="media")),
                ("job", models.CharField(max_length=500)),
                ("comment", models.TextField()),
                ("rank", models.IntegerField()),
            ],
        ),
    ]
