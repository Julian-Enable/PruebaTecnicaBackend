"""
Serializadores para aplicación de documentos
"""
import uuid
from rest_framework import serializers
from django.conf import settings
from documents.models import Document, DocumentDownloadAudit, DocumentStateAudit
from validation.models import ValidationFlow, ValidationStep


class ValidationStepSerializer(serializers.Serializer):
    """Serializador para paso de validación en creación de documento"""
    order = serializers.IntegerField(min_value=1)
    approver_user_id = serializers.IntegerField()
    
    def validate_order(self, value):
        """Asegura que el orden es positivo"""
        if value < 1:
            raise serializers.ValidationError("El orden debe ser al menos 1")
        return value


class ValidationFlowCreateSerializer(serializers.Serializer):
    """Serializador para configuración de flujo de validación"""
    enabled = serializers.BooleanField(default=True)  # type: ignore[call-arg]
    steps = ValidationStepSerializer(many=True, required=False)
    
    def validate_steps(self, value):
        """Valida que los pasos estén ordenados correctamente"""
        if not value:
            return value
        
        orders = [step['order'] for step in value]
        # Verifica duplicados
        if len(orders) != len(set(orders)):
            raise serializers.ValidationError("Se encontraron órdenes de paso duplicados")
        
        # Verifica espacios en blanco (opcional, puede ser removido si se permiten espacios)
        sorted_orders = sorted(orders)
        expected_orders = list(range(1, len(orders) + 1))
        if sorted_orders != expected_orders:
            raise serializers.ValidationError("Los órdenes de paso deben ser secuenciales comenzando desde 1")
        
        return value


class DocumentMetadataSerializer(serializers.Serializer):
    """Serializador para metadatos de documento en solicitud de creación"""
    name = serializers.CharField(max_length=255)
    mime_type = serializers.CharField(max_length=100)
    size_bytes = serializers.IntegerField(min_value=1)
    bucket_key = serializers.CharField(max_length=500)
    
    def validate_mime_type(self, value):
        """Valida que el tipo MIME es permitido"""
        allowed = settings.ALLOWED_MIME_TYPES
        if value not in allowed:
            raise serializers.ValidationError(
                f"Tipo MIME '{value}' no permitido. Tipos permitidos: {', '.join(allowed)}"
            )
        return value
    
    def validate_size_bytes(self, value):
        """Valida el tamaño del archivo"""
        max_size = settings.MAX_UPLOAD_BYTES
        if value > max_size:
            raise serializers.ValidationError(
                f"Tamaño de archivo {value} excede el tamaño máximo permitido {max_size} bytes"
            )
        return value


class EntityReferenceSerializer(serializers.Serializer):
    """Serializador para referencia de entidad"""
    entity_type = serializers.CharField(max_length=100)
    entity_id = serializers.CharField(max_length=255)  # Soporta placas, códigos, UUIDs, etc.


class DocumentCreateSerializer(serializers.Serializer):
    """Serializador para solicitud de creación de documento"""
    company_id = serializers.UUIDField()
    entity = EntityReferenceSerializer()
    document = DocumentMetadataSerializer()
    validation_flow = ValidationFlowCreateSerializer(required=False)
    
    def validate(self, data):
        """Validación entre campos"""
        validation_flow = data.get('validation_flow')
        if validation_flow and validation_flow.get('enabled') and not validation_flow.get('steps'):
            raise serializers.ValidationError(
                "El flujo de validación está habilitado pero no se proporcionaron pasos"
            )
        return data


class DocumentSerializer(serializers.ModelSerializer):
    """Serializador para respuestas de documento"""
    company_id = serializers.UUIDField(source='company.id', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id',
            'company_id',
            'company_name',
            'name',
            'mime_type',
            'size_bytes',
            'bucket_key',
            'bucket_provider',
            'hash_hex',
            'validation_status',
            'entity_type',
            'entity_id',
            'created_at',
            'updated_at',
            'created_by_username',
        ]
        read_only_fields = fields


class DocumentDownloadSerializer(serializers.Serializer):
    """Serializador para respuesta de descarga de documento"""
    download_url = serializers.URLField()
    validation_status = serializers.CharField(allow_null=True)
    document_name = serializers.CharField()
    mime_type = serializers.CharField()
    size_bytes = serializers.IntegerField()


class ValidationActionSerializer(serializers.Serializer):
    """Serializador para acciones de aprobación/rechazo"""
    # actor_user_id ya no es necesario - se toma del token JWT (request.user)
    reason = serializers.CharField(required=False, allow_blank=True)


class DocumentStateAuditSerializer(serializers.ModelSerializer):
    """Serializador para auditoría de estado de documento"""
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    
    class Meta:
        model = DocumentStateAudit
        fields = [
            'id',
            'action',
            'actor_username',
            'reason',
            'from_status',
            'to_status',
            'created_at',
        ]
        read_only_fields = fields
