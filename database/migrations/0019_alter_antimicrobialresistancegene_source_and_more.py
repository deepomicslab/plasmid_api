# Generated by Django 4.2.1 on 2024-09-10 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("database", "0018_plasmid_unique_id_and_more")]

    operations = [
        migrations.AlterField(
            model_name="antimicrobialresistancegene",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="crispr",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="host",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="plasmid",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="protein",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="secondarymetabolism",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="signalpeptides",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="transmembranehelices",
            name="datasource",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="trna",
            name="source",
            field=models.IntegerField(
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
        migrations.AlterField(
            model_name="virulentfactor",
            name="source",
            field=models.IntegerField(
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
    ]