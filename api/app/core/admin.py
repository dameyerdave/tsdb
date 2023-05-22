from django.contrib import admin
from .models import ApexConfig, ApexChart, Measurement, Feature, Entity
from jsoneditor.admin import JSONFieldAdminMixin


@admin.register(ApexConfig)
class ApexConfigAdmin(JSONFieldAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ApexChart)
class ApexChartAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass
