# Generated by Django 4.2.1 on 2024-06-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0013_alter_protein_cog_category_alter_protein_cog_id_and_more")
    ]

    operations = [
        migrations.AlterField(
            model_name="protein",
            name="cog_category",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="cog_id",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="ec_number",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="function_source",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="orf_source",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="plasmid_id",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="product",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="protein",
            name="protein_id",
            field=models.CharField(max_length=1000),
        ),
    ]