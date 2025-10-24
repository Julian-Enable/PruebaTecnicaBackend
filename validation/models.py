import uuid
from django.db import models
from django.contrib.auth import get_user_model
from documents.models import Document

User = get_user_model()


class ValidationFlow(models.Model):
    """Configuración de flujo de validación para un documento"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='validation_flow')
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Flujo de Validación para {self.document.name}"


class ValidationStep(models.Model):
    """Paso individual en el flujo de validación con aprobador"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(ValidationFlow, on_delete=models.CASCADE, related_name='steps')
    order = models.IntegerField()
    approver_user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['flow', 'order'],
                name='unique_flow_order'
            )
        ]
        indexes = [
            models.Index(fields=['flow', 'order']),
            models.Index(fields=['approver_user_id']),
        ]
        ordering = ['order']
    
    def __str__(self):
        return f"Step {self.order} for {self.flow.document.name}"


class ValidationInstance(models.Model):
    """Instancia en tiempo de ejecución que rastrea el progreso de validación"""
    
    STATUS_CHOICES = [
        ('P', 'Pendiente'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.OneToOneField(ValidationFlow, on_delete=models.CASCADE, related_name='instance')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    current_max_order_approved = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Validation Instance for {self.flow.document.name} - {self.get_status_display()}"  # type: ignore[attr-defined]


class ValidationAction(models.Model):
    """Acción individual de aprobación/rechazo"""
    
    ACTION_CHOICES = [
        ('APPROVE', 'Aprobar'),
        ('REJECT', 'Rechazar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instance = models.ForeignKey(ValidationInstance, on_delete=models.CASCADE, related_name='actions')
    actor_user_id = models.IntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    step_order = models.IntegerField()
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['instance', 'created_at']),
            models.Index(fields=['actor_user_id']),
        ]
    
    def __str__(self):
        return f"{self.action} at step {self.step_order} for {self.instance.flow.document.name}"

