# Generated by Django 5.1.1 on 2025-04-28 00:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiapp", "0011_visit_remove_patient_age_remove_patient_asf_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="visit",
            name="visits",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="visits",
                to="apiapp.patient",
            ),
        ),
    ]
