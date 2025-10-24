# 🧪 PASO 2: PRUEBAS CON POSTMAN

> **Requisito:** Haber completado el PASO 1 (servidor Django corriendo)

---

## ⏱️ Tiempo estimado: 15-20 minutos

---

## 📋 Pre-requisitos

- [ ] Servidor Django corriendo (de PASO_1_CONFIGURACION.md)
- [ ] Postman instalado (descarga de: https://www.postman.com/downloads/)
- [ ] Los IDs que copiaste en el PASO 1

---

## 🚀 Paso a Paso - PRUEBAS CON POSTMAN

### 1️⃣ Abrir Postman

**Si es tu primera vez:**
- Puedes saltarte el login (hay una X arriba a la derecha)
- O crear una cuenta gratuita (recomendado para guardar tu trabajo)

---

### 2️⃣ Importar la Colección

**Paso por paso:**

1. **Click en "Import"** (arriba a la izquierda, botón naranja)

2. **Click en "Upload Files"**

3. **Navega a:** 
   ```
   C:\Users\Desktop\Documents\Julian\GitHub\PruebaTecnicaBackend\entrega\
   ```

4. **Selecciona:** `ERP_Documents_Postman_Collection.json`

5. **Click en "Import"**

**✅ Sabrás que funcionó si ves:**
- Una nueva colección llamada **"ERP Documents - Demo"** en el panel izquierdo
- Con 4 carpetas: Authentication, Documents, Validation, Download

---

### 3️⃣ Configurar las Variables de la Colección

**Esto es CRÍTICO - aquí pones los IDs que copiaste:**

1. **Click en la colección "ERP Documents - Demo"** (nombre principal)

2. **Click en la pestaña "Variables"** (arriba)

3. **Reemplaza los valores** con los IDs que copiaste del PASO 1:

| Variable | Valor Actual | Tu Valor (ejemplo) |
|----------|--------------|-------------------|
| `base_url` | http://localhost:8000 | **NO CAMBIES** |
| `token` | (vacío) | **NO CAMBIES** (se llena solo) |
| `company_id` | TU-COMPANY-ID-AQUI | **PEGA TU ID aquí** |
| `user_sebastian` | 2 | **PEGA TU ID aquí** |
| `user_camilo` | 3 | **PEGA TU ID aquí** |
| `user_juan` | 4 | **PEGA TU ID aquí** |
| `vehicle_id` | aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee | **NO CAMBIES** |
| `document_id` | (vacío) | **NO CAMBIES** (se llena solo) |

**Ejemplo de cómo se vería:**
```
company_id = ebbc771d-86ea-404e-b69e-20bd0511b1c8
user_sebastian = 1
user_camilo = 2
user_juan = 3
```

4. **Click en "Save"** (arriba a la derecha, botón azul)

---

### 4️⃣ Ejecutar las Pruebas EN ORDEN

**⚠️ IMPORTANTE:** Debes ejecutar los requests **EN ESTE ORDEN** porque cada uno depende del anterior.

---

#### 📤 REQUEST 1: Obtener Token (Autenticación)

**Ubicación:** `ERP Documents - Demo → Authentication → 1. Login - Get JWT Token`

**Qué hace:** Te da un token de autenticación para usar en todos los demás requests.

**Paso a paso:**
1. Click en **"1. Login - Get JWT Token"**
2. **Revisa el Body:** 
   - Username: `uploader`
   - Password: `test123`
3. **Click en "Send"** (botón azul grande)

**✅ Resultado esperado:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**🎉 El token se guarda automáticamente en las variables** - No necesitas copiarlo manualmente.

**❌ Si ves un error:**
- Verifica que el servidor Django esté corriendo
- Ve a http://127.0.0.1:8000/admin/ en tu navegador (debe cargar)

---

#### 📄 REQUEST 2: Listar Documentos

**Ubicación:** `ERP Documents - Demo → Documents → 2. List Documents`

**Qué hace:** Lista todos los documentos (debería estar vacío la primera vez).

**Paso a paso:**
1. Click en **"2. List Documents"**
2. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

Esto significa: "No hay documentos todavía" ✅

---

#### 📝 REQUEST 3: Crear Documento SIN Validación

**Ubicación:** `ERP Documents - Demo → Documents → 3. Create Document (No Validation)`

**Qué hace:** Crea un documento simple que NO requiere aprobaciones.

**Paso a paso:**
1. Click en **"3. Create Document (No Validation)"**
2. **Revisa el Body** (puedes modificar el `bucket_key` si quieres):
   ```json
   {
       "company": "{{company_id}}",
       "uploaded_by": "{{user_sebastian}}",
       "content_type": 9,
       "object_id": "{{vehicle_id}}",
       "bucket_provider": "s3",
       "bucket_key": "docs/manual_usuario.pdf"
   }
   ```
3. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "id": 1,
    "company": "...",
    "uploaded_by": 1,
    "bucket_provider": "s3",
    "bucket_key": "docs/manual_usuario.pdf",
    "validation_status": "approved",  ← Sin validación = auto-aprobado
    "created_at": "2025-10-23T17:30:00Z"
}
```

**Estado:** `approved` (aprobado automáticamente porque no tiene flujo de validación)

---

#### 📋 REQUEST 4: Crear Documento CON Validación de 3 Niveles

**Ubicación:** `ERP Documents - Demo → Documents → 4. Create Document (With 3-Level Validation)`

**Qué hace:** Crea un documento que REQUIERE 3 aprobaciones en cascada.

**Paso a paso:**
1. Click en **"4. Create Document (With 3-Level Validation)"**
2. **Revisa el Body** - Este es más complejo:
   ```json
   {
       "company": "{{company_id}}",
       "uploaded_by": "{{user_sebastian}}",
       "content_type": 9,
       "object_id": "{{vehicle_id}}",
       "bucket_provider": "s3",
       "bucket_key": "docs/soat_2024.pdf",
       "validation_config": {
           "flow_name": "Aprobación SOAT",
           "steps": [
               {
                   "name": "Supervisor",
                   "order": 1,
                   "approver_id": "{{user_sebastian}}"
               },
               {
                   "name": "Gerente",
                   "order": 2,
                   "approver_id": "{{user_camilo}}"
               },
               {
                   "name": "Director",
                   "order": 3,
                   "approver_id": "{{user_juan}}"
               }
           ]
       }
   }
   ```
3. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "id": 2,
    "bucket_key": "docs/soat_2024.pdf",
    "validation_status": "pending_validation",  ← Esperando aprobación
    "validation_flow": {
        "id": 1,
        "name": "Aprobación SOAT",
        "status": "pending",
        "steps": [
            {
                "name": "Supervisor",
                "order": 1,
                "status": "pending",
                "approver_name": "sebastian"
            },
            {
                "name": "Gerente",
                "order": 2,
                "status": "pending",
                "approver_name": "camilo"
            },
            {
                "name": "Director",
                "order": 3,
                "status": "pending",
                "approver_name": "juan"
            }
        ]
    }
}
```

