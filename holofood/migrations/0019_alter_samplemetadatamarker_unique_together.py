# Generated by Django 4.0.6 on 2022-08-15 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0018_sample_ena_run_accessions"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="samplemetadatamarker",
            unique_together={("name", "type")},
        ),
    ]
