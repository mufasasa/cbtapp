# Generated by Django 5.0.2 on 2024-04-09 10:30

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations_app', '0007_examination_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OrganisationComplain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('topic', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('not_attended', 'Not Attended'), ('waiting', 'Waiting'), ('cleared', 'Cleared')], default='not_attended', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complains', to='organisations_app.organisationadmin')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complains', to='organisations_app.organisation')),
            ],
        ),
    ]