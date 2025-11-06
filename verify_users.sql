-- VERIFICAR QUÉ USUARIOS EXISTEN
SELECT id, username, email, is_active, is_staff, is_superuser 
FROM auth_user 
ORDER BY id;

-- SI SEBASTIAN NO EXISTE O ESTÁ INACTIVO, ACTUALIZARLO
-- Primero verificamos si existe
SELECT * FROM auth_user WHERE username = 'sebastian';

-- Si no existe, lo creamos (ejecutar solo si no existe)
-- Password hash para "admin123" con PBKDF2
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$320000$randomsalt$hashedpassword',  -- Necesitamos generar este hash
    NULL,
    false,
    'sebastian',
    'Sebastian',
    'Rodriguez',
    'sebastian@example.com',
    false,
    true,
    NOW()
);

-- VERIFICAR MEMBRESÍAS
SELECT 
    u.username,
    c.name as company_name,
    cm.is_active
FROM core_companymembership cm
JOIN auth_user u ON cm.user_id = u.id
JOIN core_company c ON cm.company_id = c.id
ORDER BY u.username;
