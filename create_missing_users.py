"""
Crear usuarios faltantes en Railway
Ejecutar con: railway run python create_missing_users.py
"""
import os
import django

# No necesitamos configurar Django localmente
# Railway run lo hará automáticamente

from django.contrib.auth import get_user_model
from core.models import Company, CompanyMembership

User = get_user_model()

def create_users():
    # Obtener o crear la empresa
    company, _ = Company.objects.get_or_create(
        name="Empresa Demo S.A.",
        defaults={'id': '9da4abe9-57c7-4d76-ad5c-5e01d554f2c5'}
    )
    
    print(f"✅ Empresa: {company.name} ({company.id})")
    
    # Usuarios a crear
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'sebastian',
            'email': 'sebastian@example.com',
            'first_name': 'Sebastian',
            'last_name': 'Rodriguez',
            'password': 'admin123',
        },
        {
            'username': 'camilo',
            'email': 'camilo@example.com',
            'first_name': 'Camilo',
            'last_name': 'Martinez',
            'password': 'admin123',
        },
        {
            'username': 'juan',
            'email': 'juan@example.com',
            'first_name': 'Juan',
            'last_name': 'Gomez',
            'password': 'admin123',
        },
    ]
    
    created_users = []
    
    for user_data in users_data:
        username = user_data['username']
        
        # Verificar si ya existe
        user = User.objects.filter(username=username).first()
        
        if user:
            print(f"⚠️  Usuario '{username}' ya existe (ID: {user.id})")
            # Actualizar password por si acaso
            user.set_password(user_data['password'])
            user.is_active = True
            user.save()
            print(f"   ✅ Password actualizado y usuario activado")
            created_users.append(user)
        else:
            # Crear nuevo usuario
            password = user_data.pop('password')
            user = User.objects.create_user(password=password, **user_data)
            print(f"✅ Usuario '{username}' creado (ID: {user.id})")
            created_users.append(user)
        
        # Crear membresía si no existe
        membership, created = CompanyMembership.objects.get_or_create(
            user=user,
            company=company,
            defaults={'is_active': True}
        )
        
        if created:
            print(f"   ✅ Membresía creada para {company.name}")
        else:
            if not membership.is_active:
                membership.is_active = True
                membership.save()
                print(f"   ✅ Membresía activada para {company.name}")
            else:
                print(f"   ℹ️  Ya tiene membresía activa")
        
        print()
    
    print("=" * 60)
    print(f"✅ Total usuarios procesados: {len(created_users)}")
    print("=" * 60)
    
    # Mostrar resumen
    print("\n📋 RESUMEN DE USUARIOS:\n")
    for user in User.objects.all():
        memberships = CompanyMembership.objects.filter(user=user, is_active=True).count()
        print(f"  {user.id}: {user.username} - Activo: {user.is_active} - Empresas: {memberships}")

if __name__ == '__main__':
    create_users()
