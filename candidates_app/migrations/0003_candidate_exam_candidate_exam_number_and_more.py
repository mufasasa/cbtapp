# Generated by Django 5.0.2 on 2024-04-16 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates_app', '0002_candidate_nin_candidate_phone_candidate_phone2_and_more'),
        ('organisations_app', '0008_organisation_active_organisationcomplain'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_candidates', to='organisations_app.examination'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='exam_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='organisation',
        ),
        migrations.AddField(
            model_name='candidate',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='organisations_app.organisation'),
        ),
    ]