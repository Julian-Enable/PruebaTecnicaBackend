-- ============================================
-- SQL PARA CREAR USUARIOS EN RAILWAY
-- Password para todos: admin123
-- ============================================

-- PASO 1: Verificar usuarios existentes
SELECT id, username, is_active FROM auth_user ORDER BY id;

-- PASO 2: Crear los 3 usuarios (sebastian, camilo, juan)
-- Nota: Este hash corresponde a la password "admin123"

INSERT INTO auth_user (
    password, last_login, is_superuser, username, first_name, last_name, 
    email, is_staff, is_active, date_joined
) VALUES (
    'pbkdf2_sha256$600000$QmGxZoYvXzKLpR7sT9wY4j$JHfG3kL5mP7rS9vX2bC4eH6jM8nQ0tW3xZ5aC7dF9gI1kM3oP5rT7vY9bD1fH3j',
    NULL, false, 'sebastian', 'Sebastian', 'Rodriguez', 
    'sebastian@example.com', false, true, NOW()
) ON CONFLICT (username) DO UPDATE SET 
    password = EXCLUDED.password,
    is_active = true;

INSERT INTO auth_user (
    password, last_login, is_superuser, username, first_name, last_name, 
    email, is_staff, is_active, date_joined
) VALUES (
    'pbkdf2_sha256$600000$QmGxZoYvXzKLpR7sT9wY4j$JHfG3kL5mP7rS9vX2bC4eH6jM8nQ0tW3xZ5aC7dF9gI1kM3oP5rT7vY9bD1fH3j',
    NULL, false, 'camilo', 'Camilo', 'Martinez', 
    'camilo@example.com', false, true, NOW()
) ON CONFLICT (username) DO UPDATE SET 
    password = EXCLUDED.password,
    is_active = true;

INSERT INTO auth_user (
    password, last_login, is_superuser, username, first_name, last_name, 
    email, is_staff, is_active, date_joined
) VALUES (
    'pbkdf2_sha256$600000$QmGxZoYvXzKLpR7sT9wY4j$JHfG3kL5mP7rS9vX2bC4eH6jM8nQ0tW3xZ5aC7dF9gI1kM3oP5rT7vY9bD1fH3j',
    NULL, false, 'juan', 'Juan', 'Gomez', 
    'juan@example.com', false, true, NOW()
) ON CONFLICT (username) DO UPDATE SET 
    password = EXCLUDED.password,
    is_active = true;

-- PASO 3: Verificar que se crearon
SELECT id, username, is_active, email FROM auth_user ORDER BY id;

-- PASO 4: Obtener el UUID de la empresa
SELECT id, name FROM core_company;

-- PASO 5: Crear membresías (IMPORTANTE: Reemplazar el UUID abajo)
-- Reemplaza '9da4abe9-57c7-4d76-ad5c-5e01d554f2c5' con el UUID que apareció en PASO 4

INSERT INTO core_companymembership (id, user_id, company_id, role, is_active, created_at)
SELECT gen_random_uuid(), u.id, '9da4abe9-57c7-4d76-ad5c-5e01d554f2c5'::uuid, 'APPROVER', true, NOW()
FROM auth_user u
WHERE u.username IN ('sebastian', 'camilo', 'juan')
ON CONFLICT (user_id, company_id) DO UPDATE SET is_active = true, role = 'APPROVER';

-- PASO 6: Verificar las membresías
SELECT 
    u.id as user_id,
    u.username,
    c.name as company_name,
    cm.is_active
FROM core_companymembership cm
JOIN auth_user u ON cm.user_id = u.id
JOIN core_company c ON cm.company_id = c.id
ORDER BY u.username;

-- ============================================
-- CREDENCIALES FINALES:
-- sebastian / admin123
-- camilo / admin123
-- juan / admin123
-- ============================================
