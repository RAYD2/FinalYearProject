# Generated by Django 5.1.1 on 2025-04-28 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apiapp", "0014_remove_visit_visit_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="visit", name="DATE_VISIT", field=models.DateField(null=True),
        ),
    ]
