from rest_framework import serializers
from chat.models import Message, Conversation, ChatAttachment
from visitors.serializers import VisitorSessionSerializer, VisitorSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    
    sender_type_display = serializers.CharField(source='get_sender_type_display', read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'session', 'sender_type', 'sender_type_display',
            'sender_id', 'message_type', 'message_type_display',
            'content', 'metadata', 'sequence_number', 'is_read', 'read_at',
            'intent', 'confidence_score', 'entities', 'language',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sequence_number', 'created_at', 'updated_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new messages."""
    
    class Meta:
        model = Message
        fields = [
            'session', 'sender_type', 'sender_id', 'message_type',
            'content', 'metadata', 'language'
        ]


class ChatAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for ChatAttachment model."""
    
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatAttachment
        fields = [
            'id', 'message', 'file_type', 'file_size', 'file_size_mb',
            'file_url', 'thumbnail_url', 'filename', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    
    visitor_name = serializers.CharField(source='visitor.display_name', read_only=True)
    visitor_avatar = serializers.URLField(source='visitor.avatar_url', read_only=True)
    staff_name = serializers.CharField(source='staff.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'visitor', 'visitor_name', 'visitor_avatar',
            'staff', 'staff_name', 'active_session',
            'status', 'status_display', 'last_message_at',
            'last_message_preview', 'unread_count',
            'assigned_at', 'closed_at'
        ]
        read_only_fields = ['id', 'assigned_at', 'closed_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed conversation serializer with messages."""
    
    visitor = VisitorSerializer(read_only=True)
    staff_name = serializers.CharField(source='staff.username', read_only=True)
    recent_messages = serializers.SerializerMethodField()
    total_messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'visitor', 'staff_name', 'active_session',
            'status', 'last_message_at', 'last_message_preview',
            'unread_count', 'assigned_at', 'closed_at',
            'recent_messages', 'total_messages'
        ]
    
    def get_recent_messages(self, obj):
        from chat.models import Message
        messages = Message.objects.filter(
            session__conversation=obj
        ).order_by('-created_at')[:10]
        return MessageSerializer(messages, many=True).data
    
    def get_total_messages(self, obj):
        from chat.models import Message
        return Message.objects.filter(session__conversation=obj).count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating conversations."""
    
    class Meta:
        model = Conversation
        fields = ['visitor', 'staff', 'status']
