# Generated by Django 5.1.6 on 2025-03-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0005_alter_musicmodel_musiccover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicmodel',
            name='duration',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
