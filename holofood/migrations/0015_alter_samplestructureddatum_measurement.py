# Generated by Django 4.0.6 on 2022-08-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0014_remove_samplestructureddatum_partner_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplestructureddatum",
            name="measurement",
            field=models.CharField(max_length=200),
        ),
    ]