from django.contrib import admin
from .models import MusicFile

@admin.register(MusicFile)
class MusicFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'access']
    list_filter = ['access']
    search_fields = ['title', 'uploaded_by__username', 'allowed_users__username']
    readonly_fields = ['stream_url']
    fieldsets = (
        (None, {
            'fields': ('title', 'file', 'access')
        }),
        ('Allowed Users', {
            'fields': ('allowed_users',),
            'classes': ('collapse',)
        }),
        ('Read-Only Fields', {
            'fields': ('stream_url',),
            'classes': ('collapse', 'wide')
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
