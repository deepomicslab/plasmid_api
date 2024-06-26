# Generated by Django 4.2.1 on 2024-06-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0009_antimicrobialresistancegene_source_crispr_source_and_more")
    ]

    operations = [
        migrations.AddField(
            model_name="transmembranehelices",
            name="datasource",
            field=models.IntegerField(
                choices=[
                    (0, "PLSDB"),
                    (1, "IMG-PR"),
                    (2, "COMPASS"),
                    (3, "GenBank"),
                    (4, "RefSeq"),
                    (5, "EMBL"),
                    (6, "Kraken2"),
                    (7, "DDBJ"),
                    (8, "TPA"),
                ],
                default=0,
            ),
        )
    ]
