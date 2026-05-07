from rest_framework import serializers
from visitors.models import Visitor, VisitorSession, VisitorTag
from core.serializers import TagSerializer


class VisitorSerializer(serializers.ModelSerializer):
    """Serializer for Visitor model."""
    
    project_name = serializers.CharField(source='project.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    service_status_display = serializers.CharField(
        source='get_service_status_display', 
        read_only=True
    )
    
    class Meta:
        model = Visitor
        fields = [
            'id', 'project', 'project_name', 'platform', 'platform_name',
            'platform_open_id', 'name', 'nickname', 'avatar_url',
            'phone_number', 'email', 'company', 'job_title',
            'source', 'note', 'custom_attributes',
            'first_visit_time', 'last_visit_time', 'last_message_at',
            'visitor_send_count', 'is_online', 'is_last_message_from_visitor',
            'is_last_message_from_ai', 'language', 'timezone',
            'geo_country', 'geo_city', 'service_status', 'service_status_display',
            'display_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'first_visit_time', 'last_visit_time', 
            'created_at', 'updated_at', 'display_name'
        ]


class VisitorCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new visitors."""
    
    class Meta:
        model = Visitor
        fields = [
            'project', 'platform', 'platform_open_id', 'name',
            'nickname', 'phone_number', 'email', 'language',
            'ip_address', 'geo_country', 'geo_city'
        ]


class VisitorDetailSerializer(serializers.ModelSerializer):
    """Detailed visitor serializer with session and tag info."""
    
    project_name = serializers.CharField(source='project.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    active_session = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True, source='visitor_tags.tag')
    total_sessions = serializers.SerializerMethodField()
    total_messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Visitor
        fields = [
            'id', 'project', 'project_name', 'platform', 'platform_name',
            'platform_open_id', 'name', 'nickname', 'avatar_url',
            'phone_number', 'email', 'display_name',
            'language', 'service_status', 'is_online',
            'active_session', 'tags', 'total_sessions', 'total_messages',
            'note', 'custom_attributes', 'created_at', 'updated_at'
        ]
    
    def get_active_session(self, obj):
        session = VisitorSession.objects.filter(
            visitor=obj, 
            status='active'
        ).first()
        if session:
            return {
                'id': str(session.id),
                'staff_id': str(session.staff.id) if session.staff else None,
                'started_at': session.session_start.isoformat()
            }
        return None
    
    def get_total_sessions(self, obj):
        return VisitorSession.objects.filter(visitor=obj).count()
    
    def get_total_messages(self, obj):
        from chat.models import Message
        sessions = VisitorSession.objects.filter(visitor=obj)
        return Message.objects.filter(session__in=sessions).count()


class VisitorSessionSerializer(serializers.ModelSerializer):
    """Serializer for VisitorSession model."""
    
    visitor_name = serializers.CharField(source='visitor.display_name', read_only=True)
    staff_name = serializers.CharField(source='staff.username', read_only=True)
    
    class Meta:
        model = VisitorSession
        fields = [
            'id', 'visitor', 'visitor_name', 'staff', 'staff_name',
            'session_start', 'session_end', 'status'
        ]
        read_only_fields = ['id', 'session_start']


class VisitorSessionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating visitor sessions."""
    
    class Meta:
        model = VisitorSession
        fields = ['visitor', 'staff', 'status']


class VisitorTagSerializer(serializers.ModelSerializer):
    """Serializer for VisitorTag relationship."""
    
    visitor_name = serializers.CharField(source='visitor.display_name', read_only=True)
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    tag_color = serializers.CharField(source='tag.color', read_only=True)
    
    class Meta:
        model = VisitorTag
        fields = ['id', 'visitor', 'visitor_name', 'tag', 'tag_name', 'tag_color', 'created_at']
        read_only_fields = ['id', 'created_at']
