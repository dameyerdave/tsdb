# Generated by Django 4.1.5 on 2023-01-13 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_apexchart_sensors_alter_apexchart_switches'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apexchart',
            old_name='config',
            new_name='own_config',
        ),
    ]
