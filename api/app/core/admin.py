from django.contrib import admin
from .models import ApexConfig, ApexChart
from jsoneditor.admin import JSONFieldAdminMixin


@admin.register(ApexConfig)
class ApexConfigAdmin(JSONFieldAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ApexChart)
class ApexConfigAdmin(admin.ModelAdmin):
    pass
