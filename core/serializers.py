from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Staff, Project, Platform, Tag

StaffModel = get_user_model()


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model."""
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = StaffModel
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone_number', 'avatar_url',
            'is_online', 'max_concurrent_chats', 'language_preference',
            'is_staff', 'is_superuser', 'last_active_at', 'created_at'
        ]
        read_only_fields = ['id', 'last_active_at', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        staff = StaffModel(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class StaffCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new staff members."""
    
    class Meta:
        model = StaffModel
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'phone_number', 'language_preference', 'max_concurrent_chats'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        staff = StaffModel(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'is_active', 'config',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlatformSerializer(serializers.ModelSerializer):
    """Serializer for Platform model."""
    
    project_name = serializers.CharField(source='project.name', read_only=True)
    platform_type_display = serializers.CharField(
        source='get_platform_type_display', 
        read_only=True
    )
    
    class Meta:
        model = Platform
        fields = [
            'id', 'project', 'project_name', 'name', 'platform_type',
            'platform_type_display', 'config', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlatformCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating platforms."""
    
    class Meta:
        model = Platform
        fields = [
            'project', 'name', 'platform_type', 'config', 'is_active'
        ]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Tag
        fields = [
            'id', 'project', 'project_name', 'name', 'color',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for staff with additional info."""
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    active_sessions_count = serializers.SerializerMethodField()
    conversations_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StaffModel
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone_number', 'avatar_url',
            'is_online', 'max_concurrent_chats', 'language_preference',
            'last_active_at', 'created_at', 'active_sessions_count',
            'conversations_count'
        ]
    
    def get_active_sessions_count(self, obj):
        from visitors.models import VisitorSession
        return VisitorSession.objects.filter(
            staff=obj, 
            status='active'
        ).count()
    
    def get_conversations_count(self, obj):
        from chat.models import Conversation
        return Conversation.objects.filter(staff=obj).count()
