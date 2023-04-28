# Generated by Django 4.1.2 on 2023-02-09 15:21
import logging

from django.db import migrations, models
import django.db.models.deletion


def create_animals_for_samples(apps, schema_editor):
    """
    Creates an Animal object for each animal code in the Samples.
    This is really for development purposes only...
    Final public data import expects that samples will already be stratified into animal-level and extraction-level.
    """
    Sample = apps.get_model("holofood", "Sample")
    Animal = apps.get_model("holofood", "Animal")

    for sample in Sample.objects.all():
        animal, created = Animal.objects.get_or_create(
            animal_code=sample.animal_code,
            defaults={
                "accession": sample.accession,
                "system": sample.system,
            },
        )
        if created:
            logging.info(
                f"Created Animal {animal.animal_code} from Sample {sample.accession}"
            )
        sample.animal = animal
        logging.info(f"Set Animal to {animal.accession} for Sample {sample.accession}")
        sample.save()


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0024_alter_analysissummary_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Animal",
            fields=[
                (
                    "accession",
                    models.CharField(max_length=15, primary_key=True, serialize=False),
                ),
                (
                    "system",
                    models.CharField(
                        choices=[("chicken", "chicken"), ("salmon", "salmon")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "animal_code",
                    models.CharField(max_length=10),
                ),
            ],
        ),
        migrations.AddField(
            model_name="sample",
            name="animal",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="holofood.animal",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            create_animals_for_samples, reverse_code=migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name="sample",
            name="animal_code",
        ),
        migrations.RemoveField(
            model_name="sample",
            name="system",
        ),
        migrations.CreateModel(
            name="AnimalStructuredDatum",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("ena", "ena"), ("biosamples", "biosamples")],
                        max_length=15,
                    ),
                ),
                ("measurement", models.CharField(max_length=200)),
                ("units", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "partner_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "partner_iri",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "animal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="structured_metadata",
                        to="holofood.animal",
                    ),
                ),
                (
                    "marker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="holofood.samplemetadatamarker",
                    ),
                ),
            ],
            options={
                "ordering": ("marker__type", "marker__name", "id"),
            },
        ),
    ]