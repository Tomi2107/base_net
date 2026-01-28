from django.contrib import admin
from .models import Ad, Zone

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "advertiser", "approved", "active", "views", "clicks")
    list_filter = ("approved", "active", "zones")
    search_fields = ("title",)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
