# Generated by Django 4.2.1 on 2023-05-22 07:21

from django.db import migrations
import timescale.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_annotationdefinition_annotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='time',
            field=timescale.db.models.fields.TimescaleDateTimeField(default='2023-05-22T09:20:00', interval='1 day'),
            preserve_default=False,
        ),
    ]
