from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from visitors.models import Visitor, VisitorSession, VisitorTag
from visitors.serializers import (
    VisitorSerializer, VisitorCreateSerializer, VisitorDetailSerializer,
    VisitorSessionSerializer, VisitorSessionCreateSerializer,
    VisitorTagSerializer
)


class VisitorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing visitors.
    """
    queryset = Visitor.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VisitorCreateSerializer
        elif self.action == 'retrieve':
            return VisitorDetailSerializer
        return VisitorSerializer
    
    def get_queryset(self):
        queryset = Visitor.objects.all()
        project_id = self.request.query_params.get('project_id')
        platform_id = self.request.query_params.get('platform_id')
        service_status = self.request.query_params.get('service_status')
        is_online = self.request.query_params.get('is_online')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if platform_id:
            queryset = queryset.filter(platform_id=platform_id)
        if service_status:
            queryset = queryset.filter(service_status=service_status)
        if is_online is not None:
            queryset = queryset.filter(is_online=is_online.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def set_status_queued(self, request, pk=None):
        """Set visitor status to queued."""
        visitor = self.get_object()
        visitor.set_status_queued()
        return Response({'status': 'success', 'service_status': visitor.service_status})
    
    @action(detail=True, methods=['post'])
    def set_status_active(self, request, pk=None):
        """Set visitor status to active."""
        visitor = self.get_object()
        visitor.set_status_active()
        return Response({'status': 'success', 'service_status': visitor.service_status})
    
    @action(detail=True, methods=['post'])
    def set_status_closed(self, request, pk=None):
        """Set visitor status to closed."""
        visitor = self.get_object()
        visitor.set_status_closed()
        return Response({'status': 'success', 'service_status': visitor.service_status})
    
    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        """Get all sessions for a visitor."""
        visitor = self.get_object()
        sessions = VisitorSession.objects.filter(visitor=visitor)
        serializer = VisitorSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class VisitorSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing visitor sessions.
    """
    queryset = VisitorSession.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VisitorSessionCreateSerializer
        return VisitorSessionSerializer
    
    def get_queryset(self):
        queryset = VisitorSession.objects.all()
        visitor_id = self.request.query_params.get('visitor_id')
        staff_id = self.request.query_params.get('staff_id')
        status = self.request.query_params.get('status')
        
        if visitor_id:
            queryset = queryset.filter(visitor_id=visitor_id)
        if staff_id:
            queryset = queryset.filter(staff_id=staff_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close a session."""
        session = self.get_object()
        session.status = 'closed'
        from django.utils import timezone
        session.session_end = timezone.now()
        session.save(update_fields=['status', 'session_end'])
        return Response({'status': 'success'})


class VisitorTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing visitor tags.
    """
    queryset = VisitorTag.objects.all()
    serializer_class = VisitorTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = VisitorTag.objects.all()
        visitor_id = self.request.query_params.get('visitor_id')
        tag_id = self.request.query_params.get('tag_id')
        
        if visitor_id:
            queryset = queryset.filter(visitor_id=visitor_id)
        if tag_id:
            queryset = queryset.filter(tag_id=tag_id)
        
        return queryset
