"""
Permisos personalizados para endpoints de la API
"""
from rest_framework import permissions
from core.models import CompanyMembership


class IsCompanyMember(permissions.BasePermission):
    """
    Permiso para verificar si el usuario tiene acceso a recursos de la empresa
    """
    message = "No tienes acceso a los recursos de esta empresa."
    
    def has_permission(self, request, view):
        """Verifica si el usuario está autenticado"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Verifica si el usuario tiene acceso a la empresa relacionada con este objeto"""
        company = None
        if hasattr(obj, 'company'):
            company = obj.company
        elif hasattr(obj, 'document') and hasattr(obj.document, 'company'):
            company = obj.document.company
        
        if not company:
            return False
        
        return CompanyMembership.objects.filter(
            user=request.user,
            company=company,
            is_active=True
        ).exists()


class CanApproveDocument(permissions.BasePermission):
    """
    Permiso para verificar si el usuario puede aprobar documentos de una empresa
    """
    message = "No tienes permiso para aprobar documentos."
    
    def has_permission(self, request, view):
        """Verifica autenticación básica"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Verifica si el usuario tiene rol de aprobador"""
        company = obj.company if hasattr(obj, 'company') else obj.document.company
        
        return CompanyMembership.objects.filter(
            user=request.user,
            company=company,
            role__in=['ADMIN', 'APPROVER'],
            is_active=True
        ).exists()
