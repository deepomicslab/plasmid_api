# Generated by Django 4.2.1 on 2024-06-26 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("database", "0007_alter_plasmid_source")]

    operations = [
        migrations.RemoveField(
            model_name="antimicrobialresistancegene", name="plasmid"
        ),
        migrations.RemoveField(model_name="crispr", name="plasmid"),
        migrations.RemoveField(model_name="host", name="plasmid"),
        migrations.RemoveField(model_name="protein", name="plasmid"),
        migrations.RemoveField(model_name="secondarymetabolism", name="plasmid"),
        migrations.RemoveField(model_name="signalpeptides", name="plasmid"),
        migrations.RemoveField(model_name="transmembranehelices", name="plasmid"),
        migrations.RemoveField(model_name="trna", name="plasmid"),
        migrations.RemoveField(model_name="virulentfactor", name="plasmid"),
        migrations.AddField(
            model_name="antimicrobialresistancegene",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="crispr",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="host",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="protein",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="secondarymetabolism",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="signalpeptides",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="transmembranehelices",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="trna",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="virulentfactor",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
