"""
Script para crear un superusuario en Railway
Ejecutar con: railway run python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpdocs.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Datos del superusuario
username = 'admin'
email = 'admin@test.com'
password = 'admin123'

# Crear superusuario si no existe
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superusuario creado: {username} / {password}')
else:
    print(f'⚠️  El usuario {username} ya existe')
