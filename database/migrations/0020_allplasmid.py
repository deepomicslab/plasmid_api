# Generated by Django 4.2.1 on 2024-09-15 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0019_alter_antimicrobialresistancegene_source_and_more")
    ]

    operations = [
        migrations.CreateModel(
            name="AllPlasmid",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("plasmid_id", models.CharField(db_index=True, max_length=200)),
                (
                    "source",
                    models.IntegerField(
                        choices=[
                            (0, "PLSDB"),
                            (1, "IMG-PR"),
                            (2, "COMPASS"),
                            (3, "GenBank"),
                            (4, "RefSeq"),
                            (5, "ENA"),
                            (6, "Kraken2"),
                            (7, "DDBJ"),
                            (8, "TPA"),
                            (9, "mMGE"),
                        ],
                        default=0,
                    ),
                ),
                ("topology", models.CharField(blank=True, max_length=200, null=True)),
                ("length", models.IntegerField(blank=True, null=True)),
                ("gc_content", models.FloatField(blank=True, null=True)),
                ("host", models.TextField(blank=True, null=True)),
                (
                    "completeness",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("mob_type", models.TextField(blank=True, null=True)),
                ("mobility", models.TextField(blank=True, null=True)),
                ("cluster", models.CharField(blank=True, max_length=200, null=True)),
                ("subcluster", models.CharField(blank=True, max_length=200, null=True)),
                ("unique_id", models.CharField(blank=True, max_length=200, null=True)),
            ],
        )
    ]