**🎉 El `document_id` se guarda automáticamente** - Lo usarás en los siguientes requests.

**Estado:** `pending_validation` (esperando aprobaciones)

---

#### ✅ REQUEST 5: Aprobar como Juan (Nivel 3) - CASCADA MÁGICA

**Ubicación:** `ERP Documents - Demo → Validation → 5. Approve Document (Juan - Level 3 CASCADE)`

**Qué hace:** 
- Juan (nivel MÁS ALTO - orden 3) aprueba el documento
- **AUTOMÁTICAMENTE aprueba niveles 1 y 2** (sebastian y camilo)
- El documento pasa a estado `approved` (TERMINAL)

**⭐ ESTO ES LO MÁS IMPORTANTE DE TODO EL SISTEMA ⭐**

**Paso a paso:**
1. Click en **"5. Approve Document (Juan - Level 3 CASCADE)"**
2. **Revisa el Body:**
   ```json
   {
       "comments": "Documento aprobado por el director"
   }
   ```
3. **Nota:** Este request usa un token diferente (de Juan) para simular que es él quien aprueba
4. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "message": "Documento aprobado exitosamente",
    "document": {
        "id": 2,
        "validation_status": "approved",  ← AHORA ESTÁ APROBADO
        "validation_flow": {
            "status": "approved",
            "steps": [
                {
                    "name": "Supervisor",
                    "order": 1,
                    "status": "approved",  ← Aprobado automáticamente
                    "approver_name": "sebastian"
                },
                {
                    "name": "Gerente",
                    "order": 2,
                    "status": "approved",  ← Aprobado automáticamente
                    "approver_name": "camilo"
                },
                {
                    "name": "Director",
                    "order": 3,
                    "status": "approved",  ← Juan lo aprobó
                    "approver_name": "juan",
                    "approved_at": "2025-10-23T17:35:00Z"
                }
            ]
        }
    }
}
```

**🎉 ¡CASCADA EN ACCIÓN!**
- Juan (orden 3) aprobó
- Automáticamente aprobó a sebastian (orden 1) y camilo (orden 2)
- El documento está en estado TERMINAL: `approved`

---

#### 📊 REQUEST 6: Ver Historial de Auditoría

**Ubicación:** `ERP Documents - Demo → Validation → 6. Get Document Audit History`

**Qué hace:** Muestra TODO lo que ha pasado con el documento.

**Paso a paso:**
1. Click en **"6. Get Document Audit History"**
2. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "document_id": 2,
    "current_status": "approved",
    "state_audit": [
        {
            "changed_at": "2025-10-23T17:32:00Z",
            "previous_status": null,
            "new_status": "pending_validation",
            "changed_by": "uploader"
        },
        {
            "changed_at": "2025-10-23T17:35:00Z",
            "previous_status": "pending_validation",
            "new_status": "approved",
            "changed_by": "juan"
        }
    ],
    "validation_actions": [
        {
            "action": "approve",
            "step_name": "Director",
            "step_order": 3,
            "performed_by": "juan",
            "comments": "Documento aprobado por el director",
            "performed_at": "2025-10-23T17:35:00Z"
        }
    ]
}
```

