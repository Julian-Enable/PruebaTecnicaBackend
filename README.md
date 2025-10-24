# ERP Documents - Sistema de Gestión de Documentos

Sistema backend completo de gestión de documentos para ERP con validaciones jerárquicas, storage en S3/GCS, y auditoría completa.

## Características

- Backend Django 5.x + DRF con autenticación JWT
- Storage en cloud (S3/GCS) con URLs prefirmadas
- Validaciones jerárquicas con flujo de aprobaciones multinivel
- Multi-tenancy con permisos por empresa
- Auditoría completa de acciones y descargas
- Atomicidad garantizada (no hay objetos huérfanos)
- Tests completos con pytest y mocks
- Docker para desarrollo y producción
- API REST documentada con Swagger

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
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=true

# Database
DB_HOST=postgres          # o localhost para dev local
DB_NAME=erpdocs
DB_USER=erpdocs
DB_PASSWORD=erpdocs

# Storage
STORAGE_PROVIDER=S3       # S3 o GCS
STORAGE_BUCKET_NAME=erpdocs-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# Validaciones
ALLOWED_MIME_TYPES=application/pdf,image/jpeg,image/png
MAX_UPLOAD_BYTES=10485760  # 10MB
```

## API Endpoints

### Autenticación

```bash
# Obtener token JWT
POST /api/token/
{
  "username": "sebastian",
  "password": "test123"
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

#### 2. Crear documento (después de subir a bucket)

```bash
POST /api/documents/
Authorization: Bearer <token>
{
  "company_id": "11111111-1111-1111-1111-111111111111",
  "entity": {
    "entity_type": "vehicle",
    "entity_id": "22222222-2222-2222-2222-222222222222"
  },
  "document": {
    "name": "soat.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 123456,
    "bucket_key": "companies/uuid/vehicles/uuid/docs/soat.pdf"
  },
  "validation_flow": {
    "enabled": true,
    "steps": [
      {"order": 1, "approver_user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
      {"order": 2, "approver_user_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"},
      {"order": 3, "approver_user_id": "cccccccc-cccc-cccc-cccc-cccccccccccc"}
    ]
  }
}
```

⚠️ **CRÍTICO**: El objeto DEBE existir en el bucket antes de llamar a este endpoint.

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
POST /api/documents/{document_id}/approve/
Authorization: Bearer <token>
{
  "actor_user_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
  "reason": "Cumple con los requisitos"
}
```

**Lógica de aprobación:**
- Si aprueba en orden K, se marcan aprobados automáticamente todos los pasos < K pendientes
- Si aprueba en el orden MÁS ALTO, el documento pasa a estado "Approved" (A)
- Si hay más pasos pendientes, el documento sigue en "Pending" (P)

#### 5. Rechazar documento

```bash
POST /api/documents/{document_id}/reject/
Authorization: Bearer <token>
{
  "actor_user_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
  "reason": "Documento ilegible"
}
```

**Lógica de rechazo:**
- CUALQUIER rechazo pone el documento en estado "Rejected" (R) - **TERMINAL**
- NO se pueden hacer más acciones después de un rechazo

#### 6. Ver historial de auditoría

```bash
GET /api/documents/{document_id}/audit/
Authorization: Bearer <token>
```

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

## Reglas de Negocio

### Atomicidad
1. No se crea registro en DB si el objeto no existe en bucket
2. Se verifica con `HEAD` antes de crear el documento
3. No hay objetos huérfanos en bucket

### Validaciones Jerárquicas
1. Pasos ordenados secuencialmente (1, 2, 3, ...)
2. Aprobación en orden K marca aprobados implícitamente todos < K
3. Aprobación en orden máximo → documento "Approved" (A)
4. Cualquier rechazo → documento "Rejected" (R) - terminal
5. No se pueden hacer acciones después de rechazo o aprobación final

### Permisos
1. Usuario debe ser miembro de la empresa para acceder a documentos
2. Solo aprobadores del flujo pueden aprobar/rechazar
3. Auditoría de todas las acciones

## Datos de Prueba

Después de ejecutar `seed`, tendrás:

**Empresa:**
- Test Company (UUID se muestra en la salida)

**Usuarios:** (password: `test123`)
- `sebastian` - Aprobador orden 1
- `camilo` - Aprobador orden 2  
- `juan` - Aprobador orden 3
- `uploader` - Puede subir documentos

## Ejemplo de Flujo Completo

```bash
# 1. Obtener token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"uploader","password":"test123"}' \
  | jq -r '.access')

