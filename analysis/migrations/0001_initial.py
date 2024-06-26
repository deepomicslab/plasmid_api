# Generated by Django 4.2.1 on 2024-06-21 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("name", models.CharField(blank=True, max_length=300, null=True)),
                ("user", models.CharField(blank=True, max_length=300, null=True)),
                ("uploadpath", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "analysis_type",
                    models.CharField(blank=True, max_length=60, null=True),
                ),
                ("modulelist", models.CharField(blank=True, max_length=400, null=True)),
                ("status", models.CharField(blank=True, max_length=60, null=True)),
                ("task_log", models.TextField(blank=True, null=True)),
                ("task_detail", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        )
    ]
