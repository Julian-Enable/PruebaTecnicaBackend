"""
Servicio de validación para flujos de aprobación jerárquicos
"""
import logging
from typing import Optional, TYPE_CHECKING
from django.db import transaction
from django.contrib.auth import get_user_model
from documents.models import Document, DocumentStateAudit
from validation.models import ValidationFlow, ValidationStep, ValidationInstance, ValidationAction

if TYPE_CHECKING:
    from typing import Any

User = get_user_model()
logger = logging.getLogger(__name__)


class ValidationService:
    """Servicio para gestionar flujos de validación de documentos"""
    
    @staticmethod
    @transaction.atomic
    def approve_document(document_id: str, actor_user_id: str, reason: Optional[str] = None) -> Document:
        """
        Aprueba un documento en el nivel de paso del actor.
        Aprueba automáticamente todos los pasos pendientes de orden inferior.
        Si el actor está en el orden más alto, el documento se aprueba completamente.
        
        Args:
            document_id: UUID del documento
            actor_user_id: ID del usuario que aprueba
            reason: Razón opcional para la aprobación
            
        Returns:
            Instancia de Document actualizada
            
        Raises:
            ValueError: Si se violan las reglas de validación
        """
        try:
            document = Document.objects.select_for_update().get(id=document_id)
        except Document.DoesNotExist:
            raise ValueError(f"Documento {document_id} no encontrado")
        
        if not hasattr(document, 'validation_flow'):
            raise ValueError("El documento no tiene un flujo de validación")
        
        flow = document.validation_flow  # type: ignore[attr-defined]
        if not flow.enabled:
            raise ValueError("El flujo de validación no está habilitado")
        
        # Get validation instance
        try:
            instance = flow.instance
        except ValidationInstance.DoesNotExist:
            raise ValueError("Instancia de validación no encontrada")
        
        if instance.status == 'R':
            raise ValueError("No se puede aprobar: el documento está rechazado (estado terminal)")
        
        if instance.status == 'A':
            raise ValueError("El documento ya está completamente aprobado")
        
        actor_step = ValidationStep.objects.filter(
            flow=flow,
            approver_user_id=actor_user_id
        ).first()
        
        if not actor_step:
            raise ValueError(f"El usuario {actor_user_id} no es aprobador en este flujo de validación")
        
        existing_approval = ValidationAction.objects.filter(
            instance=instance,
            step_order=actor_step.order,
            action='APPROVE'
        ).exists()
        
        if existing_approval:
            logger.warning(f"Paso {actor_step.order} ya aprobado para documento {document_id}")
            return document
        
        # Get all steps
        all_steps = list(ValidationStep.objects.filter(flow=flow).order_by('order'))
        max_order = max(step.order for step in all_steps)
        
        # Registrar aprobaciones en cascada para niveles inferiores
        # Si el actor aprueba en orden K, auto-aprobar todos los órdenes < K que estén pendientes
        if actor_step.order > 1:
            lower_steps = [s for s in all_steps if s.order < actor_step.order]
            for lower_step in lower_steps:
                # Verificar si ya fue aprobado
                already_approved = ValidationAction.objects.filter(
                    instance=instance,
                    step_order=lower_step.order,
                    action='APPROVE'
                ).exists()
                
                if not already_approved:
                    # Auto-aprobar este nivel
                    ValidationAction.objects.create(
                        instance=instance,
                        actor_user_id=actor_user_id,
                        action='APPROVE',
                        step_order=lower_step.order,
                        reason=f"Auto-aprobado por cascada (aprobador de nivel {actor_step.order})"
                    )
                    
                    # Registrar en auditoría
                    DocumentStateAudit.objects.create(
                        document=document,
                        action='APPROVE',
                        actor_id=actor_user_id,
                        reason=f"Auto-aprobado por cascada desde nivel {actor_step.order}",
                        from_status='P',
                        to_status='P',  # Sigue pendiente hasta que todos aprueben
                        validation_level=lower_step.order
                    )
                    
                    logger.info(
                        f"Nivel {lower_step.order} auto-aprobado por cascada "
                        f"por usuario {actor_user_id} (nivel {actor_step.order})"
                    )
        
        # Record approval action for the actual approver's level
        ValidationAction.objects.create(
            instance=instance,
            actor_user_id=actor_user_id,
            action='APPROVE',
            step_order=actor_step.order,
            reason=reason
        )
        
        # Registrar aprobación del nivel actual en auditoría
        DocumentStateAudit.objects.create(
            document=document,
            action='APPROVE',
            actor_id=actor_user_id,
            reason=reason or f"Aprobado en nivel {actor_step.order}",
            from_status='P',
            to_status='P' if actor_step.order < max_order else 'A',
            validation_level=actor_step.order
        )
        
        # Update current_max_order_approved
        current_max = instance.current_max_order_approved or 0
        if actor_step.order > current_max:
            instance.current_max_order_approved = actor_step.order
        
        # Check if this is the highest order step
        if actor_step.order == max_order:
            # Document fully approved
            old_status = document.validation_status
            document.validation_status = 'A'
            instance.status = 'A'
            document.save()
            instance.save()
            
            # Registrar cambio de estado final del documento en auditoría
            DocumentStateAudit.objects.create(
                document=document,
                action='APPROVE',
                actor_id=actor_user_id,
                reason=f"Documento completamente aprobado en nivel {actor_step.order}",
                from_status=old_status,
                to_status='A',
                validation_level=actor_step.order
            )
            
            logger.info(
                f"Documento {document_id} completamente aprobado por usuario {actor_user_id} "
                f"en paso {actor_step.order}"
            )
        else:
            # Aprobación parcial
            instance.save()
            logger.info(
                f"Documento {document_id} aprobado en paso {actor_step.order} "
                f"por usuario {actor_user_id}. Quedan niveles pendientes."
            )
        
        return document
    
    @staticmethod
    @transaction.atomic
    def reject_document(document_id: str, actor_user_id: str, reason: Optional[str] = None) -> Document:
        """
        Rechaza un documento. Cualquier rechazo pone el documento en estado terminal Rechazado.
        
        Args:
            document_id: UUID del documento
            actor_user_id: UUID del usuario que rechaza
            reason: Razón opcional del rechazo
            
        Returns:
            Instancia de Document actualizada
            
        Raises:
            ValueError: Si se violan las reglas de validación
        """
        try:
            document = Document.objects.select_for_update().get(id=document_id)
        except Document.DoesNotExist:
            raise ValueError(f"Document {document_id} not found")
        
        if not hasattr(document, 'validation_flow'):
            raise ValueError("Document does not have a validation flow")
        
        flow = document.validation_flow  # type: ignore[attr-defined]
        if not flow.enabled:
            raise ValueError("Validation flow is not enabled")
        
        # Get validation instance
        try:
            instance = flow.instance
        except ValidationInstance.DoesNotExist:
            raise ValueError("Validation instance not found")
        
        # Verifica si ya está en estado terminal
        if instance.status == 'R':
            raise ValueError("El documento ya está rechazado")
        
        if instance.status == 'A':
            raise ValueError("No se puede rechazar: el documento ya está completamente aprobado")
        
        # Find the step for this actor
        actor_step = ValidationStep.objects.filter(
            flow=flow,
            approver_user_id=actor_user_id
        ).first()
        
        if not actor_step:
            raise ValueError(f"User {actor_user_id} is not an approver in this validation flow")
        
        # Registra acción de rechazo
        ValidationAction.objects.create(
            instance=instance,
            actor_user_id=actor_user_id,
            action='REJECT',
            step_order=actor_step.order,
            reason=reason
        )
        
        # Actualiza documento e instancia a estado rechazado (terminal)
        old_status = document.validation_status
        document.validation_status = 'R'
        instance.status = 'R'
        
        document.save()
        instance.save()
        
        # Audita cambio de estado
        DocumentStateAudit.objects.create(
            document=document,
            action='REJECT',
            actor_id=actor_user_id,
            reason=reason,
            from_status=old_status,
            to_status='R'
        )
        
        logger.info(
            f"Documento {document_id} rechazado por usuario {actor_user_id} "
            f"en paso {actor_step.order}. Razón: {reason}"
        )
        
        return document
    
    @staticmethod
    def get_validation_status(document_id: str) -> dict:
        """
        Obtiene el estado de validación actual y el historial de un documento
        
        Returns:
            Diccionario con detalles de validación
        """
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise ValueError(f"Document {document_id} not found")
        
        if not hasattr(document, 'validation_flow'):
            return {
                'has_validation': False,
                'status': None,
            }
        
        flow = document.validation_flow  # type: ignore[attr-defined]
        instance = flow.instance
        
        steps = list(ValidationStep.objects.filter(flow=flow).order_by('order'))
        actions = list(ValidationAction.objects.filter(instance=instance).order_by('created_at'))
        
        return {
            'has_validation': True,
            'enabled': flow.enabled,
            'status': instance.status,
            'current_max_order_approved': instance.current_max_order_approved,
            'total_steps': len(steps),
            'steps': [
                {
                    'order': step.order,
                    'approver_user_id': str(step.approver_user_id),
                }
                for step in steps
            ],
            'actions': [
                {
                    'action': action.action,
                    'actor_user_id': str(action.actor_user_id),
                    'step_order': action.step_order,
                    'reason': action.reason,
                    'created_at': action.created_at.isoformat(),
                }
                for action in actions
            ],
        }
