# ERP Documents - Sistema de Gestión de Documentos

Sistema backend completo de gestión de documentos para ERP con validaciones jerárquicas, storage en S3/GCS, y auditoría completa.

## Demo en Producción

**URL de la API**: https://pruebatecnicabackend-production.up.railway.app

**Credenciales de prueba**:
- **Admin**: `admin` / `admin123`
- **Sebastian** (Supervisor): `sebastian` / `admin123`
- **Camilo** (Gerente): `camilo` / `admin123`
- **Juan** (CEO): `juan` / `admin123`

**Archivos de la demo**: Ver carpeta `/entrega/` con:
- `GUION_VIDEO.md` - Guion detallado para video de sustentación
- `INSTRUCTIVO_DEMO.md` - Instructivo completo de pruebas
- `ERP_Documents_Postman_Collection.json` - Colección de Postman lista para importar

## Características

- Backend Django 5.0.1 + DRF con autenticación JWT
- Storage en cloud (AWS S3) o modo LOCAL para demos
- **Aprobación en cascada**: CEO puede aprobar todos los niveles automáticamente
- Validaciones jerárquicas con flujo de aprobaciones multinivel
- Multi-tenancy con permisos por empresa
- Auditoría completa e inmutable de todas las acciones
- Estados terminales para documentos rechazados
- Desplegado en Railway con PostgreSQL
- API REST documentada y probada con Postman

## Requisitos

- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose (opcional)
- Cuenta AWS S3 o Google Cloud Storage

## Instalación

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar repositorio
git clone <repo-url>
cd PruebaTecnicaBackend

# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus credenciales
# Especialmente AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY

# Levantar servicios
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Seed de datos de prueba
docker-compose exec web python manage.py shell < scripts/seed_data.py
```

### Opción 2: Entorno Local

```bash
# Clonar repositorio
git clone <repo-url>
cd PruebaTecnicaBackend

# Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Editar .env con configuración local
# Cambiar DB_HOST=localhost

# Asegurarse que PostgreSQL está corriendo localmente
# Crear base de datos: CREATE DATABASE erpdocs;

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
.\scripts\manage.ps1 seed

# Iniciar servidor
python manage.py runserver
```

## Estructura del Proyecto

```
PruebaTecnicaBackend/
├── erpdocs/              # Configuración Django
│   ├── settings.py       # Settings con variables de entorno
│   └── urls.py           # URLs principales
├── core/                 # Modelos base
│   ├── models.py         # Company, CompanyMembership, AuditMixin
│   └── permissions.py    # IsCompanyMember, CanApproveDocument
├── documents/            # Gestión de documentos
│   ├── models.py         # Document, DocumentDownloadAudit, DocumentStateAudit
│   ├── serializers.py    # Serializers de DRF
│   └── views.py          # ViewSets y endpoints
├── validation/           # Sistema de validaciones
│   ├── models.py         # ValidationFlow, ValidationStep, ValidationInstance, ValidationAction
│   └── services.py       # Lógica de aprobación/rechazo
├── storageapp/           # Integración con S3/GCS
│   ├── services.py       # StorageService, S3Provider, GCSProvider
│   └── views.py          # Endpoint presign-put
├── tests/                # Suite de pruebas
│   ├── conftest.py       # Fixtures de pytest
│   ├── test_validation.py
│   └── test_api.py
├── docker/
│   └── Dockerfile        # Imagen Docker
├── scripts/              # Utilidades
│   └── manage.ps1        # Script de gestión
├── docker-compose.yml    # Orquestación de servicios
├── requirements.txt      # Dependencias Python
└── README.md
```

## Variables de Entorno

Ver `.env.example` para todas las opciones. Las principales son:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.railway.app,.up.railway.app

# Database (Railway provee DATABASE_URL automáticamente)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Storage - Modo LOCAL para demos sin S3 real
STORAGE_PROVIDER=LOCAL              # LOCAL para demos, S3 para producción
AWS_STORAGE_BUCKET_NAME=erp-documents-production
AWS_ACCESS_KEY_ID=your-key          # Solo si STORAGE_PROVIDER=S3
AWS_SECRET_ACCESS_KEY=your-secret   # Solo si STORAGE_PROVIDER=S3
AWS_S3_REGION_NAME=us-east-2        # Solo si STORAGE_PROVIDER=S3

# En modo LOCAL, los download URLs son simulados para propósitos de demo
```

