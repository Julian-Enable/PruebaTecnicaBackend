"""
Script de semilla para crear datos de prueba
Ejecutar con: python manage.py shell < scripts/seed_data.py
"""
from django.contrib.auth.models import User
from core.models import Company, CompanyMembership
import uuid

print("=" * 50)
print("Poblando base de datos con datos de prueba...")
print("=" * 50)

# Crear usuarios de prueba
users_data = [
    ('sebastian', 'APPROVER'),
    ('camilo', 'APPROVER'),
    ('juan', 'APPROVER'),
    ('uploader', 'UPLOADER'),
]

users = {}
for username, role in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@example.com',
            'first_name': username.capitalize(),
            'last_name': 'Test'
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'Usuario creado: {username} (rol: {role})')
    else:
        print(f'Usuario ya existe: {username}')
    users[username] = {'user': user, 'role': role}

# Crear empresa de prueba
company, created = Company.objects.get_or_create(
    name='Test Company',
    defaults={'is_active': True}
)
if created:
    print(f'Empresa creada: {company.name}')
else:
    print(f'Empresa ya existe: {company.name}')

# Crear membresías
for username, data in users.items():
    membership, created = CompanyMembership.objects.get_or_create(
        user=data['user'],
        company=company,
        defaults={'role': data['role'], 'is_active': True}
    )
    if created:
        print(f'Membresía creada: {username} - {data["role"]}')

print("\n" + "=" * 50)
print("Datos de prueba creados exitosamente!")
print("=" * 50)
print(f'\nID de Empresa: {company.id}')
print(f'Nombre de Empresa: {company.name}\n')
print('Usuarios de Prueba (contraseña: test123):')
for username, data in users.items():
    print(f'   - {username:12} (ID: {data["user"].id}) - Rol: {data["role"]}')

print('\nPara obtener token JWT, usar:')
print('   POST http://localhost:8000/api/token/')
print('   {"username": "uploader", "password": "test123"}')
print("=" * 50)
