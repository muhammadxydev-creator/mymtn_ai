from django.db import models
from django.conf import settings
from uuid import uuid4
from core.models import Project


class IntentCategory(models.Model):
    """
    Intent category model for classifying user queries.
    Based on myMTN NG use cases from Chapter 3.
    """
    
    INTENT_CHOICES = [
        ('check_balance', 'Check Balance'),
        ('buy_data', 'Buy Data Bundle'),
        ('buy_airtime', 'Buy Airtime'),
        ('subscribe_plan', 'Subscribe to Plan'),
        ('complaint', 'Complaint'),
        ('greeting', 'Greeting'),
        ('escalate_to_human', 'Escalate to Human Agent'),
        ('account_issue', 'Account Issue'),
        ('network_issue', 'Network Issue'),
        ('billing_inquiry', 'Billing Inquiry'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='intent_categories'
    )
    name = models.CharField(max_length=100)
    intent_code = models.CharField(
        max_length=50,
        choices=INTENT_CHOICES,
        unique=True
    )
    description = models.TextField(blank=True, null=True)
    training_samples_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'nlp_intent_category'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_intent_code_display()})"


class Entity(models.Model):
    """
    Entity model for extracting structured data from user messages.
    Examples: phone_number, amount, plan_type, etc.
    """
    
    ENTITY_TYPE_CHOICES = [
        ('phone_number', 'Phone Number'),
        ('amount', 'Amount'),
        ('plan_type', 'Plan Type'),
        ('date', 'Date'),
        ('location', 'Location'),
        ('account_number', 'Account Number'),
        ('transaction_id', 'Transaction ID'),
        ('product_name', 'Product Name'),
        ('duration', 'Duration'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='entities'
    )
    name = models.CharField(max_length=100)
    entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPE_CHOICES
    )
    description = models.TextField(blank=True, null=True)
    extraction_pattern = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'nlp_entity'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"


class NLPModel(models.Model):
    """
    NLP Model configuration for intent classification and entity extraction.
    Uses AfroXLMR transformer model as specified in Chapter 3.
    """
    
    MODEL_TYPE_CHOICES = [
        ('intent_classification', 'Intent Classification'),
        ('entity_extraction', 'Entity Extraction'),
        ('language_detection', 'Language Detection'),
        ('sentiment_analysis', 'Sentiment Analysis'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='nlp_models'
    )
    name = models.CharField(max_length=255)
    model_type = models.CharField(
        max_length=50,
        choices=MODEL_TYPE_CHOICES
    )
    model_path = models.CharField(max_length=500, blank=True, null=True)
    model_version = models.CharField(max_length=50, default='1.0.0')
    base_model = models.CharField(max_length=100, default='AfroXLMR')
    accuracy_score = models.FloatField(null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Configuration
    config = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'nlp_model'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (v{self.model_version})"


class TrainingSample(models.Model):
    """
    Training sample for NLP model training and improvement.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    intent_category = models.ForeignKey(
        IntentCategory,
        on_delete=models.CASCADE,
        related_name='training_samples'
    )
    text = models.TextField()
    language = models.CharField(max_length=10, default='en')
    entities = models.JSONField(default=list, blank=True)
    is_validated = models.BooleanField(default=False)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'nlp_training_sample'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['intent_category', 'language']),
        ]
    
    def __str__(self):
        return f"{self.text[:50]}..."


class NLPPredictionLog(models.Model):
    """
    Log of NLP predictions for monitoring and improvement.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='nlp_prediction_logs'
    )
    input_text = models.TextField()
    detected_language = models.CharField(max_length=10, default='en')
    predicted_intent = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    extracted_entities = models.JSONField(default=list, blank=True)
    processing_time_ms = models.PositiveIntegerField()
    model_used = models.CharField(max_length=255)
    
    # Feedback
    is_correct = models.BooleanField(null=True, blank=True)
    corrected_intent = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nlp_prediction_log'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['predicted_intent', '-created_at']),
            models.Index(fields=['confidence_score']),
        ]
    
    def __str__(self):
        return f"Prediction: {self.predicted_intent} ({self.confidence_score:.2f})"
