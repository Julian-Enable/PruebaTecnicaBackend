# 🔧 PASO 1: CONFIGURACIÓN INICIAL

> **Lee esto PRIMERO antes de hacer cualquier cosa**

---

## ⏱️ Tiempo estimado: 10-15 minutos

---

## 📋 Pre-requisitos

Antes de empezar, asegúrate de tener:

- [ ] PostgreSQL instalado en tu computadora
- [ ] Python 3.12 instalado
- [ ] Este proyecto descargado
- [ ] PowerShell abierto (como Administrador si es posible)

---

## 🚀 Paso a Paso - CONFIGURACIÓN

### 1️⃣ Abrir PowerShell en la carpeta del proyecto

```powershell
# Navega a la carpeta del proyecto
cd C:\Users\Desktop\Documents\Julian\GitHub\PruebaTecnicaBackend
```

**¿Cómo saber que estás en el lugar correcto?**
- Debes ver una carpeta llamada `entrega`
- Debes ver un archivo llamado `manage.py`

---

### 2️⃣ Crear la Base de Datos PostgreSQL

```powershell
# Ve a la carpeta entrega
cd entrega

# Ejecuta el script de configuración
.\setup_postgres.ps1
```

**📝 ¿Qué hace este script?**
- Crea una base de datos llamada `erpdocs`
- Configura los permisos necesarios

**❓ Te pedirá:**
- La contraseña de PostgreSQL (la que configuraste al instalar PostgreSQL)

**✅ Sabrás que funcionó si ves:**
```
Base de datos creada correctamente
PostgreSQL configurado correctamente
```

**❌ Si ves un error:**
- Verifica que PostgreSQL esté corriendo
- En Windows busca "Services" y busca "postgresql"
- Debe estar en estado "Running"

---

### 3️⃣ Arreglar Permisos de PostgreSQL

```powershell
# Ejecuta el script de permisos
.\fix_postgres_permissions.ps1
```

**📝 ¿Qué hace este script?**
- Otorga permisos al esquema `public` de la base de datos
- Permite que Django pueda crear tablas

**❓ Te pedirá:**
- La contraseña de PostgreSQL (la misma de antes)

**✅ Sabrás que funcionó si ves:**
```
Permisos configurados correctamente
```

---

### 4️⃣ Volver a la carpeta raíz del proyecto

```powershell
# Vuelve a la carpeta principal
cd ..
```

**Verifica que estás en el lugar correcto:**
```powershell
# Debes ver "manage.py" en esta carpeta
ls manage.py
```

---

### 5️⃣ Activar el Entorno Virtual de Python

```powershell
# Activa el entorno virtual
.venv\Scripts\Activate.ps1
```

**✅ Sabrás que funcionó si ves:**
- `(.venv)` al inicio de tu línea de comando
- Ejemplo: `(.venv) PS C:\...\PruebaTecnicaBackend>`

**❌ Si no funciona:**
- Puede que necesites ejecutar este comando primero:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### 6️⃣ Crear las Tablas en la Base de Datos (Migraciones)

```powershell
# Ejecuta las migraciones de Django
python manage.py migrate
```

**📝 ¿Qué hace este comando?**
- Crea TODAS las tablas en la base de datos PostgreSQL
- Tablas para usuarios, empresas, documentos, validaciones, etc.

**✅ Sabrás que funcionó si ves:**
```
Applying contenttypes.0001_initial... OK
Applying auth.0001_initial... OK
Applying core.0001_initial... OK
Applying documents.0001_initial... OK
Applying validation.0001_initial... OK
```

**Verás aproximadamente 21 líneas que dicen "OK"**

---

### 7️⃣ Crear el Usuario Administrador (Ya lo tienes creado)

> **NOTA:** Ya creaste este usuario antes, así que SALTA este paso.

Si necesitas crearlo de nuevo:
```powershell
python manage.py createsuperuser --username admin --email admin@example.com
```

Cuando te pida contraseña, escribe: `admin123` (no verás nada mientras escribes, es normal)

---

### 8️⃣ Cargar Datos de Prueba (Usuarios y Empresa)

```powershell
# Abre el shell de Django
python manage.py shell
```

