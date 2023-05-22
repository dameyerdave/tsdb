# Generated by Django 4.2.1 on 2023-05-22 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_sensors_apexchart_measurements'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('level', models.CharField(choices=[('I', 'INFO'), ('W', 'WARN'), ('E', 'ERROR')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.annotationdefinition')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entity')),
            ],
        ),
    ]
