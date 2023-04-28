# Generated by Django 4.2 on 2023-04-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("holofood", "0029_alter_sample_sample_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sample",
            name="metabolights_files",
        ),
        migrations.AddField(
            model_name="sample",
            name="metabolights_study",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]