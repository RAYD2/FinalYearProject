# Generated by Django 5.1.1 on 2025-04-23 21:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prediction",
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
                ("SUBJECT_ID", models.CharField(max_length=50, null=True)),
                ("Prediction_Result", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("date_of_birth", models.DateField(null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Patient",
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
                ("SUBJECT_ID", models.CharField(max_length=50, null=True)),
                ("MRI_ID", models.CharField(max_length=50, null=True)),
                (
                    "GENDER",
                    models.IntegerField(
                        choices=[(0, "Male"), (1, "Female")], null=True
                    ),
                ),
                (
                    "HAND",
                    models.IntegerField(choices=[(0, "Right"), (1, "Left")], null=True),
                ),
                (
                    "GROUP",
                    models.IntegerField(
                        choices=[
                            (0, "Non Demented"),
                            (1, "Demented"),
                            (2, "Converted"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "EDUCATION",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "SES",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                (
                    "CDR",
                    models.IntegerField(
                        choices=[
                            (0, "Non Demented"),
                            (0.5, "Very Mild AD"),
                            (1, "Mild AD"),
                            (2, "Moderate AD"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "MMSCORE",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                    ),
                ),
                (
                    "AGE",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "ETIV",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(30),
                        ],
                    ),
                ),
                (
                    "NWBV",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "ASF",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "Health_Provider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="current_patients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
