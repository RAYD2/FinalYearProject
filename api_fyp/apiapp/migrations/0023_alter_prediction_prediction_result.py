# Generated by Django 5.1.1 on 2025-05-01 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiapp", "0022_alter_visit_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prediction",
            name="Prediction_Result",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
