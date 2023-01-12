from django.db import models
from django.utils import timezone
from datetime import timedelta as td
from django_jsonform.models.fields import JSONField
import json

with open('core/schemas/apex_options.json', 'r') as schema_file:
    APEX_OPTIONS_SCHEMA = json.load(schema_file)


class TimescaleModel(models.Model):
    def save(self, *args, **kwargs):
        # We want to smear the timestamp if sensors are read at the same time
        # we just add a µs to the time
        while self.__class__.objects.filter(time=self.time).exists():
            self.time += td(microseconds=1)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)


class SensorReading(TimescaleModel):
    time = models.DateTimeField(default=timezone.now, primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()

    @classmethod
    def add(cls, sensor: str, value: float):
        _sensor, created = Sensor.objects.get_or_create(name=sensor)
        cls.objects.create(sensor=_sensor, value=value)

    class Meta:
        unique_together = ('time', 'sensor')
        index_together = [
            ('time', 'sensor'),
        ]
        ordering = ('time',)


class Switch(models.Model):
    name = models.CharField(max_length=50, unique=True)


class SwitchState(TimescaleModel):
    time = models.DateTimeField(default=timezone.now, primary_key=True)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    on = models.BooleanField(default=False)

    @classmethod
    def add(cls, switch: str, on: bool):
        _switch, created = Switch.objects.get_or_create(name=switch)
        cls.objects.create(switch=_switch, on=on)

    class Meta:
        unique_together = ('time', 'switch')
        index_together = [
            ('time', 'switch'),
        ]
        ordering = ('time',)


class ApexConfig(models.Model):
    name = models.CharField(max_length=50, unique=True)
    config = JSONField(schema=APEX_OPTIONS_SCHEMA, null=True)

    class Meta:
        ordering = ('name',)
