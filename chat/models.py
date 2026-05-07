from django.db import models
from uuid import uuid4
from core.models import Staff
from visitors.models import Visitor, VisitorSession


class MessageType(models.TextChoices):
    """Message type enumeration."""
    TEXT = 'text', 'Text'
    IMAGE = 'image', 'Image'
    FILE = 'file', 'File'
    AUDIO = 'audio', 'Audio'
    VIDEO = 'video', 'Video'
    SYSTEM = 'system', 'System'
    AI_RESPONSE = 'ai_response', 'AI Response'


class Message(models.Model):
    """
    Message model for chat conversations.
    Based on TGO chat message structure.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    session = models.ForeignKey(
        VisitorSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Sender information
    sender_type = models.CharField(max_length=20, choices=[
        ('visitor', 'Visitor'),
        ('staff', 'Staff'),
        ('ai', 'AI'),
        ('system', 'System'),
    ])
    sender_id = models.UUIDField(null=True, blank=True)  # Can be visitor_id or staff_id
    
    # Message content
    message_type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT
    )
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)  # For files, images, etc.
    
    # Message tracking
    sequence_number = models.PositiveIntegerField(default=0)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # AI-related fields
    intent = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.FloatField(null=True, blank=True)
    entities = models.JSONField(default=list, blank=True)
    language = models.CharField(max_length=10, default='en')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_message'
        ordering = ['sequence_number', 'created_at']
        indexes = [
            models.Index(fields=['session', '-created_at']),
            models.Index(fields=['sender_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"Message {self.id} - {self.sender_type}"
    
    def mark_as_read(self):
        """Mark the message as read."""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])


class Conversation(models.Model):
    """
    Conversation model representing a chat between visitor and staff/AI.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    active_session = models.ForeignKey(
        VisitorSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversation'
    )
    
    # Status
    status = models.CharField(max_length=20, default='open', choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ])
    
    # Tracking
    last_message_at = models.DateTimeField(null=True, blank=True)
    last_message_preview = models.TextField(blank=True, null=True)
    unread_count = models.PositiveIntegerField(default=0)
    
    # Assignment info
    assigned_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'chat_conversation'
        ordering = ['-last_message_at']
        indexes = [
            models.Index(fields=['status', '-last_message_at']),
            models.Index(fields=['visitor', '-last_message_at']),
        ]
    
    def __str__(self):
        return f"Conversation with {self.visitor.display_name}"


class ChatAttachment(models.Model):
    """
    Attachment model for files, images, and media in chat messages.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    
    file_type = models.CharField(max_length=50)  # image/png, application/pdf, etc.
    file_size = models.PositiveIntegerField()  # in bytes
    file_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    filename = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_attachment'
    
    def __str__(self):
        return f"{self.filename} ({self.file_type})"
