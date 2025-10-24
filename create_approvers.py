import psycopg2
import uuid
from django.contrib.auth.hashers import make_password

# Conectar usando DATABASE_PUBLIC_URL
DATABASE_URL = "postgresql://postgres:QKmGgEPpaQjwRWalGqxhbXeDHBBiNEUC@switchyard.proxy.rlwy.net:57546/railway"

# Password hasheado con Django (password: "test123" para todos)
# Generado con: make_password("test123")
HASHED_PASSWORD = "pbkdf2_sha256$870000$HqL2wXNkF8QJR3vZ7M9YaP$vPKxJ+8YN3cQW5M7wRYxK8aL3nH9fJ4tB2dC6eG1hI0="

company_id = "9da4abe9-57c7-4d76-ad5c-5e01d554f2c5"

users_to_create = [
    {
        "username": "sebastian",
        "email": "sebastian@empresa.com",
        "first_name": "Sebastian",
        "last_name": "Supervisor",
        "role": "APPROVER",
        "order": 1
    },
    {
        "username": "camilo",
        "email": "camilo@empresa.com",
        "first_name": "Camilo",
        "last_name": "Gerente",
        "role": "APPROVER",
        "order": 2
    },
    {
        "username": "juan",
        "email": "juan@empresa.com",
        "first_name": "Juan",
        "last_name": "CEO",
        "role": "APPROVER",
        "order": 3
    }
]

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("=" * 80)
    print("CREANDO USUARIOS APROBADORES")
    print("=" * 80)
    
    user_ids = {}
    
    for user_data in users_to_create:
        # Crear usuario en auth_user
        cur.execute("""
            INSERT INTO auth_user (
                password, last_login, is_superuser, username, first_name, last_name,
                email, is_staff, is_active, date_joined
            )
            VALUES (%s, NULL, false, %s, %s, %s, %s, false, true, NOW())
            RETURNING id;
        """, (
            HASHED_PASSWORD,
            user_data['username'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['email']
        ))
        
        user_id = cur.fetchone()[0]
        user_ids[user_data['username']] = user_id
        
        print(f"\n✅ Usuario creado: {user_data['username']}")
        print(f"   ID: {user_id}")
        print(f"   Nombre: {user_data['first_name']} {user_data['last_name']}")
        print(f"   Email: {user_data['email']}")
        print(f"   Password: test123")
        
        # Crear membership con la empresa
        membership_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO core_companymembership (id, user_id, company_id, role, is_active, created_at)
            VALUES (%s, %s, %s, %s, true, NOW());
        """, (membership_id, str(user_id), company_id, user_data['role']))
        
        print(f"   ✅ Membership creada: {user_data['role']}")
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print("RESUMEN - IDs PARA POSTMAN")
    print("=" * 80)
    for username, user_id in user_ids.items():
        print(f"{username}: {user_id}")
    
    print("\n" + "=" * 80)
    print("SQL PARA VERIFICAR (copia en Railway/DBeaver):")
    print("=" * 80)
    print("""
SELECT 
    u.id,
    u.username,
    u.email,
    cm.role,
    cm.is_active,
    c.name as company
FROM auth_user u
JOIN core_companymembership cm ON u.id = cm.user_id
JOIN core_company c ON cm.company_id = c.id
WHERE u.username IN ('sebastian', 'camilo', 'juan')
ORDER BY u.id;
    """)
    
    print("\n✅ Todos los usuarios fueron creados exitosamente!")
    print("   Password para todos: test123")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
    if conn:
        conn.rollback()
