from rest_framework import serializers
from knowledge_base.models import (
    KnowledgeBase, Document, QAPair, 
    WebsiteCrawl, CrawledPage, KnowledgeFeedback
)


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeBase model."""
    
    creator_username = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    
    class Meta:
        model = KnowledgeBase
        fields = [
            'id', 'project', 'name', 'description', 'category',
            'is_public', 'allow_ai_training', 'language',
            'document_count', 'qa_pair_count', 'last_updated_at',
            'creator_username', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'document_count', 'qa_pair_count', 
            'last_updated_at', 'created_at', 'updated_at'
        ]


class KnowledgeBaseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating knowledge bases."""
    
    class Meta:
        model = KnowledgeBase
        fields = [
            'project', 'name', 'description', 'category',
            'is_public', 'allow_ai_training', 'language'
        ]


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Document model."""
    
    knowledge_base_name = serializers.CharField(
        source='knowledge_base.name', 
        read_only=True
    )
    file_type_display = serializers.CharField(
        source='get_file_type_display', 
        read_only=True
    )
    processing_status_display = serializers.CharField(
        source='get_processing_status_display', 
        read_only=True
    )
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'knowledge_base', 'knowledge_base_name', 'title',
            'file_url', 'file_size', 'file_size_mb', 'file_type',
            'file_type_display', 'mime_type', 'processing_status',
            'processing_status_display', 'chunk_count', 'embedding_model',
            'error_message', 'source_type', 'metadata',
            'created_at', 'updated_at', 'processed_at'
        ]
        read_only_fields = [
            'id', 'chunk_count', 'embedding_model', 'error_message',
            'created_at', 'updated_at', 'processed_at'
        ]
    
    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)


class DocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating documents."""
    
    class Meta:
        model = Document
        fields = [
            'knowledge_base', 'title', 'file_url', 'file_size',
            'file_type', 'mime_type', 'source_type', 'metadata'
        ]


class QAPairSerializer(serializers.ModelSerializer):
    """Serializer for QAPair model."""
    
    knowledge_base_name = serializers.CharField(
        source='knowledge_base.name', 
        read_only=True
    )
    creator_username = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    tag_names = serializers.SerializerMethodField()
    
    class Meta:
        model = QAPair
        fields = [
            'id', 'knowledge_base', 'knowledge_base_name', 'question',
            'answer', 'category', 'tags', 'tag_names', 'usage_count',
            'helpful_count', 'not_helpful_count', 'status', 'status_display',
            'source_type', 'source_url', 'similar_questions', 'embeddings',
            'creator_username', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'usage_count', 'helpful_count', 'not_helpful_count',
            'created_at', 'updated_at'
        ]
    
    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]


class QAPairCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Q&A pairs."""
    
    class Meta:
        model = QAPair
        fields = [
            'knowledge_base', 'question', 'answer', 'category',
            'tags', 'status', 'source_type', 'source_url'
        ]


class QAPairBulkImportSerializer(serializers.Serializer):
    """Serializer for bulk importing Q&A pairs."""
    
    knowledge_base_id = serializers.UUIDField()
    qa_pairs = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


class WebsiteCrawlSerializer(serializers.ModelSerializer):
    """Serializer for WebsiteCrawl model."""
    
    knowledge_base_name = serializers.CharField(
        source='knowledge_base.name', 
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
    )
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WebsiteCrawl
        fields = [
            'id', 'knowledge_base', 'knowledge_base_name', 'url',
            'max_depth', 'allowed_domains', 'excluded_patterns',
            'status', 'status_display', 'pages_crawled', 'pages_failed',
            'error_message', 'is_scheduled', 'cron_expression',
            'progress_percentage', 'created_at', 'updated_at',
            'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'pages_crawled', 'pages_failed', 'error_message',
            'created_at', 'updated_at', 'started_at', 'completed_at'
        ]
    
    def get_progress_percentage(self, obj):
        total = obj.pages_crawled + obj.pages_failed
        if total == 0:
            return 0
        return round((obj.pages_crawled / total) * 100, 2)


class WebsiteCrawlCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating website crawls."""
    
    class Meta:
        model = WebsiteCrawl
        fields = [
            'knowledge_base', 'url', 'max_depth', 'allowed_domains',
            'excluded_patterns', 'is_scheduled', 'cron_expression'
        ]


class CrawledPageSerializer(serializers.ModelSerializer):
    """Serializer for CrawledPage model."""
    
    class Meta:
        model = CrawledPage
        fields = [
            'id', 'website_crawl', 'url', 'title', 'content',
            'html_content', 'chunk_count', 'embeddings_generated',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class KnowledgeFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeFeedback model."""
    
    feedback_type_display = serializers.CharField(
        source='get_feedback_type_display', 
        read_only=True
    )
    question_preview = serializers.CharField(
        source='qa_pair.question', 
        read_only=True
    )
    
    class Meta:
        model = KnowledgeFeedback
        fields = [
            'id', 'qa_pair', 'question_preview', 'feedback_type',
            'feedback_type_display', 'comment', 'visitor_id',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class KnowledgeFeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating feedback."""
    
    class Meta:
        model = KnowledgeFeedback
        fields = [
            'qa_pair', 'feedback_type', 'comment', 'visitor_id'
        ]