**Esto muestra:**
- Cuándo se creó el documento
- Cuándo cambió de estado
- Quién hizo cada acción
- Los comentarios de cada aprobación

---

#### ❌ REQUEST 7: Intentar Rechazar (Verás un Error)

**Ubicación:** `ERP Documents - Demo → Validation → 7. Reject Document (Will Fail - Terminal State)`

**Qué hace:** Intenta rechazar un documento que ya está aprobado.

**Paso a paso:**
1. Click en **"7. Reject Document (Will Fail - Terminal State)"**
2. **Click en "Send"**

**✅ Resultado esperado (ERROR INTENCIONAL):**
```json
{
    "error": "El documento ya está en un estado terminal (approved)"
}
```

**¿Por qué falla?**
- Estados terminales = `approved` o `rejected`
- Una vez en estado terminal, **NO SE PUEDE CAMBIAR**
- Esto es una característica de seguridad del sistema

---

#### 📥 REQUEST 8: Generar URL de Descarga

**Ubicación:** `ERP Documents - Demo → Download → 8. Generate Download URL`

**Qué hace:** Genera una URL temporal (1 hora) para descargar el archivo de S3.

**Paso a paso:**
1. Click en **"8. Generate Download URL"**
2. **Click en "Send"**

**✅ Resultado esperado:**
```json
{
    "download_url": "https://bucket-name.s3.amazonaws.com/docs/soat_2024.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...",
    "expires_in": 3600,
    "file_key": "docs/soat_2024.pdf"
}
```

**Notas:**
- La URL es temporal (válida por 1 hora)
- Se registra en auditoría quién descargó el archivo
- En producción, esta URL llevaría al archivo real en S3

---

## ✅ Checklist de Pruebas Completadas

Marca cada request que hayas ejecutado exitosamente:

- [ ] 1. Login - Token obtenido
- [ ] 2. List Documents - Lista vacía o con documentos
- [ ] 3. Create Document (No Validation) - Creado con status `approved`
- [ ] 4. Create Document (With Validation) - Creado con status `pending_validation`
- [ ] 5. Approve (Juan - Cascade) - **TODOS los niveles aprobados automáticamente**
- [ ] 6. Audit History - Viste el historial completo
- [ ] 7. Reject (Error) - Viste el error de estado terminal
- [ ] 8. Download URL - Generaste URL temporal

---

## 🎯 Lo Que Acabas de Probar

✅ **Autenticación JWT** - Sistema de tokens seguro

✅ **Creación de documentos** - Con y sin validación

✅ **Aprobación en cascada** - La característica ESTRELLA del sistema:
   - Al aprobar nivel 3, automáticamente aprueba niveles 1 y 2
   - Lógica implementada en `validation/services.py`

✅ **Estados terminales** - Una vez aprobado/rechazado, no se puede cambiar

✅ **Auditoría completa** - Todo queda registrado (quién, cuándo, qué)

✅ **URLs prefirmadas** - Descargas seguras desde S3

---

## 📝 Notas Importantes para el Video

**Esto es lo que debes ENFATIZAR en tu video:**

1. **La cascada de aprobación** es la lógica central
   - Código en: `validation/services.py` líneas ~150-180

2. **Estados terminales** evitan cambios después de aprobar/rechazar
   - Seguridad del sistema

3. **Auditoría completa** - Trazabilidad total
   - DocumentStateAudit: cambios de estado
   - ValidationAction: acciones de validación
   - DocumentDownloadAudit: descargas

4. **Abstracción de storage** - Funciona con S3, GCS, o cualquier bucket
   - No guardamos archivos en DB, solo referencias

---

## 🎯 Siguiente Paso

**Ahora ve a:** `PASO_3_GUION_VIDEO.md`

Ahí está el guion COMPLETO de qué decir y hacer en tu video de 10 minutos.

---

## 🆘 Problemas Comunes

### "Could not send request"
- **Solución:** Verifica que el servidor Django esté corriendo en http://127.0.0.1:8000/

### "Invalid token" o "Authentication credentials were not provided"
- **Solución:** Ejecuta el Request 1 (Login) de nuevo para obtener un token fresco

### Las variables no se reemplazan (ves `{{company_id}}` en el Body)
- **Solución:** Asegúrate de haber guardado las variables en la colección (paso 3️⃣)

### No veo la respuesta que esperaba
- **Solución:** Lee el mensaje de error en la respuesta, generalmente explica qué falta

---

**¿Completaste todas las pruebas? ✅ Continúa con el PASO 3**
