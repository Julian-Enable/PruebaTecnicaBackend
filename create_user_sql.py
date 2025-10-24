"""
Crear superusuario directamente en PostgreSQL de Railway
Ejecutar: railway run python create_user_sql.py
"""
import os
import sys

# Verificar que tengamos DATABASE_URL
database_url = os.getenv('DATABASE_URL')
if not database_url:
    print("❌ DATABASE_URL no encontrada")
    sys.exit(1)

print(f"✅ DATABASE_URL encontrada: {database_url[:30]}...")

# Intentar importar psycopg
try:
    import psycopg
    print("✅ psycopg encontrado")
except ImportError:
    print("❌ psycopg no está instalado")
    print("   Instala con: pip install psycopg")
    sys.exit(1)

# Datos del usuario
username = 'admin'
email = 'admin@test.com'
# Password hasheado para 'admin123' usando Django's PBKDF2
password_hash = 'pbkdf2_sha256$600000$dummy$hash'  # Necesitamos generar esto correctamente

print("\n⚠️  ADVERTENCIA: Este método requiere generar el hash de contraseña correctamente")
print("   Es más seguro usar el Django management command")
print("\n📝 Mejor opción: Espera, voy a crear una solución mejor...")
