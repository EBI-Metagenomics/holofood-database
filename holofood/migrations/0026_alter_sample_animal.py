# Generated by Django 4.1.2 on 2023-02-09 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0025_animal_remove_sample_animal_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sample",
            name="animal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="samples",
                to="holofood.animal",
            ),
        ),
    ]