**Se abrirá una consola interactiva de Python. Verás algo como:**
```
Python 3.12.0 (...)
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

Ahora **copia TODO el contenido** del archivo `entrega\load_data.py` y **pégalo** en esta consola.

**Para copiar el archivo:**
1. Abre `entrega\load_data.py` en VS Code
2. Selecciona TODO (Ctrl+A)
3. Copia (Ctrl+C)
4. Vuelve a la consola de PowerShell
5. Pega (Click derecho del mouse o Ctrl+V)
6. Presiona Enter

**✅ Sabrás que funcionó si ves:**

```
==================================================
Cargando datos de prueba...
==================================================

Creando usuarios...
  - Usuario creado: sebastian
  - Usuario creado: camilo
  - Usuario creado: juan
  - Usuario creado: uploader

Creando empresa...
  - Empresa creada: Test Company SAS

Creando membresias...
  - Membresia creada: sebastian - APPROVER
  - Membresia creada: camilo - APPROVER
  - Membresia creada: juan - APPROVER
  - Membresia creada: uploader - UPLOADER

============================================================
COPIA ESTOS IDs PARA POSTMAN
============================================================
$COMPANY_ID = "ebbc771d-86ea-404e-b69e-20bd0511b1c8"
$USER_SEBASTIAN = 1
$USER_CAMILO = 2
$USER_JUAN = 3
$USER_UPLOADER = 4

# ID de vehiculo de prueba (puedes usar cualquier UUID):
$VEHICLE_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
============================================================

Datos cargados exitosamente!
============================================================
```

**🔴 MUY IMPORTANTE:**
**COPIA LOS IDs QUE APARECEN** - Los necesitarás para Postman en el siguiente paso.

Para salir del shell de Django, escribe `exit()` y presiona Enter.

---

### 9️⃣ Iniciar el Servidor de Django

```powershell
# Inicia el servidor de desarrollo
python manage.py runserver
```

**✅ Sabrás que funcionó si ves:**
```
Django version 5.0.1, using settings 'erpdocs.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**🎉 ¡El servidor está corriendo!**

**IMPORTANTE:** 
- **NO CIERRES esta ventana de PowerShell**
- El servidor debe estar corriendo para hacer las pruebas
- Para detenerlo más tarde: presiona `Ctrl+C`

---

## ✅ Checklist de Verificación

Marca cada cosa que hayas completado:

- [ ] Base de datos `erpdocs` creada
- [ ] Permisos de PostgreSQL arreglados
- [ ] Entorno virtual activado (ves `(.venv)` en la consola)
- [ ] Migraciones aplicadas (viste ~21 "OK")
- [ ] Usuario admin creado
- [ ] Datos de prueba cargados (4 usuarios + 1 empresa)
- [ ] **IDs copiados y guardados en algún lugar**
- [ ] Servidor Django corriendo en http://127.0.0.1:8000/

---

## 📝 Usuarios Creados

Tienes estos usuarios para las pruebas:

| Usuario | Contraseña | Rol | Descripción |
|---------|-----------|-----|-------------|
| admin | admin123 | Superusuario | Acceso al admin de Django |
| sebastian | test123 | APPROVER | Puede aprobar nivel 1 |
| camilo | test123 | APPROVER | Puede aprobar nivel 2 |
| juan | test123 | APPROVER | Puede aprobar nivel 3 (más alto) |
| uploader | test123 | UPLOADER | Solo sube documentos |

---

## 🎯 Siguiente Paso

**Ahora ve a:** `PASO_2_PRUEBAS_POSTMAN.md`

Ahí aprenderás cómo probar el sistema usando Postman.

---

## 🆘 Problemas Comunes

### "No se puede conectar a PostgreSQL"
- **Solución:** Verifica que PostgreSQL esté corriendo
- Windows: Services → postgresql-x64-XX → Start

### "ModuleNotFoundError: No module named 'django'"
- **Solución:** Activa el entorno virtual: `.venv\Scripts\Activate.ps1`

### "permission denied for schema public"
- **Solución:** Ejecuta `.\fix_postgres_permissions.ps1` de nuevo

### No veo ningún error pero algo no funciona
- **Solución:** Asegúrate de estar en la carpeta correcta (donde está `manage.py`)

---

**¿Todo listo? ✅ Continúa con el PASO 2**
