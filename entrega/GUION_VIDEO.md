# 🎬 GUION DETALLADO DEL VIDEO - ERP DOCUMENTS API

**Duración Total**: 5-7 minutos  
**Objetivo**: Demostrar el sistema de gestión documental con validación jerárquica

---

## 🎯 ESTRUCTURA DEL VIDEO

### **INTRODUCCIÓN** (30 segundos)
### **DEMO TÉCNICA** (4-5 minutos)
### **CIERRE** (30 segundos)

---

## 📝 GUION COMPLETO

---

## **PARTE 1: INTRODUCCIÓN** (30 segundos)

### 🎤 **Lo que vas a decir:**

> "Hola, soy Julián González y les voy a presentar el sistema ERP Documents, una API REST desarrollada en Django que permite gestionar documentos empresariales con flujos de validación jerárquica.
> 
> El sistema cuenta con autenticación JWT, multi-tenancy para múltiples empresas, y una característica especial: la aprobación en cascada, donde un CEO puede aprobar un documento y automáticamente se aprueban todos los niveles inferiores.
> 
> El proyecto está desplegado en Railway con PostgreSQL y usa AWS S3 para almacenamiento de archivos. Vamos a verlo en acción."

### 📹 **Lo que vas a mostrar:**

- Tu pantalla con Postman abierto
- Puedes mencionar la arquitectura: Django + PostgreSQL + Railway

---

## **PARTE 2: AUTENTICACIÓN** (30 segundos)

### 🎤 **Lo que vas a decir:**

> "Primero, necesitamos autenticarnos. El sistema usa JWT (JSON Web Tokens) para la autenticación.
> 
> Voy a hacer login con el usuario 'admin' y contraseña 'admin123'."

### 📹 **Lo que vas a hacer:**

1. **Abrir Postman** → Carpeta "1. Autenticación"
2. **Seleccionar**: "Obtener Token JWT"
3. **Mostrar el body**:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. **Hacer clic en "Send"**
5. **Mostrar la respuesta** (200 OK con access y refresh tokens)

### 🎤 **Lo que vas a decir:**

> "Como pueden ver, recibimos un token de acceso que se guarda automáticamente en las variables de Postman y vamos a usar en todas las siguientes peticiones."

---

## **PARTE 3: CREAR DOCUMENTO CON VALIDACIÓN** (1 minuto)

### 🎤 **Lo que vas a decir:**

> "Ahora voy a crear un documento que requiere validación de 3 niveles jerárquicos:
> - Nivel 1: Sebastian, el Supervisor
> - Nivel 2: Camilo, el Gerente  
> - Nivel 3: Juan, el CEO
> 
> El sistema permite configurar flujos de aprobación flexibles según la jerarquía de la empresa."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: Carpeta "2. Documentos"
2. **Seleccionar**: "Crear Documento CON Validación (3 niveles)"
3. **Mostrar el body** (resaltar `validation_flow`):
   ```json
   {
     "company_id": "9da4abe9-57c7-4d76-ad5c-5e01d554f2c5",
     "entity": {
       "entity_type": "vehicle",
       "entity_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
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
         {"order": 1, "approver_user_id": 9},
         {"order": 2, "approver_user_id": 10},
         {"order": 3, "approver_user_id": 11}
       ]
     }
   }
   ```
4. **Hacer clic en "Send"**
5. **Mostrar la respuesta** (201 Created)
6. **Resaltar**: `"validation_status": "P"` (PENDING)

### 🎤 **Lo que vas a decir:**

> "El documento se creó exitosamente con estado PENDING, lo que significa que está esperando las aprobaciones de los 3 niveles."

---

## **PARTE 4: VERIFICAR DOCUMENTOS PENDIENTES** (20 segundos)

### 🎤 **Lo que vas a decir:**

> "Podemos verificar que el documento está pendiente de aprobación consultando todos los documentos con estado PENDING."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: "Listar Documentos PENDIENTES"
2. **Hacer clic en "Send"**
3. **Mostrar la respuesta** (debe aparecer el documento recién creado)

### 🎤 **Lo que vas a decir:**

> "Aquí vemos nuestro documento esperando aprobación."

---

## **PARTE 5: APROBACIÓN EN CASCADA** ⭐ (1 minuto 30 segundos)

