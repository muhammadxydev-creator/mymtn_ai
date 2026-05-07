from django.contrib import admin
from .models import Message, Conversation, ChatAttachment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'sender_type', 'message_type', 'content_preview', 'intent', 'confidence_score', 'language', 'created_at']
    list_filter = ['sender_type', 'message_type', 'intent', 'language', 'is_read']
    search_fields = ['content', 'intent']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Message Info', {
            'fields': ('id', 'session', 'sender_type', 'sender_id')
        }),
        ('Content', {
            'fields': ('message_type', 'content', 'metadata')
        }),
        ('Tracking', {
            'fields': ('sequence_number', 'is_read', 'read_at')
        }),
        ('AI Analysis', {
            'fields': ('intent', 'confidence_score', 'entities', 'language'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'visitor', 'staff', 'status', 'unread_count', 'last_message_preview', 'last_message_at']
    list_filter = ['status', 'last_message_at']
    search_fields = ['visitor__name', 'visitor__nickname', 'staff__username']
    readonly_fields = ['id', 'assigned_at', 'closed_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('id', 'visitor', 'staff', 'active_session')
        }),
        ('Status', {
            'fields': ('status', 'unread_count')
        }),
        ('Last Message', {
            'fields': ('last_message_at', 'last_message_preview')
        }),
        ('Assignment', {
            'fields': ('assigned_at', 'closed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatAttachment)
class ChatAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'filename', 'file_type', 'file_size', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['filename']
    readonly_fields = ['id', 'created_at']
