from django.contrib import admin
from .models import IntentCategory, Entity, NLPModel, TrainingSample, NLPPredictionLog


@admin.register(IntentCategory)
class IntentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'intent_code', 'project', 'training_samples_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'project', 'intent_code']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'project', 'is_required', 'created_at']
    list_filter = ['entity_type', 'is_required', 'project']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(NLPModel)
class NLPModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'base_model', 'model_version', 'accuracy_score', 'is_default', 'is_active']
    list_filter = ['model_type', 'base_model', 'is_default', 'is_active', 'project']
    search_fields = ['name', 'model_path']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(TrainingSample)
class TrainingSampleAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'intent_category', 'language', 'is_validated', 'validated_by', 'created_at']
    list_filter = ['language', 'is_validated', 'intent_category']
    search_fields = ['text']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(NLPPredictionLog)
class NLPPredictionLogAdmin(admin.ModelAdmin):
    list_display = ['predicted_intent', 'confidence_score', 'detected_language', 'processing_time_ms', 'is_correct', 'created_at']
    list_filter = ['predicted_intent', 'detected_language', 'is_correct', 'project']
    search_fields = ['input_text', 'predicted_intent']
    readonly_fields = ['id', 'created_at']
    list_editable = ['is_correct']
