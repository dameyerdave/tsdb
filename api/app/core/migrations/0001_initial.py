# Generated by Django 4.1.5 on 2023-01-13 13:23

import core.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApexConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('own_config', models.JSONField(blank=True, default=core.models.get_default_apex_options, null=True)),
                ('inherit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='inheritors', to='core.apexconfig')),
                ('mixins', models.ManyToManyField(blank=True, related_name='mixin_sources', to='core.apexconfig')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ApexChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('sensors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('switches', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='charts', to='core.apexconfig')),
            ],
        ),
        migrations.CreateModel(
            name='SwitchState',
            fields=[
                ('time', models.DateTimeField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('on', models.BooleanField(default=False)),
                ('switch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.switch')),
            ],
            options={
                'ordering': ('time',),
                'unique_together': {('time', 'switch')},
                'index_together': {('time', 'switch')},
            },
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('time', models.DateTimeField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('value', models.FloatField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sensor')),
            ],
            options={
                'ordering': ('time',),
                'unique_together': {('time', 'sensor')},
                'index_together': {('time', 'sensor')},
            },
        ),
    ]
