"""
Vistas de API para documentos
"""
import logging
from typing import TYPE_CHECKING
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.conf import settings

if TYPE_CHECKING:
    from rest_framework.request import Request

from documents.models import Document, DocumentDownloadAudit, DocumentStateAudit
from documents.serializers import (
    DocumentCreateSerializer,
    DocumentSerializer,
    DocumentDownloadSerializer,
    ValidationActionSerializer,
    DocumentStateAuditSerializer,
)
from validation.models import ValidationFlow, ValidationStep, ValidationInstance
from validation.services import ValidationService
from storageapp.services import StorageService
from core.models import Company
from core.permissions import IsCompanyMember

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de documentos
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]
    
    def get_queryset(self):
        """Filtra documentos por membresía de empresa y opcionalmente por validation_status"""
        user = self.request.user  # type: ignore[attr-defined]
        company_ids = user.company_memberships.filter(is_active=True).values_list('company_id', flat=True)  # type: ignore[attr-defined]
        queryset = Document.objects.filter(company_id__in=company_ids)
        
        # Filtrar por validation_status si se proporciona en query params
        validation_status = self.request.query_params.get('validation_status')  # type: ignore[attr-defined]
        if validation_status:
            queryset = queryset.filter(validation_status=validation_status)
        
        return queryset
    
    @transaction.atomic
    def create(self, request):
        """
        Crea un nuevo documento con flujo de validación opcional.
        Valida que el objeto existe en el bucket antes de crear el registro en BD.
        """
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data  # type: ignore[assignment]
        company_id = data['company_id']  # type: ignore[index]
        entity = data['entity']  # type: ignore[index]
        doc_data = data['document']  # type: ignore[index]
        validation_flow_data = data.get('validation_flow')  # type: ignore[union-attr]
        
        try:
            company = Company.objects.get(id=company_id, is_active=True)
        except Company.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada o inactiva'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not request.user.company_memberships.filter(company=company, is_active=True).exists():
            return Response(
                {'error': 'No tienes acceso a esta empresa'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        bucket_key = doc_data['bucket_key']
        
        # CRÍTICO: Verificar que el objeto existe en el bucket (solo si storage está configurado)
        if settings.STORAGE_PROVIDER and settings.STORAGE_PROVIDER != 'LOCAL':
            logger.info(f"Verificando que el objeto existe en el bucket: {bucket_key}")
            if not StorageService.verify_object_exists(bucket_key):
                return Response(
                    {'error': f'Objeto no encontrado en el bucket: {bucket_key}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            logger.info(f"DEMO MODE: Saltando verificación de storage para {bucket_key}")
        
        
        document = Document.objects.create(
            company=company,
            name=doc_data['name'],
            mime_type=doc_data['mime_type'],
            size_bytes=doc_data['size_bytes'],
            bucket_key=bucket_key,
            bucket_provider=settings.STORAGE_PROVIDER,
            entity_type=entity['entity_type'],
            entity_id=entity['entity_id'],
            created_by=request.user,
            updated_by=request.user,
        )
        
        if validation_flow_data and validation_flow_data.get('enabled'):
            steps_data = validation_flow_data.get('steps', [])
            
            if steps_data:
                # Set document to pending validation
                document.validation_status = 'P'
                document.save()
                
                flow = ValidationFlow.objects.create(
                    document=document,
                    enabled=True
                )
                
                for step_data in steps_data:
                    ValidationStep.objects.create(
                        flow=flow,
                        order=step_data['order'],
                        approver_user_id=step_data['approver_user_id']
                    )
                
                ValidationInstance.objects.create(
                    flow=flow,
                    status='P',
                    current_max_order_approved=None
                )
                
                logger.info(f"Flujo de validación creado con {len(steps_data)} pasos para documento {document.id}")
        
        DocumentStateAudit.objects.create(
            document=document,
            action='CREATE',
            actor=request.user,
            from_status=None,
            to_status=document.validation_status
        )
        
        logger.info(f"Documento {document.id} creado exitosamente por usuario {request.user.username}")
        
        response_serializer = DocumentSerializer(document)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        """Genera URL prefirmada de descarga para documento"""
        document = self.get_object()
        
        try:
            # Si STORAGE_PROVIDER está configurado, usar S3/GCS real
            if settings.STORAGE_PROVIDER and settings.STORAGE_PROVIDER != 'LOCAL':
                download_url = StorageService.generate_get_url(document.bucket_key)
                logger.info(f"URL de descarga generada desde {settings.STORAGE_PROVIDER} para documento {document.id}")
            else:
                # Generar URL mock para demo sin storage configurado
                download_url = f"https://storage-demo.example.com/{document.bucket_key}?expires=900"
                logger.info(f"URL de descarga MOCK generada para documento {document.id}")
        except Exception as e:
            logger.error(f"Error generando URL de descarga: {e}")
            return Response(
                {'error': 'Error al generar URL de descarga'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        DocumentDownloadAudit.objects.create(
            document=document,
            actor=request.user,
        )
        
        logger.info(f"URL de descarga generada para documento {document.id} por usuario {request.user.username}")
        
        serializer = DocumentDownloadSerializer(data={
            'download_url': download_url,
            'validation_status': document.validation_status,
            'document_name': document.name,
            'mime_type': document.mime_type,
            'size_bytes': document.size_bytes,
        })
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """Aprueba documento en el paso de validación del actor"""
        document = self.get_object()
        
        serializer = ValidationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # CORRECCIÓN: Usar el usuario autenticado, no el del body
        actor_user_id = request.user.id  # Tomar del token JWT
        reason = serializer.validated_data.get('reason')
        
        if not request.user.company_memberships.filter(
            company=document.company,
            is_active=True
        ).exists():
            return Response(
                {'error': 'No tienes acceso a esta empresa'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            updated_document = ValidationService.approve_document(
                document_id=str(document.id),
                actor_user_id=actor_user_id,
                reason=reason
            )
            
            logger.info(f"Documento {document.id} aprobado por {actor_user_id}")
            
            serializer = DocumentSerializer(updated_document)
            return Response(serializer.data)
            
        except ValueError as e:
            logger.warning(f"Aprobación falló: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """Rechaza documento"""
        document = self.get_object()
        
        serializer = ValidationActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # CORRECCIÓN: Usar el usuario autenticado, no el del body
        actor_user_id = request.user.id  # Tomar del token JWT
        reason = serializer.validated_data.get('reason')
        
        if not request.user.company_memberships.filter(
            company=document.company,
            is_active=True
        ).exists():
            return Response(
                {'error': 'No tienes acceso a esta empresa'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            updated_document = ValidationService.reject_document(
                document_id=str(document.id),
                actor_user_id=actor_user_id,
                reason=reason
            )
            
            logger.info(f"Documento {document.id} rechazado por {actor_user_id}")
            
            serializer = DocumentSerializer(updated_document)
            return Response(serializer.data)
            
        except ValueError as e:
            logger.warning(f"Rechazo falló: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'], url_path='audit')
    def audit(self, request, pk=None):
        """Obtiene historial de auditoría para documento"""
        document = self.get_object()
        
        audits = DocumentStateAudit.objects.filter(document=document).order_by('-created_at')
        serializer = DocumentStateAuditSerializer(audits, many=True)
        
        return Response(serializer.data)

