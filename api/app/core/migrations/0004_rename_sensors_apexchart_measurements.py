# Generated by Django 4.2.1 on 2023-05-22 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_apexchart_switches_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apexchart',
            old_name='sensors',
            new_name='measurements',
        ),
    ]