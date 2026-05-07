from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from core.models import Staff, Project, Platform, Tag
from core.serializers import (
    StaffSerializer, StaffCreateSerializer, StaffDetailSerializer,
    ProjectSerializer, PlatformSerializer, PlatformCreateSerializer,
    TagSerializer
)

StaffModel = get_user_model()


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing staff members.
    """
    queryset = StaffModel.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return StaffCreateSerializer
        elif self.action == 'retrieve':
            return StaffDetailSerializer
        return StaffSerializer
    
    def get_queryset(self):
        queryset = StaffModel.objects.all()
        role = self.request.query_params.get('role')
        is_online = self.request.query_params.get('is_online')
        
        if role:
            queryset = queryset.filter(role=role)
        if is_online is not None:
            queryset = queryset.filter(is_online=is_online.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def toggle_online(self, request, pk=None):
        """Toggle staff online status."""
        staff = self.get_object()
        staff.is_online = not staff.is_online
        staff.save(update_fields=['is_online'])
        return Response({'status': 'success', 'is_online': staff.is_online})
    
    @action(detail=False, methods=['get'])
    def online_staff(self, request):
        """Get all online staff members."""
        queryset = self.queryset.filter(is_online=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available_for_chat(self, request):
        """Get staff available for new chat assignments."""
        from visitors.models import VisitorSession
        available_staff = []
        for staff in self.queryset.filter(is_online=True, role='agent'):
            active_sessions = VisitorSession.objects.filter(
                staff=staff, 
                status='active'
            ).count()
            if active_sessions < staff.max_concurrent_chats:
                available_staff.append(staff)
        
        serializer = self.get_serializer(available_staff, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Project.objects.all()
        is_active = self.request.query_params.get('is_active')
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a project."""
        project = self.get_object()
        project.is_active = True
        project.save(update_fields=['is_active'])
        return Response({'status': 'success'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a project."""
        project = self.get_object()
        project.is_active = False
        project.save(update_fields=['is_active'])
        return Response({'status': 'success'})


class PlatformViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing communication platforms.
    """
    queryset = Platform.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PlatformCreateSerializer
        return PlatformSerializer
    
    def get_queryset(self):
        queryset = Platform.objects.all()
        project_id = self.request.query_params.get('project_id')
        platform_type = self.request.query_params.get('platform_type')
        is_active = self.request.query_params.get('is_active')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if platform_type:
            queryset = queryset.filter(platform_type=platform_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Tag.objects.all()
        project_id = self.request.query_params.get('project_id')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        
        return queryset
