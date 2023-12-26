# Generated by Django 4.2.6 on 2023-12-24 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("drink", "0005_remove_notebook_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notebook",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notebooks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
