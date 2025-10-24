"""
Servicio de almacenamiento con soporte para S3 y GCS
Proporciona URLs prefirmadas y verificación de objetos
"""
import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional, Dict

import boto3
from botocore.exceptions import ClientError
from google.cloud import storage as gcs_storage
from google.cloud.exceptions import GoogleCloudError
from django.conf import settings

logger = logging.getLogger(__name__)


class StorageProvider(ABC):
    """Clase base abstracta para proveedores de almacenamiento"""
    
    @abstractmethod
    def generate_put_url(self, bucket_key: str, mime_type: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para carga"""
        pass
    
    @abstractmethod
    def generate_get_url(self, bucket_key: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para descarga"""
        pass
    
    @abstractmethod
    def head_object(self, bucket_key: str) -> Optional[Dict]:
        """Verifica que el objeto existe y obtiene metadatos"""
        pass


class S3StorageProvider(StorageProvider):
    """Proveedor de almacenamiento Amazon S3"""
    
    def __init__(self):
        self.bucket_name = settings.STORAGE_BUCKET_NAME
        self.region = settings.STORAGE_REGION
        self.client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
    
    def generate_put_url(self, bucket_key: str, mime_type: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para operación PUT"""
        try:
            url = self.client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': bucket_key,
                    'ContentType': mime_type,
                },
                ExpiresIn=expires_seconds,
            )
            logger.info(f"URL PUT S3 generada para {bucket_key}")
            return url
        except ClientError as e:
            logger.error(f"Error generando URL PUT S3: {e}")
            raise
    
    def generate_get_url(self, bucket_key: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para operación GET"""
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': bucket_key,
                },
                ExpiresIn=expires_seconds,
            )
            logger.info(f"URL GET S3 generada para {bucket_key}")
            return url
        except ClientError as e:
            logger.error(f"Error generando URL GET S3: {e}")
            raise
    
    def head_object(self, bucket_key: str) -> Optional[Dict]:
        """Verifica que el objeto existe y retorna metadatos"""
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=bucket_key)
            logger.info(f"Objeto S3 existe: {bucket_key}")
            return {
                'content_type': response.get('ContentType'),
                'size_bytes': response.get('ContentLength'),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag', '').strip('"'),
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.warning(f"Objeto S3 no encontrado: {bucket_key}")
                return None
            logger.error(f"Error verificando objeto S3: {e}")
            raise


class GCSStorageProvider(StorageProvider):
    """Proveedor de Google Cloud Storage"""
    
    def __init__(self):
        self.bucket_name = settings.STORAGE_BUCKET_NAME
        self.project_id = settings.GCS_PROJECT_ID
        
        # Inicializa cliente con credenciales si se proporcionan
        if settings.GCS_CREDENTIALS_PATH:
            self.client = gcs_storage.Client.from_service_account_json(
                settings.GCS_CREDENTIALS_PATH,
                project=self.project_id
            )
        else:
            self.client = gcs_storage.Client(project=self.project_id)
        
        self.bucket = self.client.bucket(self.bucket_name)
    
    def generate_put_url(self, bucket_key: str, mime_type: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para operación PUT"""
        try:
            blob = self.bucket.blob(bucket_key)
            url = blob.generate_signed_url(
                version='v4',
                expiration=timedelta(seconds=expires_seconds),
                method='PUT',
                content_type=mime_type,
            )
            logger.info(f"URL PUT GCS generada para {bucket_key}")
            return url
        except GoogleCloudError as e:
            logger.error(f"Error generando URL PUT GCS: {e}")
            raise
    
    def generate_get_url(self, bucket_key: str, expires_seconds: int) -> str:
        """Genera URL prefirmada para operación GET"""
        try:
            blob = self.bucket.blob(bucket_key)
            url = blob.generate_signed_url(
                version='v4',
                expiration=timedelta(seconds=expires_seconds),
                method='GET',
            )
            logger.info(f"URL GET GCS generada para {bucket_key}")
            return url
        except GoogleCloudError as e:
            logger.error(f"Error generando URL GET GCS: {e}")
            raise
    
    def head_object(self, bucket_key: str) -> Optional[Dict]:
        """Verifica que el objeto existe y retorna metadatos"""
        try:
            blob = self.bucket.blob(bucket_key)
            if not blob.exists():
                logger.warning(f"Objeto GCS no encontrado: {bucket_key}")
                return None
            
            blob.reload()
            logger.info(f"Objeto GCS existe: {bucket_key}")
            return {
                'content_type': blob.content_type,
                'size_bytes': blob.size,
                'last_modified': blob.updated,
                'etag': blob.etag,
            }
        except GoogleCloudError as e:
            logger.error(f"Error verificando objeto GCS: {e}")
            raise


class StorageService:
    """Servicio principal de almacenamiento que delega a implementaciones de proveedores"""
    
    _provider: Optional[StorageProvider] = None
    
    @classmethod
    def get_provider(cls) -> StorageProvider:
        """Obtiene o crea instancia de proveedor de almacenamiento"""
        if cls._provider is None:
            provider_type = settings.STORAGE_PROVIDER
            if provider_type == 'S3':
                cls._provider = S3StorageProvider()
            elif provider_type == 'GCS':
                cls._provider = GCSStorageProvider()
            else:
                raise ValueError(f"Proveedor de almacenamiento no soportado: {provider_type}")
        return cls._provider
    
    @classmethod
    def generate_put_url(cls, bucket_key: str, mime_type: str, expires_seconds: Optional[int] = None) -> str:
        """Genera URL prefirmada para carga"""
        expires = expires_seconds if expires_seconds is not None else settings.STORAGE_URL_EXPIRES_SECONDS
        return cls.get_provider().generate_put_url(bucket_key, mime_type, expires)
    
    @classmethod
    def generate_get_url(cls, bucket_key: str, expires_seconds: Optional[int] = None) -> str:
        """Genera URL prefirmada para descarga"""
        expires = expires_seconds if expires_seconds is not None else settings.STORAGE_URL_EXPIRES_SECONDS
        return cls.get_provider().generate_get_url(bucket_key, expires)
    
    @classmethod
    def head_object(cls, bucket_key: str) -> Optional[Dict]:
        """Verifica que el objeto existe y obtiene metadatos"""
        return cls.get_provider().head_object(bucket_key)
    
    @classmethod
    def verify_object_exists(cls, bucket_key: str) -> bool:
        """Verificación simple de existencia de objeto"""
        metadata = cls.head_object(bucket_key)
        return metadata is not None
