"""
Storage API views
"""
import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from storageapp.services import StorageService

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def presign_put_url(request):
    """
    Generate presigned PUT URL for uploading files
    
    POST /api/storage/presign-put
    Body: {
        "bucket_key": "path/to/file",
        "mime_type": "application/pdf"
    }
    
    Response: {
        "upload_url": "https://...",
        "bucket_key": "path/to/file",
        "expires_in": 900
    }
    """
    bucket_key = request.data.get('bucket_key')
    mime_type = request.data.get('mime_type')
    
    if not bucket_key or not mime_type:
        return Response(
            {'error': 'bucket_key and mime_type are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate MIME type
    if mime_type not in settings.ALLOWED_MIME_TYPES:
        return Response(
            {'error': f'MIME type not allowed: {mime_type}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        upload_url = StorageService.generate_put_url(bucket_key, mime_type)
        
        logger.info(f"Generated presigned PUT URL for {bucket_key} by user {request.user.username}")
        
        return Response({
            'upload_url': upload_url,
            'bucket_key': bucket_key,
            'expires_in': settings.STORAGE_URL_EXPIRES_SECONDS,
        })
    except Exception as e:
        logger.error(f"Error generating presigned PUT URL: {e}")
        return Response(
            {'error': 'Failed to generate upload URL'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

