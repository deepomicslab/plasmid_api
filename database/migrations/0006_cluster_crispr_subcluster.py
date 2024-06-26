# Generated by Django 3.2.12 on 2024-06-07 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20240515_0104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_id', models.CharField(max_length=200)),
                ('avg_gc', models.FloatField(blank=True, null=True)),
                ('avg_length', models.FloatField(blank=True, null=True)),
                ('no_of_subclusters', models.IntegerField(blank=True, max_length=200, null=True)),
                ('no_of_members', models.IntegerField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcluster_id', models.CharField(max_length=200)),
                ('avg_gc', models.FloatField(blank=True, null=True)),
                ('avg_length', models.FloatField(blank=True, null=True)),
                ('no_of_members', models.IntegerField(blank=True, max_length=200, null=True)),
                ('members', models.TextField(blank=True, null=True)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subclusters', to='database.cluster')),
            ],
        ),
        migrations.CreateModel(
            name='Crispr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cas_id', models.CharField(max_length=200)),
                ('cas_start', models.IntegerField(blank=True, null=True)),
                ('cas_end', models.IntegerField(blank=True, null=True)),
                ('cas_subtype', models.CharField(blank=True, max_length=200, null=True)),
                ('crispr_id', models.CharField(max_length=200)),
                ('start', models.IntegerField(blank=True, null=True)),
                ('end', models.IntegerField(blank=True, null=True)),
                ('crispr_subtype', models.CharField(blank=True, max_length=200, null=True)),
                ('cas_consenus_prediction', models.CharField(blank=True, max_length=200, null=True)),
                ('consensus_repeat_sequence', models.TextField(blank=True, null=True)),
                ('cas_genes', models.TextField(blank=True, null=True)),
                ('plasmid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crisprs', to='database.plasmid')),
            ],
        ),
    ]