## Inicio Rápido con Postman

La forma más rápida de probar la API:

1. **Importar la colección**: Abrir Postman e importar `entrega/ERP_Documents_Postman_Collection.json`

2. **Obtener token JWT**: Ejecutar la petición "Obtener Token JWT" en la carpeta "1. Autenticación"

3. **Probar los 5 escenarios**:
   - Aprobación en cascada (CEO aprueba todos los niveles)
   - Aprobación secuencial (paso por paso)
   - Rechazo de documento
   - Documento sin validación
   - Descarga de documento

4. **Ver la auditoría**: Consultar el historial completo de cada documento

Ver `entrega/INSTRUCTIVO_DEMO.md` para guía detallada paso a paso.

## API Endpoints

### Autenticación

```bash
# Obtener token JWT
POST https://pruebatecnicabackend-production.up.railway.app/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

# Respuesta
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Documentos

#### 1. Obtener URL de subida (opcional)

```bash
POST /api/storage/presign-put/
Authorization: Bearer <token>
{
  "bucket_key": "companies/uuid/vehicles/uuid/docs/soat.pdf",
  "mime_type": "application/pdf"
}

# Respuesta
{
  "upload_url": "https://s3.amazonaws.com/...",
  "bucket_key": "companies/uuid/...",
  "expires_in": 900
}
```

#### 2. Crear documento

```bash
POST https://pruebatecnicabackend-production.up.railway.app/api/documents/
Authorization: Bearer <token>
Content-Type: application/json

{
  "company_id": "9da4abe9-57c7-4d76-ad5c-5e01d554f2c5",
  "entity": {
    "entity_type": "vehicle",
    "entity_id": "22222222-2222-2222-2222-222222222222"
  },
  "document": {
    "name": "documento_1729845123456.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 123456,
    "bucket_key": "companies/demo/vehicles/documento_1729845123456.pdf"
  },
  "validation_flow": {
    "enabled": true,
    "steps": [
      {"order": 1, "approver_user_id": 9},    # Sebastian (Supervisor)
      {"order": 2, "approver_user_id": 10},   # Camilo (Gerente)
      {"order": 3, "approver_user_id": 11}    # Juan (CEO)
    ]
  }
}
```

**Nota**: En modo `STORAGE_PROVIDER=LOCAL`, la verificación de existencia del archivo en S3 se omite para propósitos de demo. En producción con S3, el bucket_key debe existir antes de crear el documento.

#### 3. Descargar documento

```bash
GET /api/documents/{document_id}/download/
Authorization: Bearer <token>

# Respuesta
{
  "download_url": "https://s3.amazonaws.com/...",
  "validation_status": "P",
  "document_name": "soat.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 123456
}
```

#### 4. Aprobar documento

```bash
POST https://pruebatecnicabackend-production.up.railway.app/api/documents/{document_id}/approve/
Authorization: Bearer <token>
Content-Type: application/json

{
  "actor_user_id": 11,
  "reason": "Aprobado por CEO - cumple todos los requisitos"
}
```

**Lógica de aprobación en cascada:**
- Si Juan (orden 3, CEO) aprueba, automáticamente se aprueban Sebastian (orden 1) y Camilo (orden 2)
- Todos los pasos con orden menor al aprobador se marcan como aprobados automáticamente
- El documento pasa directo de estado "P" (Pending) a "A" (Approved)
- Queda registrado en auditoría quién aprobó y cuáles fueron auto-aprobaciones en cascada

**Lógica de aprobación secuencial:**
- Si Sebastian (orden 1) aprueba primero, el documento sigue en "P"
- Luego Camilo (orden 2) aprueba, el documento sigue en "P"
- Finalmente Juan (orden 3) aprueba, el documento pasa a "A"

#### 5. Rechazar documento

```bash
POST https://pruebatecnicabackend-production.up.railway.app/api/documents/{document_id}/reject/
Authorization: Bearer <token>
Content-Type: application/json

