# Generated by Django 1.10.5 on 2017-02-26 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DownLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dl_url", models.URLField(verbose_name="download url")),
                (
                    "dl_url_text",
                    models.CharField(
                        max_length=100, verbose_name="text for download url"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Soft",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="app name")),
                (
                    "version",
                    models.CharField(max_length=100, verbose_name="app version"),
                ),
                ("upd_date", models.DateField(verbose_name="date updated")),
                ("url_key", models.SlugField(unique=True, verbose_name="url slug")),
            ],
            options={
                "verbose_name": "Soft entry",
                "verbose_name_plural": "Soft enries",
                "ordering": ["-upd_date"],
            },
        ),
        migrations.AddField(
            model_name="downlink",
            name="soft",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="links",
                to="soft.Soft",
            ),
        ),
    ]
