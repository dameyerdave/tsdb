from django.contrib import admin
from .models import (
    ApexConfig,
    ApexChart,
    Measurement,
    Feature,
    Entity,
    Annotation,
    AnnotationDefinition,
)
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


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("entity", "definition")
    search_fields = ("entity",)
    list_filter = ("entity__name", "definition__name")


@admin.register(AnnotationDefinition)
class AnnotationDefinitionAdmin(admin.ModelAdmin):
    pass
