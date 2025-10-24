"""
Script para crear superusuario - Se ejecuta EN Railway
Este archivo se sube a GitHub y luego se ejecuta en Railway
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpdocs.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Datos del usuario
username = 'admin'
email = 'admin@test.com'
password = 'admin123'

print("=" * 60)
print("🚀 Creando superusuario en Railway...")
print("=" * 60)

# Verificar si ya existe
if User.objects.filter(username=username).exists():
    print(f"⚠️  El usuario '{username}' ya existe")
    user = User.objects.get(username=username)
    print(f"   Email: {user.email}")
    print(f"   Es superusuario: {user.is_superuser}")
    print(f"   Está activo: {user.is_active}")
else:
    # Crear superusuario
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("=" * 60)
    print("✅ ¡SUPERUSUARIO CREADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print("=" * 60)
    print("\n📝 Usa estas credenciales en Postman:")
    print(f'   {{"username": "{username}", "password": "{password}"}}')
    print("=" * 60)