# 2. Obtener URL de subida
UPLOAD_DATA=$(curl -X POST http://localhost:8000/api/storage/presign-put/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bucket_key":"test/soat-2025.pdf",
    "mime_type":"application/pdf"
  }')

UPLOAD_URL=$(echo $UPLOAD_DATA | jq -r '.upload_url')

# 3. Subir archivo al bucket usando la URL prefirmada
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/pdf" \
  --data-binary @soat.pdf

# 4. Crear documento en el sistema
DOC_RESPONSE=$(curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id":"<COMPANY_UUID>",
    "entity":{"entity_type":"vehicle","entity_id":"22222222-2222-2222-2222-222222222222"},
    "document":{
      "name":"soat.pdf",
      "mime_type":"application/pdf",
      "size_bytes":123456,
      "bucket_key":"test/soat-2025.pdf"
    },
    "validation_flow":{
      "enabled":true,
      "steps":[
        {"order":1,"approver_user_id":"<SEBASTIAN_UUID>"},
        {"order":2,"approver_user_id":"<CAMILO_UUID>"},
        {"order":3,"approver_user_id":"<JUAN_UUID>"}
      ]
    }
  }')

DOC_ID=$(echo $DOC_RESPONSE | jq -r '.id')

# 5. Aprobar en orden 3 (aprobación final)
curl -X POST http://localhost:8000/api/documents/$DOC_ID/approve/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "actor_user_id":"<JUAN_UUID>",
    "reason":"Documento válido"
  }'

# 6. Descargar documento
curl -X GET http://localhost:8000/api/documents/$DOC_ID/download/ \
  -H "Authorization: Bearer $TOKEN"
```

## 🎬 Demo en Video

Para grabar un video de demostración:

1. Iniciar el servidor: `docker-compose up`
2. Abrir Swagger UI: `http://localhost:8000/api/docs/`
3. Ejecutar la secuencia de comandos de arriba
4. Mostrar en el admin de Django: `http://localhost:8000/admin/`
   - Documentos creados
   - Flujos de validación
   - Auditorías de estado y descargas

## 🐛 Troubleshooting

### Error de conexión a PostgreSQL
```bash
# Verificar que PostgreSQL está corriendo
docker-compose ps

# Ver logs
docker-compose logs postgres
```

### Error de credenciales S3
```bash
# Verificar variables en .env
cat .env | grep AWS

# Probar credenciales con AWS CLI
aws s3 ls s3://erpdocs-bucket --profile default
```

### Tests fallan
```bash
# Limpiar base de datos de test
python manage.py flush --database=default --no-input

# Verificar que storage está mockeado
grep -r "mock_storage_service" tests/
```

## Documentación API

Una vez iniciado el servidor:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Schema OpenAPI**: http://localhost:8000/api/schema/

## Seguridad

- Autenticación JWT
- Permisos por empresa (multi-tenancy)
- Validación de MIME types
- Límite de tamaño de archivo
- URLs prefirmadas con expiración
- No se exponen credenciales de storage

## Deployment

Ver `docker/Dockerfile` para build de producción.

Para producción, cambiar en `.env`:
```env
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<generar uno seguro>
DB_PASSWORD=<contraseña fuerte>
```

## Licencia

MIT License

**Criterios de Aceptación Cumplidos:**

- Crear documento falla si `head_object(bucket_key)` no existe  
- Aprobación por usuario de orden K marca aprobados previos < K  
- Aprobación en último orden cambia documento a A  
- Cualquier rechazo pone documento en R y bloquea posteriores acciones  
- GET /download devuelve URL prefirmada y estado actual  
- Usuarios sin acceso a la empresa reciben 403          
- Pruebas clave pasan en CI local (pytest -q)  
- README con instrucciones reproducibles (Docker o venv)  
