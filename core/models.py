from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from uuid import uuid4


class Language(models.TextChoices):
    """
    Language choices for myMTN NG multilingual support.
    Includes English and major Nigerian languages as per Chapter 3.
    """
    ENGLISH = 'en', 'English'
    YORUBA = 'yo', 'Yoruba'
    HAUSA = 'ha', 'Hausa'
    IGBO = 'ig', 'Igbo'
    PIDGIN = 'pcm', 'Nigerian Pidgin'


class Staff(AbstractUser):
    """
    Staff model for customer support agents and administrators.
    Extends Django's AbstractUser to include additional fields.
    """
    
    STAFF_ROLE_CHOICES = [
        ('agent', 'Support Agent'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=STAFF_ROLE_CHOICES,
        default='agent'
    )
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    is_available = models.BooleanField(
        default=True,
        help_text='Indicates if staff is available to receive new chat assignments'
    )
    max_concurrent_chats = models.PositiveIntegerField(default=5)
    language_preference = models.CharField(max_length=10, default='en')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'core_staff'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def update_last_active(self):
        """Update the last active timestamp."""
        self.last_active_at = timezone.now()
        self.save(update_fields=['last_active_at'])
    
    @property
    def can_accept_chat(self):
        """Check if staff can accept new chat based on availability and concurrent limit."""
        from chat.models import Conversation
        if not self.is_available or not self.is_online:
            return False
        active_chats = Conversation.objects.filter(
            assigned_to=self,
            status='active'
        ).count()
        return active_chats < self.max_concurrent_chats


class Project(models.Model):
    """
    Project model for multi-tenant isolation.
    Each project represents a separate deployment or client.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Configuration
    config = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Platform(models.Model):
    """
    Platform model representing different communication channels.
    Examples: Website, WhatsApp, Telegram, Mobile App, etc.
    """
    
    PLATFORM_TYPE_CHOICES = [
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('mobile_app', 'Mobile App'),
        ('facebook', 'Facebook Messenger'),
        ('email', 'Email'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='platforms'
    )
    name = models.CharField(max_length=255)
    platform_type = models.CharField(
        max_length=50,
        choices=PLATFORM_TYPE_CHOICES
    )
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_platforms'
        unique_together = ['project', 'platform_type']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_type_display()})"


class Tag(models.Model):
    """
    Tag model for categorizing visitors and conversations.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    description = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_tags'
        unique_together = ['project', 'name']
        ordering = ['name']
    
    def __str__(self):
        return self.name
