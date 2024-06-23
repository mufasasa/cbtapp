# Generated by Django 5.0.2 on 2024-05-07 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations_app', '0013_candidateexam_score_examination_auto_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateexam',
            name='admitted_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='candidateexam',
            name='time_admitted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]