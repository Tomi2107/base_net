from django.contrib import admin
from .models import ParroquialPost


@admin.register(ParroquialPost)
class ParroquialPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'zone', 'author', 'created_at')
    list_filter = ('service_type', 'zone')
    search_fields = ('title', 'content', 'zone')
