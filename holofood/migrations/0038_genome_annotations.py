# Generated by Django 4.2 on 2024-07-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("holofood", "0037_genomesamplecontainment"),
    ]

    operations = [
        migrations.AddField(
            model_name="genome",
            name="annotations",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
