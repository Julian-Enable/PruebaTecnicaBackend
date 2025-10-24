import uuid
from django.db import models
from django.contrib.auth import get_user_model
from core.models import Company, AuditMixin

User = get_user_model()


class Document(AuditMixin):
    """Modelo de documento con referencia a storage y estado de validación"""
    
    VALIDATION_STATUS_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ]
    
    BUCKET_PROVIDER_CHOICES = [
        ('S3', 'Amazon S3'),
        ('GCS', 'Google Cloud Storage'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField()
    bucket_key = models.CharField(max_length=500)
    bucket_provider = models.CharField(max_length=10, choices=BUCKET_PROVIDER_CHOICES)
    hash_hex = models.CharField(max_length=128, null=True, blank=True)
    validation_status = models.CharField(
        max_length=1,
        choices=VALIDATION_STATUS_CHOICES,
        null=True,
        blank=True
    )
    
    # Entity reference (generic relationship via fields)
    # Referencia a entidad (relación genérica via campos)
    entity_type = models.CharField(max_length=100)
    entity_id = models.UUIDField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'bucket_key'],
                name='unique_company_bucket_key'
            )
        ]
        indexes = [
            models.Index(fields=['company', 'entity_type', 'entity_id']),
            models.Index(fields=['validation_status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.company.name})"


class DocumentDownloadAudit(models.Model):
    """Registro de auditoría para descargas de documentos"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='download_audits')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='document_downloads')
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document', 'created_at']),
        ]
    
    def __str__(self):
        return f"Download of {self.document.name} by {self.actor.username if self.actor else 'Unknown'}"


class DocumentStateAudit(models.Model):
    """Registro de auditoría para cambios de estado de documentos"""
    
    ACTION_CHOICES = [
        ('CREATE', 'Crear'),
        ('APPROVE', 'Aprobar'),
        ('REJECT', 'Rechazar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='state_audits')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='document_state_changes')
    reason = models.TextField(null=True, blank=True)
    from_status = models.CharField(max_length=1, null=True, blank=True)
    to_status = models.CharField(max_length=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['document', 'created_at']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.action} on {self.document.name} by {self.actor.username if self.actor else 'Unknown'}"

