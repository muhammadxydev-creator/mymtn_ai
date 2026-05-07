from django.contrib import admin
from .models import KnowledgeBase, Document, QAPair, WebsiteCrawl, CrawledPage, KnowledgeFeedback


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'category', 'document_count', 'qa_pair_count', 'is_public', 'allow_ai_training', 'language']
    list_filter = ['is_public', 'allow_ai_training', 'language', 'project', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'project', 'name', 'description', 'category')
        }),
        ('Configuration', {
            'fields': ('is_public', 'allow_ai_training', 'language')
        }),
        ('Statistics', {
            'fields': ('document_count', 'qa_pair_count', 'last_updated_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'knowledge_base', 'file_type', 'file_size', 'processing_status', 'chunk_count', 'created_at']
    list_filter = ['file_type', 'processing_status', 'source_type', 'knowledge_base']
    search_fields = ['title', 'file_url']
    readonly_fields = ['id', 'created_at', 'updated_at', 'processed_at']
    
    fieldsets = (
        ('Document Info', {
            'fields': ('id', 'knowledge_base', 'title', 'file_url', 'file_size', 'file_type', 'mime_type')
        }),
        ('Processing', {
            'fields': ('processing_status', 'chunk_count', 'embedding_model', 'error_message', 'processed_at')
        }),
        ('Metadata', {
            'fields': ('source_type', 'metadata'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QAPair)
class QAPairAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'knowledge_base', 'category', 'status', 'usage_count', 'helpful_count', 'not_helpful_count']
    list_filter = ['status', 'category', 'knowledge_base', 'source_type']
    search_fields = ['question', 'answer']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Q&A Content', {
            'fields': ('id', 'knowledge_base', 'question', 'answer')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Usage Statistics', {
            'fields': ('usage_count', 'helpful_count', 'not_helpful_count')
        }),
        ('Status & Source', {
            'fields': ('status', 'source_type', 'source_url')
        }),
        ('AI Data', {
            'fields': ('similar_questions', 'embeddings'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(WebsiteCrawl)
class WebsiteCrawlAdmin(admin.ModelAdmin):
    list_display = ['url', 'knowledge_base', 'status', 'max_depth', 'pages_crawled', 'pages_failed', 'is_scheduled']
    list_filter = ['status', 'is_scheduled', 'knowledge_base']
    search_fields = ['url']
    readonly_fields = ['id', 'created_at', 'updated_at', 'started_at', 'completed_at']


@admin.register(CrawledPage)
class CrawledPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'website_crawl', 'url', 'chunk_count', 'embeddings_generated']
    list_filter = ['embeddings_generated', 'website_crawl']
    search_fields = ['title', 'url', 'content']
    readonly_fields = ['id', 'created_at']


@admin.register(KnowledgeFeedback)
class KnowledgeFeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_type', 'qa_pair_preview', 'comment_preview', 'visitor_id', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['comment', 'qa_pair__question']
    readonly_fields = ['id', 'created_at']
    
    def qa_pair_preview(self, obj):
        return obj.qa_pair.question[:30] + '...' if len(obj.qa_pair.question) > 30 else obj.qa_pair.question
    qa_pair_preview.short_description = 'Q&A'
    
    def comment_preview(self, obj):
        return obj.comment[:30] + '...' if obj.comment and len(obj.comment) > 30 else (obj.comment or '-')
    comment_preview.short_description = 'Comment'
