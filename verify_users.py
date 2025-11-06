"""
Script para verificar usuarios en Railway
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpdocs.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import CompanyMembership

User = get_user_model()

print("\n" + "="*60)
print("USUARIOS EN LA BASE DE DATOS DE RAILWAY")
print("="*60 + "\n")

users = User.objects.all()

if not users.exists():
    print("❌ NO HAY USUARIOS EN LA BASE DE DATOS")
else:
    for user in users:
        print(f"🔹 Username: {user.username}")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Activo: {'✅ Sí' if user.is_active else '❌ No'}")
        print(f"   Staff: {'✅ Sí' if user.is_staff else '❌ No'}")
        print(f"   Superuser: {'✅ Sí' if user.is_superuser else '❌ No'}")
        
        # Verificar membresías
        memberships = CompanyMembership.objects.filter(user=user)
        if memberships.exists():
            print(f"   Empresas: {memberships.count()}")
            for m in memberships:
                print(f"      - {m.company.name} (Activo: {m.is_active})")
        else:
            print("   Empresas: Ninguna")
        
        print()

print("="*60)
print(f"Total de usuarios: {users.count()}")
print("="*60)
