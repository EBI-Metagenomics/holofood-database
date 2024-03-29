# Generated by Django 4.0.6 on 2022-08-18 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0019_alter_samplemetadatamarker_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="sample",
            name="metabolights_files",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name="sample",
            name="ena_run_accessions",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
