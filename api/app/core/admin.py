from django.contrib import admin
from .models import ApexConfig, ApexChart, Sensor, SensorReading, Switch, SwitchState
from jsoneditor.admin import JSONFieldAdminMixin


@admin.register(ApexConfig)
class ApexConfigAdmin(JSONFieldAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ApexChart)
class ApexChartAdmin(admin.ModelAdmin):
    pass


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    pass


@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    pass


@admin.register(SwitchState)
class SwitchStateAdmin(admin.ModelAdmin):
    pass
