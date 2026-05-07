from django.db import models
from django.conf import settings
from uuid import uuid4
from core.models import Project, Tag


class KnowledgeSourceType(models.TextChoices):
    """Knowledge source type enumeration."""
    MANUAL = 'manual', 'Manual Entry'
    DOCUMENT = 'document', 'Document Upload'
    WEB_SCRAPED = 'web_scraped', 'Web Scraped'
    IMPORTED = 'imported', 'Imported'


class KnowledgeBase(models.Model):
    """
    Knowledge Base model for storing organized collections of knowledge.
    Based on TGO knowledge base design and Chapter 3 requirements.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='knowledge_bases'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    # Configuration
    is_public = models.BooleanField(default=False)
    allow_ai_training = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    
    # Statistics
    document_count = models.PositiveIntegerField(default=0)
    qa_pair_count = models.PositiveIntegerField(default=0)
    last_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_knowledge_bases'
    )
    
    class Meta:
        db_table = 'knowledge_base'
        ordering = ['-created_at']
        unique_together = ['project', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"
    
    def update_statistics(self):
        """Update document and QA pair counts."""
        self.document_count = self.documents.count()
        self.qa_pair_count = self.qa_pairs.count()
        from django.utils import timezone
        self.last_updated_at = timezone.now()
        self.save(update_fields=['document_count', 'qa_pair_count', 'last_updated_at', 'updated_at'])


class Document(models.Model):
    """
    Document model for uploaded files in the knowledge base.
    """
    
    PROCESSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    DOCUMENT_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('txt', 'Text File'),
        ('html', 'HTML'),
        ('md', 'Markdown'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=255)
    file_url = models.URLField()
    file_size = models.PositiveIntegerField()  # in bytes
    file_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other'
    )
    mime_type = models.CharField(max_length=100)
    
    # Processing
    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default='pending'
    )
    chunk_count = models.PositiveIntegerField(default=0)
    embedding_model = models.CharField(max_length=100, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    
    # Metadata
    source_type = models.CharField(
        max_length=20,
        choices=KnowledgeSourceType.choices,
        default=KnowledgeSourceType.MANUAL
    )
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'knowledge_base_document'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['knowledge_base', 'processing_status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_file_type_display()})"


class QAPair(models.Model):
    """
    Question-Answer pair model for structured knowledge.
    Based on TGO Q&A knowledge base design.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='qa_pairs'
    )
    question = models.TextField()
    answer = models.TextField()
    
    # Categorization
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='qa_pairs'
    )
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Source
    source_type = models.CharField(
        max_length=20,
        choices=KnowledgeSourceType.choices,
        default=KnowledgeSourceType.MANUAL
    )
    source_url = models.URLField(blank=True, null=True)
    
    # AI-related
    similar_questions = models.JSONField(default=list, blank=True)
    embeddings = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_qa_pairs'
    )
    
    class Meta:
        db_table = 'knowledge_base_qa_pair'
        ordering = ['-usage_count', '-created_at']
        indexes = [
            models.Index(fields=['knowledge_base', 'status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"Q: {self.question[:50]}..."


class WebsiteCrawl(models.Model):
    """
    Website crawl configuration for automated knowledge extraction.
    Based on TGO website knowledge base design.
    """
    
    CRAWL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name='website_crawls'
    )
    url = models.URLField()
    max_depth = models.PositiveIntegerField(default=2)
    allowed_domains = models.JSONField(default=list, blank=True)
    excluded_patterns = models.JSONField(default=list, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=CRAWL_STATUS_CHOICES,
        default='pending'
    )
    pages_crawled = models.PositiveIntegerField(default=0)
    pages_failed = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    
    # Schedule
    is_scheduled = models.BooleanField(default=False)
    cron_expression = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'knowledge_base_website_crawl'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Crawl: {self.url}"


class CrawledPage(models.Model):
    """
    Individual page crawled from a website.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    website_crawl = models.ForeignKey(
        WebsiteCrawl,
        on_delete=models.CASCADE,
        related_name='pages'
    )
    url = models.URLField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    html_content = models.TextField(blank=True, null=True)
    
    # Processing
    chunk_count = models.PositiveIntegerField(default=0)
    embeddings_generated = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'knowledge_base_crawled_page'
        unique_together = ['website_crawl', 'url']
    
    def __str__(self):
        return f"{self.title} ({self.url})"


class KnowledgeFeedback(models.Model):
    """
    Feedback on knowledge base items for continuous improvement.
    """
    
    FEEDBACK_TYPE_CHOICES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect Information'),
        ('outdated', 'Outdated'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    qa_pair = models.ForeignKey(
        QAPair,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=FEEDBACK_TYPE_CHOICES
    )
    comment = models.TextField(blank=True, null=True)
    visitor_id = models.UUIDField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'knowledge_base_feedback'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_feedback_type_display()} - {self.qa_pair.question[:30]}..."
