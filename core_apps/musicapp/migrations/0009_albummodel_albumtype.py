# Generated by Django 5.1.6 on 2025-04-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0008_alter_albummodel_artist_id_alter_albummodel_genre_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='albummodel',
            name='albumtype',
            field=models.SmallIntegerField(default=1),
        ),
    ]
