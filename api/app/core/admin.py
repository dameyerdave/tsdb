from django.contrib import admin
from .models import ApexConfig


@admin.register(ApexConfig)
class ApexConfigAdmin(admin.ModelAdmin):
    pass
