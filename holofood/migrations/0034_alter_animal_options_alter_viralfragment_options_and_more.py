# Generated by Django 4.2 on 2024-01-17 12:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("holofood", "0033_remove_sample_ena_run_accessions_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="animal",
            options={"ordering": ("accession",)},
        ),
        migrations.AlterModelOptions(
            name="viralfragment",
            options={"ordering": ("id",)},
        ),
        migrations.RemoveField(
            model_name="viralfragment",
            name="host_mag",
        ),
    ]
