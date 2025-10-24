"""
Script para crear una empresa de prueba en Railway
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpdocs.settings')
django.setup()

from core.models import Company

# Crear empresa de prueba
company, created = Company.objects.get_or_create(
    name='Empresa Demo S.A.',
    defaults={'is_active': True}
)

print("=" * 60)
if created:
    print("✅ Empresa creada exitosamente!")
else:
    print("⚠️  La empresa ya existía")
    
print("=" * 60)
print(f"ID (UUID): {company.id}")
print(f"Nombre: {company.name}")
print(f"Activa: {company.is_active}")
print("=" * 60)
print("\n📋 COPIA ESTE UUID para usar en Postman como company_id:")
print(f"\n   {company.id}\n")
print("=" * 60)
