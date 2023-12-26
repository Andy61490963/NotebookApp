# Generated by Django 4.2.6 on 2023-12-24 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("drink", "0004_remove_note_user_notebook_note_notebook"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notebook",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="notebook",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="notebook",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notebook",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]