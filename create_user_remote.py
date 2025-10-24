"""
Crear superusuario conectándose directamente a PostgreSQL de Railway
"""
import psycopg2
from psycopg2.extras import execute_values
import hashlib

# Credenciales de Railway (las viste en railway variables)
DATABASE_URL = "postgresql://postgres:QKmGgEPpaQjwRWalGqxhbXeDHBBiNEUC@postgres.railway.internal:5432/railway"

# Cambiar el host interno por uno público
# Railway expone PostgreSQL públicamente, necesitamos el host público
print("❌ No podemos conectarnos directamente - postgres.railway.internal es interno al cluster")
print("\n✅ Mejor opción: Usar railway shell o Django Admin")
print("\n📝 Instrucciones:")
print("1. Abre Postman")
print("2. Importa la colección de entrega/")
print("3. Usa el endpoint de registro (si existe)")
print("4. O accede a /admin/ y crea el usuario manualmente")
