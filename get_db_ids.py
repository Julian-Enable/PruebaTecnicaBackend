import psycopg2
import uuid

# Conectar usando DATABASE_PUBLIC_URL
DATABASE_URL = "postgresql://postgres:QKmGgEPpaQjwRWalGqxhbXeDHBBiNEUC@switchyard.proxy.rlwy.net:57546/railway"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("\n=== USUARIO ADMIN ===")
    cur.execute("SELECT id, username, email, is_active FROM auth_user WHERE username = 'admin';")
    user_row = cur.fetchone()
    if user_row:
        user_id = user_row[0]
        print(f"ID: {user_id}")
        print(f"Username: {user_row[1]}")
        print(f"Email: {user_row[2]}")
        print(f"Active: {user_row[3]}")
    else:
        print("Usuario 'admin' no encontrado")
        user_id = None
    
    print("\n=== EMPRESA ===")
    cur.execute("SELECT id, name, is_active FROM core_company ORDER BY created_at DESC LIMIT 1;")
    company_row = cur.fetchone()
    if company_row:
        company_id = company_row[0]
        print(f"ID: {company_id}")
        print(f"Name: {company_row[1]}")
        print(f"Active: {company_row[2]}")
    else:
        print("No se encontró empresa")
        company_id = None
    
    print("\n=== MEMBERSHIPS ===")
    if user_id:
        cur.execute("""
            SELECT id, user_id, company_id, role, is_active, created_at
            FROM core_companymembership
            WHERE user_id = %s;
        """, (str(user_id),))
        memberships = cur.fetchall()
        if memberships:
            for m in memberships:
                print(f"ID: {m[0]}, Company: {m[2]}, Role: {m[3]}, Active: {m[4]}")
        else:
            print("No hay memberships para este usuario")
            print("\n=== GENERANDO SQL PARA CREAR MEMBERSHIP ===")
            if company_id:
                membership_id = str(uuid.uuid4())
                sql = f"""
INSERT INTO core_companymembership (id, user_id, company_id, role, is_active, created_at)
VALUES ('{membership_id}', '{user_id}', '{company_id}', 'ADMIN', true, NOW());
"""
                print(sql)
                print("\nEjecuta este SQL en Railway o DBeaver para crear la membership.")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