### 🎤 **Lo que vas a decir:**

> "Ahora viene la característica más interesante del sistema: la aprobación en cascada.
> 
> Cuando un aprobador de nivel superior, como el CEO que está en el orden 3, aprueba un documento, automáticamente se aprueban todos los niveles inferiores. Esto es útil en casos de emergencia o cuando el CEO tiene autoridad total para aprobar directamente.
> 
> Voy a aprobar el documento como Juan, el CEO."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: Carpeta "3. Validación"
2. **Seleccionar**: "Aprobar - Juan (Orden 3) - CASCADA"
3. **Mostrar el body**:
   ```json
   {
     "actor_user_id": 11,
     "reason": "Aprobado por CEO - cumple todos los requisitos"
   }
   ```
4. **Hacer clic en "Send"**
5. **Mostrar la respuesta** (200 OK)
6. **Resaltar**: `"validation_status": "A"` (APPROVED)

### 🎤 **Lo que vas a decir:**

> "Como pueden ver, el documento pasó directo de PENDING a APPROVED. Vamos a ver la auditoría para confirmar que se aprobaron automáticamente los 3 niveles."

---

## **PARTE 6: VER AUDITORÍA** (1 minuto)

### 🎤 **Lo que vas a decir:**

> "El sistema mantiene un registro de auditoría inmutable de todas las acciones. Vamos a ver el historial completo de este documento."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: "Auditoría - Historial del Documento"
2. **Hacer clic en "Send"**
3. **Mostrar la respuesta**
4. **Resaltar los registros** de auditoría:
   - CREATE (estado inicial PENDING)
   - APPROVE orden 1 (Sebastian) - auto-aprobado
   - APPROVE orden 2 (Camilo) - auto-aprobado
   - APPROVE orden 3 (Juan) - aprobado manualmente

### 🎤 **Lo que vas a decir:**

> "Aquí podemos ver el registro completo:
> - Primero se creó el documento en estado PENDING
> - Luego, cuando Juan aprobó, se generaron automáticamente las aprobaciones de Sebastian (orden 1) y Camilo (orden 2) con la razón 'Auto-aprobado por cascada'
> - Finalmente, la aprobación manual de Juan
> 
> Cada registro incluye el usuario que realizó la acción, el timestamp exacto, y la razón de la aprobación."

---

## **PARTE 7: RECHAZO DE DOCUMENTO** (1 minuto)

### 🎤 **Lo que vas a decir:**

> "Ahora voy a demostrar el flujo de rechazo. Primero creo otro documento con validación."

### 📹 **Lo que vas a hacer:**

1. **Volver a**: "Crear Documento CON Validación (3 niveles)"
2. **Hacer clic en "Send"** (se creará con nombre único automático)
3. **Mostrar**: documento creado con estado PENDING

### 🎤 **Lo que vas a decir:**

> "Ahora Camilo, el gerente, va a rechazar este documento porque le falta documentación."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: "Rechazar Documento"
2. **Mostrar el body**:
   ```json
   {
     "actor_user_id": 10,
     "reason": "Documento ilegible - falta firma del representante legal"
   }
   ```
3. **Hacer clic en "Send"**
4. **Mostrar la respuesta**: `"validation_status": "R"` (REJECTED)

### 🎤 **Lo que vas a decir:**

> "El documento pasó a estado REJECTED, que es un estado terminal. Esto significa que no se puede aprobar después de haber sido rechazado. Es una medida de seguridad para evitar conflictos de estado."

---

## **PARTE 8: LISTAR DOCUMENTOS FINALES** (30 segundos)

### 🎤 **Lo que vas a decir:**

> "Finalmente, vamos a ver todos los documentos de la empresa para verificar los estados finales."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: "Listar Documentos"
2. **Hacer clic en "Send"**
3. **Mostrar la respuesta** con los documentos:
   - Documento 1: APPROVED (aprobado en cascada)
   - Documento 2: REJECTED (rechazado por Camilo)

### 🎤 **Lo que vas a decir:**

> "Aquí vemos nuestros dos documentos: uno aprobado y otro rechazado. El sistema mantiene el historial completo de ambos para fines de auditoría."

---

## **PARTE 9: CIERRE** (30 segundos)

### 🎤 **Lo que vas a decir:**

