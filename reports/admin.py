from django.contrib import admin
from .models import Report, Note

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('project', 'author', 'title', 'content', 'status', 'feedback')
        }),
        ('Дата и время', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('content', 'author__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('author', 'content', 'category', 'content_type', 'object_id')
        }),
        ('Дата и время', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )