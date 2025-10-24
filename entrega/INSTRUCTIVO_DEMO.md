# 📋 INSTRUCTIVO COMPLETO - DEMO ERP DOCUMENTS API

**Fecha**: 24 de Octubre, 2025  
**Autor**: Julian Gonzalez  
**Proyecto**: Sistema de Gestión de Documentos con Validación Jerárquica

---

## 🎯 OBJETIVO

Demostrar el funcionamiento completo del sistema de gestión documental con flujos de validación jerárquica, incluyendo:
- Autenticación JWT
- Creación de documentos con/sin validación
- Aprobación en cascada (CEO aprueba todo)
- Aprobación secuencial (paso a paso)
- Rechazo de documentos
- Auditoría completa
- Generación de URLs de descarga

---

## 🔐 CREDENCIALES

### **Usuarios Disponibles**

| Usuario   | Password  | Rol      | Order | User ID |
|-----------|-----------|----------|-------|---------|
| admin     | admin123  | ADMIN    | -     | 8       |
| sebastian | test123   | APPROVER | 1     | 9       |
| camilo    | test123   | APPROVER | 2     | 10      |
| juan      | test123   | APPROVER | 3     | 11      |

### **Datos del Sistema**

- **Company ID**: `9da4abe9-57c7-4d76-ad5c-5e01d554f2c5`
- **Company Name**: Empresa Demo S.A.
- **Base URL**: `https://pruebatecnicabackend-production.up.railway.app`

---

## 📦 CONFIGURACIÓN INICIAL

### **1. Importar Colección de Postman**

1. Abrir Postman
2. **Import** → Seleccionar archivo: `entrega/ERP_Documents_Postman_Collection.json`
3. Verificar que las variables estén configuradas:
   - `base_url`: URL de Railway
   - `company_id`: UUID de la empresa
   - `token`: Se llenará automáticamente al hacer login

### **2. Verificar Deployment en Railway**

1. Ir a: https://railway.app
2. Proyecto: `endearing-rejoicing`
3. Servicio: `PruebaTecnicaBackend`
4. Verificar que el deployment esté **ACTIVE** (verde)

---

## 🎬 ESCENARIOS DE PRUEBA

---

## **ESCENARIO 1: APROBACIÓN EN CASCADA** ⭐

**Concepto**: Cuando un aprobador de nivel superior (CEO - orden 3) aprueba un documento, automáticamente se aprueban todos los niveles inferiores (1 y 2).

### **Paso 1: Login como Admin**

📁 **1. Autenticación** → **Obtener Token JWT**

**Body**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "access": "eyJ0eXAiOi...",
  "refresh": "eyJ0eXAiOi..."
}
```

✅ El token se guarda automáticamente en la variable `{{token}}`

---

### **Paso 2: Crear Documento CON Validación**

📁 **2. Documentos** → **Crear Documento CON Validación (3 niveles)**

**Resultado Esperado**: `201 Created`
```json
{
  "id": "uuid-del-documento",
  "name": "documento_1729845123456.pdf",
  "validation_status": "P",  // PENDING
  "company_name": "Empresa Demo S.A.",
  ...
}
```

✅ El `document_id` se guarda automáticamente
✅ El nombre incluye timestamp único (no se duplica nunca)

---

### **Paso 3: Verificar que está PENDING**

📁 **2. Documentos** → **Listar Documentos PENDIENTES**

**Resultado Esperado**: `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid-del-documento",
      "validation_status": "P"
    }
  ]
}
```

---

### **Paso 4: Aprobar como Juan (CEO - Cascada)**

📁 **3. Validación** → **Aprobar - Juan (Orden 3) - CASCADA**

**Body**:
```json
{
  "actor_user_id": 11,
  "reason": "Aprobado por CEO - cumple todos los requisitos"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "id": "uuid-del-documento",
  "validation_status": "A",  // APPROVED
  ...
}
```

**🎯 LÓGICA DE CASCADA**:
- ✅ Juan aprueba (orden 3)
- ✅ Automáticamente se aprueban órdenes 1 y 2 (Sebastian y Camilo)
- ✅ Documento pasa directo a APPROVED

---

### **Paso 5: Ver Auditoría Completa**

📁 **3. Validación** → **Auditoría - Historial del Documento**

**Resultado Esperado**: `200 OK`
```json
{
  "document": {...},
  "audit_trail": [
    {
      "action": "CREATE",
      "user": "admin",
      "old_status": null,
      "new_status": "PENDING"
    },
    {
      "action": "APPROVE",
      "user": "sebastian",
      "order": 1,
      "reason": "Auto-aprobado por cascada"
    },
    {
      "action": "APPROVE",
      "user": "camilo",
      "order": 2,
      "reason": "Auto-aprobado por cascada"
    },
    {
      "action": "APPROVE",
      "user": "juan",
      "order": 3,
      "reason": "Aprobado por CEO - cumple todos los requisitos"
    }
  ]
}
```

✅ Muestra las 3 aprobaciones automáticas con timestamps

---

## **ESCENARIO 2: RECHAZO DE DOCUMENTO** 🚫

**Concepto**: Un documento rechazado entra en estado terminal y no puede ser aprobado después.

### **Paso 1: Crear Nuevo Documento**

📁 **2. Documentos** → **Crear Documento CON Validación (3 niveles)**

(El timestamp generará un nombre único automáticamente)

---

### **Paso 2: Rechazar como Camilo**

📁 **3. Validación** → **Rechazar Documento**

**Body**:
```json
{
  "actor_user_id": 10,
  "reason": "Documento ilegible - falta firma del representante legal"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "id": "uuid-del-documento",
  "validation_status": "R",  // REJECTED
  ...
}
```

✅ Estado terminal: no se puede aprobar después

---

### **Paso 3: Intentar Aprobar (debe fallar)**

📁 **3. Validación** → **Aprobar - Sebastian (Orden 1)**

**Resultado Esperado**: `400 Bad Request` o `403 Forbidden`
```json
{
  "error": "No se puede aprobar un documento rechazado"
}
```

---

### **Paso 4: Ver Auditoría del Rechazo**

📁 **3. Validación** → **Auditoría - Historial del Documento**

Muestra el registro REJECT con usuario, razón y timestamp.

---

## **ESCENARIO 3: APROBACIÓN SECUENCIAL** ⚡

**Concepto**: Aprobación paso a paso en orden jerárquico (1 → 2 → 3).

### **Paso 1: Crear Nuevo Documento**

📁 **2. Documentos** → **Crear Documento CON Validación (3 niveles)**

---

### **Paso 2: Aprobar Orden 1 (Sebastian)**

📁 **3. Validación** → **Aprobar - Sebastian (Orden 1)**

**Body**:
```json
{
  "actor_user_id": 9,
  "reason": "Aprobado por Supervisor - documentación completa"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "validation_status": "P"  // Sigue PENDING
}
```

✅ Solo se aprobó orden 1, documento sigue pendiente

---

### **Paso 3: Aprobar Orden 2 (Camilo)**

📁 **3. Validación** → **Aprobar - Camilo (Orden 2)**

**Body**:
```json
{
  "actor_user_id": 10,
  "reason": "Aprobado por Gerente - presupuesto aprobado"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "validation_status": "P"  // Sigue PENDING
}
```

✅ Se aprobaron órdenes 1 y 2, pero aún falta orden 3

---

### **Paso 4: Aprobar Orden 3 (Juan) - FINAL**

📁 **3. Validación** → **Aprobar - Juan (Orden 3) - FINAL**

**Body**:
```json
{
  "actor_user_id": 11,
  "reason": "Aprobado por CEO - autorización final"
}
```

**Resultado Esperado**: `200 OK`
```json
{
  "validation_status": "A"  // APPROVED
}
```

✅ Documento completamente aprobado

---

### **Paso 5: Ver Auditoría Secuencial**

📁 **3. Validación** → **Auditoría - Historial del Documento**

Muestra 4 registros:
1. CREATE (PENDING)
2. APPROVE orden 1 (P → P)
3. APPROVE orden 2 (P → P)
4. APPROVE orden 3 (P → A)

---

## **ESCENARIO 4: DOCUMENTO SIN VALIDACIÓN** 📄

**Concepto**: Documentos que no requieren aprobación.

### **Paso 1: Crear Documento SIN Validación**

📁 **2. Documentos** → **Crear Documento SIN Validación**

**Resultado Esperado**: `201 Created`
```json
{
  "id": "uuid-del-documento",
  "validation_status": null,  // Sin validación
  ...
}
```

✅ `validation_status = null` → No requiere aprobación
✅ Disponible inmediatamente

---

## **ESCENARIO 5: GENERACIÓN DE URL DE DESCARGA** 📥

### **Paso 1: Generar URL**

📁 **4. Descarga** → **Generar URL de Descarga**

**Resultado Esperado**: `200 OK`
```json
{
  "download_url": "https://storage-demo.example.com/...",
  "validation_status": "A",
  "document_name": "documento_1729845123456.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 123456
}
```

✅ URL mock (modo demo sin S3)
✅ Expira en 900 segundos (15 minutos)
✅ Se registra la descarga en auditoría

---

## 📊 RESUMEN DE ESTADOS

| Estado | Código | Descripción |
|--------|--------|-------------|
| PENDING | P | Esperando aprobación |
| APPROVED | A | Completamente aprobado |
| REJECTED | R | Rechazado (terminal) |
| null | - | Sin validación (no requiere aprobación) |

---

## 🎯 ENDPOINTS PRINCIPALES

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/token/` | POST | Obtener JWT |
| `/api/documents/` | GET | Listar documentos |
| `/api/documents/` | POST | Crear documento |
| `/api/documents/{id}/` | GET | Ver documento específico |
| `/api/documents/{id}/approve/` | POST | Aprobar documento |
| `/api/documents/{id}/reject/` | POST | Rechazar documento |
| `/api/documents/{id}/audit/` | GET | Ver auditoría |
| `/api/documents/{id}/download/` | GET | Generar URL de descarga |

