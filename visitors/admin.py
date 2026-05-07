from django.contrib import admin
from .models import Visitor, VisitorSession, VisitorTag


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'platform', 'service_status', 'is_online', 'language', 'phone_number', 'last_visit_time']
    list_filter = ['service_status', 'is_online', 'language', 'platform', 'project']
    search_fields = ['name', 'nickname', 'phone_number', 'email', 'platform_open_id']
    readonly_fields = ['id', 'first_visit_time', 'last_visit_time', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Identification', {
            'fields': ('id', 'project', 'platform', 'platform_open_id')
        }),
        ('Personal Information', {
            'fields': ('name', 'nickname', 'nickname_zh', 'avatar_url', 'phone_number', 'email', 'company', 'job_title')
        }),
        ('Additional Info', {
            'fields': ('source', 'note', 'custom_attributes'),
            'classes': ('collapse',)
        }),
        ('Activity Tracking', {
            'fields': ('first_visit_time', 'last_visit_time', 'last_message_at', 'visitor_send_count', 'is_online')
        }),
        ('Service Status', {
            'fields': ('service_status', 'ai_disabled', 'ai_fallback_retry_count')
        }),
        ('Locale & Network', {
            'fields': ('timezone', 'language', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('Geolocation', {
            'fields': ('geo_country', 'geo_region', 'geo_city', 'geo_isp'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VisitorSession)
class VisitorSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'visitor', 'staff', 'session_start', 'session_end', 'status']
    list_filter = ['status', 'session_start']
    search_fields = ['visitor__name', 'visitor__nickname', 'staff__username']
    readonly_fields = ['id', 'session_start', 'session_end']


@admin.register(VisitorTag)
class VisitorTagAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'tag', 'created_at']
    list_filter = ['tag', 'created_at']
    search_fields = ['visitor__name', 'tag__name']
    readonly_fields = ['id', 'created_at']
