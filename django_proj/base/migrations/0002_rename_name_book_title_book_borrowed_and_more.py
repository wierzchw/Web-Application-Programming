# Generated by Django 4.2.7 on 2023-12-31 09:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book",
            old_name="name",
            new_name="title",
        ),
        migrations.AddField(
            model_name="book",
            name="borrowed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="book",
            name="releaseYear",
            field=models.IntegerField(default=2137),
        ),
        migrations.AddField(
            model_name="borrow",
            name="book",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="base.book"
            ),
        ),
        migrations.AddField(
            model_name="borrow",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="base.user"
            ),
        ),
        migrations.AlterField(
            model_name="borrow",
            name="endDate",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 1, 14, 10, 41, 30, 630640)
            ),
        ),
    ]