{
  "actor_user_id": 10,
  "reason": "Documento ilegible - falta firma del representante legal"
}
```

**Lógica de rechazo:**
- CUALQUIER rechazo pone el documento en estado "R" (Rejected) - **ESTADO TERMINAL**
- NO se pueden hacer más aprobaciones ni rechazos después
- Queda registrado en auditoría quién rechazó y por qué

#### 6. Ver historial de auditoría

```bash
GET https://pruebatecnicabackend-production.up.railway.app/api/documents/{document_id}/audit/
Authorization: Bearer <token>
```

**Respuesta incluye:**
- Todas las acciones (CREATE, APPROVE, REJECT, DOWNLOAD)
- Usuario que realizó cada acción
- Timestamp exacto de cada acción
- Razón de aprobación/rechazo
- Indicador de aprobaciones en cascada
- Historial completo e inmutable

## Reglas de Negocio Implementadas

### Aprobación en Cascada (Característica Principal)

Cuando un aprobador de orden superior aprueba un documento:
1. Se marca como aprobado ese paso
2. Se marcan automáticamente como aprobados todos los pasos con orden inferior que estén pendientes
3. Si es el último paso, el documento pasa a estado "A" (Approved)
4. Queda registrado en auditoría cuáles fueron auto-aprobadas por cascada

**Ejemplo:** Documento con 3 niveles (Sebastian-1, Camilo-2, Juan-3)
- Si Juan (orden 3) aprueba primero → Sebastian y Camilo se aprueban automáticamente → Documento pasa a "A"
- Auditoría muestra: "Auto-aprobado por cascada" para niveles 1 y 2

### Estados Terminales

1. **Pending (P)**: Estado inicial cuando se crea con validation_flow
2. **Approved (A)**: Todos los pasos aprobados - TERMINAL
3. **Rejected (R)**: Cualquier rechazo - TERMINAL
4. No se puede aprobar un documento rechazado
5. No se puede rechazar un documento ya aprobado

### Permisos y Multi-tenancy

1. Usuario debe ser miembro de la empresa para ver/crear documentos
2. Solo el aprobador asignado en cada step puede aprobar/rechazar ese paso
3. Cada empresa tiene sus documentos completamente aislados
4. Auditoría registra quién hizo qué en cada documento

### Storage

- **Modo LOCAL**: URLs simuladas para demos sin configurar S3 real
- **Modo S3**: Integración real con AWS S3 (verificación de bucket_key antes de crear documento)

## Ejecutar Tests

```bash
# Con Docker
docker-compose exec web pytest tests/ -v

# Local
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html

# Tests específicos
pytest tests/test_validation.py -v
pytest tests/test_api.py::TestDocumentAPI::test_create_document_with_validation_flow -v
```

## Datos de Prueba en Producción

La instancia de Railway ya tiene configurados:

**Empresa:**
- Empresa Demo S.A. (UUID: `9da4abe9-57c7-4d76-ad5c-5e01d554f2c5`)

**Usuarios:** (todos con password `admin123`)
- `admin` (ID: 8) - Administrador
- `sebastian` (ID: 9) - Supervisor (orden 1)
- `camilo` (ID: 10) - Gerente (orden 2)
- `juan` (ID: 11) - CEO (orden 3)

Todos los usuarios son miembros de "Empresa Demo S.A." y pueden crear/aprobar documentos.

**Usuarios:** (password: `test123`)
- `sebastian` - Aprobador orden 1
- `camilo` - Aprobador orden 2  
- `juan` - Aprobador orden 3
- `uploader` - Puede subir documentos

## Ejemplo de Flujo Completo

**Nota**: Usar mejor la colección de Postman en `entrega/ERP_Documents_Postman_Collection.json`

```bash
# 1. Obtener token
curl -X POST https://pruebatecnicabackend-production.up.railway.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 2. Crear documento con validación de 3 niveles
curl -X POST https://pruebatecnicabackend-production.up.railway.app/api/documents/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id":"9da4abe9-57c7-4d76-ad5c-5e01d554f2c5",
    "entity":{"entity_type":"vehicle","entity_id":"22222222-2222-2222-2222-222222222222"},
    "document":{
      "name":"documento_demo.pdf",
      "mime_type":"application/pdf",
      "size_bytes":123456,
      "bucket_key":"companies/demo/vehicles/documento_demo.pdf"
    },
    "validation_flow":{
      "enabled":true,
      "steps":[
        {"order":1,"approver_user_id":9},
        {"order":2,"approver_user_id":10},
        {"order":3,"approver_user_id":11}
      ]
    }
  }'

