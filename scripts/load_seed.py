from django.contrib.auth.models import User
from core.models import Company, CompanyMembership

print("Creando datos de prueba...")

# Crear usuarios
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
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'Usuario creado: {username}')
    users[username] = {'user': user, 'role': role}

# Crear empresa
company, created = Company.objects.get_or_create(
    name='Test Company',
    defaults={'is_active': True}
)
print(f'Empresa: {company.name}')

# Crear membresías
for username, data in users.items():
    membership, created = CompanyMembership.objects.get_or_create(
        company=company,
        user=data['user'],
        defaults={'role': data['role']}
    )
    if created:
        print(f'Añadido {username} a empresa como {data["role"]}')

print("\nDatos de prueba cargados exitosamente!")
print("\nCredenciales:")
print("Usuario admin: admin / admin123")
print("Usuarios de prueba: sebastian, camilo, juan, uploader (todos con contraseña: test123)")
print(f"ID de Empresa: {company.id}")
