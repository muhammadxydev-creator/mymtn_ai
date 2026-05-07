from rest_framework import serializers
from nlp_service.models import (
    IntentCategory, Entity, NLPModel, 
    TrainingSample, NLPPredictionLog
)


class IntentCategorySerializer(serializers.ModelSerializer):
    """Serializer for IntentCategory model."""
    
    intent_code_display = serializers.CharField(
        source='get_intent_code_display', 
        read_only=True
    )
    
    class Meta:
        model = IntentCategory
        fields = [
            'id', 'project', 'name', 'intent_code', 'intent_code_display',
            'description', 'training_samples_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IntentCategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating intent categories."""
    
    class Meta:
        model = IntentCategory
        fields = [
            'project', 'name', 'intent_code', 'description', 'is_active'
        ]


class EntitySerializer(serializers.ModelSerializer):
    """Serializer for Entity model."""
    
    entity_type_display = serializers.CharField(
        source='get_entity_type_display', 
        read_only=True
    )
    
    class Meta:
        model = Entity
        fields = [
            'id', 'project', 'name', 'entity_type', 'entity_type_display',
            'description', 'extraction_pattern', 'is_required',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EntityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating entities."""
    
    class Meta:
        model = Entity
        fields = [
            'project', 'name', 'entity_type', 'description',
            'extraction_pattern', 'is_required'
        ]


class NLPModelSerializer(serializers.ModelSerializer):
    """Serializer for NLPModel model."""
    
    model_type_display = serializers.CharField(
        source='get_model_type_display', 
        read_only=True
    )
    
    class Meta:
        model = NLPModel
        fields = [
            'id', 'project', 'name', 'model_type', 'model_type_display',
            'model_path', 'model_version', 'base_model', 'accuracy_score',
            'is_default', 'is_active', 'config', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NLPModelCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating NLP models."""
    
    class Meta:
        model = NLPModel
        fields = [
            'project', 'name', 'model_type', 'model_path', 'model_version',
            'base_model', 'is_default', 'is_active', 'config'
        ]


class TrainingSampleSerializer(serializers.ModelSerializer):
    """Serializer for TrainingSample model."""
    
    intent_category_name = serializers.CharField(
        source='intent_category.name', 
        read_only=True
    )
    validator_username = serializers.CharField(
        source='validated_by.username', 
        read_only=True
    )
    
    class Meta:
        model = TrainingSample
        fields = [
            'id', 'intent_category', 'intent_category_name', 'text',
            'language', 'entities', 'is_validated', 'validator_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TrainingSampleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating training samples."""
    
    class Meta:
        model = TrainingSample
        fields = [
            'intent_category', 'text', 'language', 'entities'
        ]


class TrainingSampleBulkCreateSerializer(serializers.Serializer):
    """Serializer for bulk creating training samples."""
    
    intent_category_id = serializers.UUIDField()
    samples = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


class NLPPredictionLogSerializer(serializers.ModelSerializer):
    """Serializer for NLPPredictionLog model."""
    
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = NLPPredictionLog
        fields = [
            'id', 'project', 'project_name', 'input_text',
            'detected_language', 'predicted_intent', 'confidence_score',
            'extracted_entities', 'processing_time_ms', 'model_used',
            'is_correct', 'corrected_intent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NLPAnalysisRequestSerializer(serializers.Serializer):
    """Serializer for NLP analysis requests."""
    
    text = serializers.CharField(max_length=2000)
    language = serializers.CharField(max_length=10, required=False, default='en')
    visitor_id = serializers.UUIDField(required=False)
    session_id = serializers.UUIDField(required=False)
