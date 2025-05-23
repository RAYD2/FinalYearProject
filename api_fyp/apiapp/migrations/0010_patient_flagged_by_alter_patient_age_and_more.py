# Generated by Django 5.1.1 on 2025-04-27 10:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiapp", "0009_rename_doctor_patient_assigned_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="flagged_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flagged_by",
                to="apiapp.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="AGE",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="ASF",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="ETIV",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="MRI_ID",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="NWBV",
            field=models.FloatField(
                null=True, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="SUBJECT_ID",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