# 3. Aprobar en orden 3 (Juan - CEO) - APROBACION EN CASCADA
curl -X POST https://pruebatecnicabackend-production.up.railway.app/api/documents/<DOC_ID>/approve/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "actor_user_id":11,
    "reason":"Aprobado por CEO"
  }'

# Resultado: Sebastian (1) y Camilo (2) se aprueban automáticamente, documento pasa a estado "A"

# 4. Ver auditoría completa
curl -X GET https://pruebatecnicabackend-production.up.railway.app/api/documents/<DOC_ID>/audit/ \
  -H "Authorization: Bearer <TOKEN>"

# 5. Descargar documento
curl -X GET https://pruebatecnicabackend-production.up.railway.app/api/documents/<DOC_ID>/download/ \
  -H "Authorization: Bearer <TOKEN>"
```
# 5. Descargar documento
curl -X GET https://pruebatecnicabackend-production.up.railway.app/api/documents/<DOC_ID>/download/ \
  -H "Authorization: Bearer <TOKEN>"
```

## Ejecutar Tests
```bash
# Limpiar base de datos de test
python manage.py flush --database=default --no-input

# Verificar que storage está mockeado
grep -r "mock_storage_service" tests/
```

## Arquitectura y Decisiones de Diseño

### Modelo de Datos

**ValidationFlow y ValidationStep**: Configuración reutilizable de flujos de aprobación. Permite definir jerarquías flexibles por documento.

**ValidationInstance y ValidationAction**: Estado mutable de cada paso de aprobación. Permite tracking granular de quién aprobó qué y cuándo.

**DocumentAudit**: Registro inmutable de todas las acciones. Garantiza trazabilidad completa para compliance.

### Aprobación en Cascada

Implementada en `validation/services.py`:
- Query que actualiza todos los ValidationInstance con order < approver_order
- Genera registros de auditoría indicando "Auto-aprobado por cascada"
- Permite que ejecutivos senior aprueben rápidamente sin esperar aprobaciones de niveles inferiores

### Multi-tenancy

- Cada usuario pertenece a una o más empresas via `CompanyMembership`
- Filtrado automático de documentos por empresa en los ViewSets
- Permission classes validan membresía antes de permitir acceso

### Storage Flexible

- Abstracción `StorageService` permite cambiar entre S3, GCS, o modo LOCAL
- En producción: AWS S3 con URLs prefirmadas
- En demo: Modo LOCAL con URLs simuladas (sin necesidad de configurar S3)

## Deployment en Railway

El proyecto está desplegado en Railway con:
- PostgreSQL 16 como base de datos
- Variables de entorno configuradas
- Gunicorn como servidor WSGI
- Colección de Postman en `/entrega/` para pruebas

Para replicar el deployment:
1. Crear proyecto en Railway
2. Conectar repositorio de GitHub
3. Agregar servicio PostgreSQL
4. Configurar variables: `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `STORAGE_PROVIDER=LOCAL`
5. Deploy automático desde main branch

## Seguridad

- Autenticación JWT con tokens de acceso y refresh
- Permisos por empresa (multi-tenancy)
- Validación de que solo aprobadores asignados pueden aprobar/rechazar
- Estados terminales previenen modificaciones inconsistentes
- Auditoría inmutable de todas las acciones

## Licencia

MIT License

## Criterios de Aceptación Cumplidos

- Aprobación por usuario de orden K marca aprobados automáticamente todos los pasos con orden < K (aprobación en cascada)
- Aprobación en último orden cambia documento a estado "A" (Approved)
- Cualquier rechazo pone documento en estado "R" (Rejected) y bloquea acciones posteriores
- GET /download devuelve URL de descarga y estado actual del documento
- Usuarios sin acceso a la empresa reciben 403 Forbidden
- Multi-tenancy con aislamiento completo de datos por empresa
- Auditoría completa e inmutable de todas las acciones
- API REST funcional desplegada en producción
- Colección de Postman con casos de prueba completos  
