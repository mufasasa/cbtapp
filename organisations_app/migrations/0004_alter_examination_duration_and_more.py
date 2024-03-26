# Generated by Django 5.0.2 on 2024-03-26 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations_app', '0003_alter_examination_candidates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examination',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examination',
            name='instructions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examination',
            name='passing_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examination',
            name='total_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
