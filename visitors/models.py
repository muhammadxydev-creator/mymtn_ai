from django.db import models
from django.utils import timezone
from uuid import uuid4
from core.models import Project, Platform


class VisitorServiceStatus(models.TextChoices):
    """Visitor service status enumeration."""
    NEW = 'new', 'New'
    QUEUED = 'queued', 'Queued'
    ACTIVE = 'active', 'Active'
    CLOSED = 'closed', 'Closed'


class Visitor(models.Model):
    """
    Visitor model for external users/customers.
    Based on TGO visitor model with adaptations for myMTN support system.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name='visitors'
    )
    
    # Basic identification
    platform_open_id = models.CharField(max_length=255)
    name = models.CharField(max_length=100, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    nickname_zh = models.CharField(max_length=100, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    
    # Additional info
    source = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    custom_attributes = models.JSONField(default=dict, blank=True)
    
    # Activity tracking
    first_visit_time = models.DateTimeField(auto_now_add=True)
    last_visit_time = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    visitor_send_count = models.PositiveIntegerField(default=0)
    last_message_seq = models.PositiveIntegerField(default=0)
    is_last_message_from_visitor = models.BooleanField(default=False)
    is_last_message_from_ai = models.BooleanField(default=False)
    last_offline_time = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    ai_disabled = models.BooleanField(null=True, default=None)
    ai_fallback_retry_count = models.PositiveIntegerField(default=0)
    
    # Locale and network info
    timezone = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=10, default='en')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    # Geolocation
    geo_country = models.CharField(max_length=100, blank=True, null=True)
    geo_country_code = models.CharField(max_length=2, blank=True, null=True)
    geo_region = models.CharField(max_length=100, blank=True, null=True)
    geo_city = models.CharField(max_length=100, blank=True, null=True)
    geo_isp = models.CharField(max_length=100, blank=True, null=True)
    
    # Service status
    service_status = models.CharField(
        max_length=20,
        choices=VisitorServiceStatus.choices,
        default=VisitorServiceStatus.NEW
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'visitors_visitor'
        ordering = ['-last_visit_time']
        indexes = [
            models.Index(fields=['platform_open_id', 'platform']),
            models.Index(fields=['service_status']),
            models.Index(fields=['is_online']),
        ]
    
    def __str__(self):
        return self.display_name
    
    @property
    def display_name(self):
        """Get the best available display name for the visitor."""
        return self.name or self.nickname or self.platform_open_id
    
    @property
    def is_unassigned(self):
        """Check if visitor is unassigned (can be assigned to staff)."""
        return self.service_status in [
            VisitorServiceStatus.NEW.value,
            VisitorServiceStatus.CLOSED.value
        ]
    
    def set_status_queued(self):
        """Set visitor status to QUEUED."""
        self.service_status = VisitorServiceStatus.QUEUED.value
        self.save(update_fields=['service_status', 'updated_at'])
    
    def set_status_active(self):
        """Set visitor status to ACTIVE."""
        self.service_status = VisitorServiceStatus.ACTIVE.value
        self.save(update_fields=['service_status', 'updated_at'])
    
    def set_status_closed(self):
        """Set visitor status to CLOSED."""
        self.service_status = VisitorServiceStatus.CLOSED.value
        self.save(update_fields=['service_status', 'updated_at'])


class VisitorSession(models.Model):
    """
    Visitor session model tracking individual conversation sessions.
    Includes escalation logic for human handoff as per Chapter 3.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    staff = models.ForeignKey(
        'core.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    
    session_start = models.DateTimeField(auto_now_add=True)
    session_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active')
    
    # Escalation fields for human handoff (Chapter 3.3)
    escalated_to = models.ForeignKey(
        'core.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalated_sessions',
        help_text='Staff member to whom the session was escalated'
    )
    escalation_reason = models.TextField(
        blank=True,
        null=True,
        help_text='Reason for escalation to human agent'
    )
    escalation_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when escalation occurred'
    )
    is_escalated = models.BooleanField(
        default=False,
        help_text='Flag indicating if session requires human intervention'
    )
    
    class Meta:
        db_table = 'visitors_session'
        ordering = ['-session_start']
    
    def __str__(self):
        return f"Session {self.id} - {self.visitor.display_name}"
    
    def escalate_to(self, staff_member, reason=""):
        """Escalate session to a human staff member."""
        from django.utils import timezone
        self.escalated_to = staff_member
        self.escalation_reason = reason
        self.escalation_time = timezone.now()
        self.is_escalated = True
        self.save(update_fields=[
            'escalated_to', 'escalation_reason', 
            'escalation_time', 'is_escalated', 'updated_at'
        ])


class VisitorTag(models.Model):
    """
    Many-to-many relationship between visitors and tags.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='visitor_tags'
    )
    tag = models.ForeignKey(
        'core.Tag',
        on_delete=models.CASCADE,
        related_name='visitor_tags'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'visitors_visitor_tag'
        unique_together = ['visitor', 'tag']
    
    def __str__(self):
        return f"{self.visitor.display_name} - {self.tag.name}"
