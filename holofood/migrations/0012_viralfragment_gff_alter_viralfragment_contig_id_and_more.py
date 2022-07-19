# Generated by Django 4.0.6 on 2022-07-19 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0011_viralcatalogue_alter_genome_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="viralfragment",
            name="gff",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="viralfragment",
            name="contig_id",
            field=models.CharField(max_length=100, verbose_name="Contig ID"),
        ),
        migrations.AlterField(
            model_name="viralfragment",
            name="host_mag",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="viral_fragments",
                to="holofood.genome",
                verbose_name="Host MAG",
            ),
        ),
        migrations.AlterField(
            model_name="viralfragment",
            name="id",
            field=models.CharField(
                max_length=100, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]