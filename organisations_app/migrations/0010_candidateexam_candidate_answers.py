# Generated by Django 5.0.2 on 2024-04-19 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations_app', '0009_candidateexam'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateexam',
            name='candidate_answers',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
