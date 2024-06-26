# Generated by Django 5.0.2 on 2024-05-08 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_rename_who_to_visit_visitor_whom_to_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='exited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='visitor',
            name='time_of_exit',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
