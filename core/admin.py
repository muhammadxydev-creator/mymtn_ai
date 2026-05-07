from django.contrib import admin
from .models import Staff, Project, Platform, Tag


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_online', 'max_concurrent_chats', 'language_preference', 'last_active_at']
    list_filter = ['role', 'is_online', 'language_preference']
    search_fields = ['username', 'email', 'phone_number']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_active_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_staff', 'is_superuser', 'is_active')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'avatar_url')
        }),
        ('Work Settings', {
            'fields': ('is_online', 'max_concurrent_chats', 'language_preference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_active_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform_type', 'project', 'is_active', 'created_at']
    list_filter = ['platform_type', 'is_active', 'project']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'project', 'created_at']
    list_filter = ['project']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
