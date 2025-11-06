"""
Generar SQL con password hash válido para Railway
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erpdocs.settings')
django.setup()

from django.contrib.auth.hashers import make_password

password = "admin123"
hash_password = make_password(password)

print("\n" + "="*60)
print("SQL PARA CREAR USUARIOS EN RAILWAY")
print("="*60 + "\n")

print("-- Copiar y ejecutar esto en Railway PostgreSQL Query\n")

users = [
    ('sebastian', 'Sebastian', 'Rodriguez', 'sebastian@example.com'),
    ('camilo', 'Camilo', 'Martinez', 'camilo@example.com'),
    ('juan', 'Juan', 'Gomez', 'juan@example.com'),
]

for username, first, last, email in users:
    print(f"""
INSERT INTO auth_user (
    password, last_login, is_superuser, username, first_name, last_name, 
    email, is_staff, is_active, date_joined
) VALUES (
    '{hash_password}',
    NULL, false, '{username}', '{first}', '{last}', 
    '{email}', false, true, NOW()
) ON CONFLICT (username) DO UPDATE SET 
    password = EXCLUDED.password,
    is_active = true,
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    email = EXCLUDED.email;
""")

print("\n-- Verificar usuarios creados:")
print("SELECT id, username, is_active FROM auth_user ORDER BY id;")

print("\n-- Crear membresías (reemplazar 'YOUR_COMPANY_UUID' con el UUID real):")
print("""
INSERT INTO core_companymembership (user_id, company_id, is_active, created_at, updated_at)
SELECT u.id, 'YOUR_COMPANY_UUID'::uuid, true, NOW(), NOW()
FROM auth_user u
WHERE u.username IN ('sebastian', 'camilo', 'juan')
ON CONFLICT (user_id, company_id) DO UPDATE SET is_active = true;
""")

print("\n" + "="*60)
print(f"Password para todos: {password}")
print("="*60 + "\n")
