from django.contrib.auth.models import User
from core.models import Company, CompanyMembership

print("\n" + "="*50)
print("Cargando datos de prueba...")
print("="*50 + "\n")

# Crear usuarios
users_data = [
    ('sebastian', 'APPROVER'),
    ('camilo', 'APPROVER'),
    ('juan', 'APPROVER'),
    ('uploader', 'UPLOADER'),
]

print("Creando usuarios...")
for username, role in users_data:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': f'{username}@example.com'}
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'  - Usuario creado: {username}')
    else:
        print(f'  - Usuario ya existe: {username}')

# Crear empresa
print("\nCreando empresa...")
company, created = Company.objects.get_or_create(
    name='Test Company SAS',
    defaults={'is_active': True}
)
if created:
    print('  - Empresa creada: Test Company SAS')
else:
    print('  - Empresa ya existe: Test Company SAS')

# Crear membresias
print("\nCreando membresias...")
for username, role in users_data:
    user = User.objects.get(username=username)
    membership, created = CompanyMembership.objects.get_or_create(
        user=user,
        company=company,
        defaults={'role': role, 'is_active': True}
    )
    if created:
        print(f'  - Membresia creada: {username} - {role}')

# Mostrar IDs
print("\n" + "="*60)
print("COPIA ESTOS IDs PARA entrega/demo_simple.ps1")
print("="*60)
print(f'$COMPANY_ID = "{company.id}"')

for username, _ in users_data:
    user = User.objects.get(username=username)
    print(f'$USER_{username.upper()} = {user.id}')

# Crear vehicle de prueba
print(f'\n# ID de vehiculo de prueba (puedes usar cualquier UUID):')
print(f'$VEHICLE_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"')

print("="*60)
print("\nDatos cargados exitosamente!")
print("="*60 + "\n")