> "En resumen, el sistema ERP Documents ofrece:
> 
> ✅ Autenticación robusta con JWT  
> ✅ Flujos de validación jerárquicos configurables  
> ✅ Aprobación en cascada para casos especiales  
> ✅ Auditoría inmutable de todas las acciones  
> ✅ Multi-tenancy con control de acceso por empresa  
> ✅ Estado terminal para documentos rechazados  
> 
> El código está desplegado en Railway, usa PostgreSQL como base de datos, y está preparado para integración con AWS S3 para almacenamiento de archivos.
> 
> Todo el código está disponible en mi repositorio de GitHub. Gracias por ver esta demostración."

### 📹 **Lo que vas a mostrar:**

- Puedes mostrar brevemente el README del proyecto
- O la URL de Railway funcionando

---

## 📋 CHECKLIST PRE-GRABACIÓN

Antes de empezar a grabar, verifica:

- [ ] Railway deployment está **ACTIVE**
- [ ] Base de datos está **limpia** (0 documentos)
- [ ] Postman tiene la **colección importada**
- [ ] Token JWT está **obtenido y válido**
- [ ] Tienes el instructivo abierto de referencia
- [ ] Grabador de pantalla configurado
- [ ] Audio funcionando correctamente

---

## 💡 CONSEJOS PARA LA GRABACIÓN

### **Audio**
- Habla con claridad y ritmo tranquilo
- Usa un micrófono decente (no el del laptop si es malo)
- Graba en un lugar silencioso

### **Video**
- Resolución mínima: 1920x1080 (Full HD)
- Usa OBS Studio o similar para grabar pantalla
- Zoom al área de Postman cuando sea necesario

### **Ritmo**
- No tengas prisa, toma 5-7 minutos
- Pausa 2-3 segundos después de cada acción
- Da tiempo a que se vean las respuestas

### **Errores**
- Si cometes un error, no pares la grabación
- Puedes editar después o simplemente rehacer esa sección
- Mantén la calma y continúa

---

## 🎯 PUNTOS CLAVE A DESTACAR

### **1. Aprobación en Cascada** ⭐
> "Esta es la característica más importante: cuando el CEO aprueba, automáticamente aprueba todos los niveles inferiores"

### **2. Auditoría Inmutable**
> "Cada acción queda registrada con usuario, timestamp y razón. Esto es crucial para compliance y trazabilidad"

### **3. Estado Terminal**
> "Los documentos rechazados no pueden ser aprobados después, evitando conflictos de estado"

### **4. Multi-tenancy**
> "Cada empresa tiene sus documentos completamente aislados con control de acceso"

---

## ⏱️ TIMING SUGERIDO

| Sección | Tiempo | Acumulado |
|---------|--------|-----------|
| Introducción | 30s | 0:30 |
| Autenticación | 30s | 1:00 |
| Crear documento | 1m | 2:00 |
| Ver pendientes | 20s | 2:20 |
| Aprobar cascada | 1m 30s | 3:50 |
| Ver auditoría | 1m | 4:50 |
| Rechazar documento | 1m | 5:50 |
| Listar finales | 30s | 6:20 |
| Cierre | 30s | 6:50 |

**Total**: ~7 minutos (perfecto para una demo completa)

---

## 🎬 ALTERNATIVA CORTA (3-4 MINUTOS)

Si necesitas una versión más corta, enfócate en:

1. **Introducción** (20s)
2. **Login** (20s)
3. **Crear documento** (40s)
4. **Aprobar en cascada** (1m)
5. **Ver auditoría** (1m)
6. **Cierre** (20s)

**Total**: ~3.5 minutos

---

## ✅ DESPUÉS DE GRABAR

1. Revisa el video completo
2. Verifica que el audio se escuche bien
3. Confirma que todas las respuestas sean visibles
4. Edita si es necesario (cortar silencios largos, errores, etc.)
5. Exporta en buena calidad (1080p, H.264)

---

## 🚀 ¡MUCHA SUERTE CON TU VIDEO!

Recuerda:
- 📖 Tienes el **INSTRUCTIVO_DEMO.md** como referencia
- 📦 Tienes el **Postman Collection** listo
- 🎬 Tienes este **GUION** detallado

**¡Todo está preparado para que hagas una excelente demostración!** 🎉