---

## 🔑 CARACTERÍSTICAS CLAVE

### **1. Multi-tenancy**
- Cada empresa tiene sus propios documentos aislados
- Control de acceso por memberships

### **2. Aprobación en Cascada** ⭐
- CEO puede aprobar directamente sin pasar por niveles inferiores
- Ideal para casos de emergencia o autoridad total

### **3. Auditoría Inmutable**
- Cada acción queda registrada (quién, qué, cuándo)
- Incluye cambios de estado y razones

### **4. Validación Flexible**
- Documentos CON validación (flujo jerárquico)
- Documentos SIN validación (disponibles inmediatamente)

### **5. Estado Terminal**
- Documentos rechazados no pueden ser aprobados
- Previene conflictos de estado

---

## 🚨 TROUBLESHOOTING

### **Token Expirado**
**Error**: `401 Unauthorized`  
**Solución**: Volver a ejecutar "Obtener Token JWT"

### **Documento No Encontrado**
**Error**: `404 Not Found`  
**Solución**: Verificar que `document_id` esté actualizado en las variables de Postman

### **Empresa No Encontrada**
**Error**: `404 Empresa no encontrada`  
**Solución**: Verificar que el usuario tenga membership con la empresa

### **500 Internal Server Error**
**Solución**: Verificar que el deployment en Railway esté ACTIVE

---

## 📝 NOTAS ADICIONALES

### **Modo Demo (STORAGE_PROVIDER=LOCAL)**
- No requiere configurar AWS S3
- URLs de descarga son mock (ejemplo)
- Perfecto para demostraciones

### **Nombres Únicos Automáticos**
- Los documentos se crean con timestamp en el nombre
- No hay duplicados nunca
- Ejemplo: `documento_1729845123456.pdf`

### **Timestamps en Requests**
- Pre-request scripts generan valores únicos
- No necesitas cambiar manualmente los nombres

---

## ✅ CHECKLIST PREVIO A LA DEMO

- [ ] Deployment en Railway está ACTIVE
- [ ] Colección de Postman importada
- [ ] Token JWT obtenido (válido)
- [ ] Base de datos limpia (sin documentos de prueba)
- [ ] Variables de Postman configuradas

---

## 🎥 FLUJO SUGERIDO PARA VIDEO

1. **Introducción** (30 seg)
   - Mostrar arquitectura (Django + PostgreSQL + Railway)
   
2. **Autenticación** (30 seg)
   - Login y obtención de token

3. **Crear Documento** (1 min)
   - Mostrar creación con validación de 3 niveles
   - Explicar flujo jerárquico

4. **Aprobación en Cascada** (1 min) ⭐
   - Juan aprueba → Todos los niveles se aprueban automáticamente
   - Mostrar auditoría

5. **Rechazo** (30 seg)
   - Crear documento y rechazarlo
   - Intentar aprobar (debe fallar)

6. **Auditoría** (30 seg)
   - Mostrar historial completo de cambios

7. **Cierre** (30 seg)
   - Resumen de características

**Tiempo Total**: ~5 minutos

---

## 🏆 CONCLUSIÓN

El sistema demuestra:
- ✅ Autenticación y autorización robusta
- ✅ Flujos de validación jerárquicos flexibles
- ✅ Aprobación en cascada (feature avanzada)
- ✅ Auditoría inmutable
- ✅ Multi-tenancy con control de acceso
- ✅ API RESTful completa y documentada

---

**¡Éxito con tu demo!** 🚀
