# 🎬 GUION DETALLADO DEL VIDEO - SUSTENTACIÓN Y DEMO

**Duración Total**: 8-10 minutos  
**Objetivo**: Explicar cómo se realizó la prueba técnica y demostrar el funcionamiento del sistema

---

## 🎯 ESTRUCTURA DEL VIDEO

### **PARTE 1: INTRODUCCIÓN Y CONTEXTO** (1 minuto)
### **PARTE 2: EXPLICACIÓN DE LA SOLUCIÓN** (2-3 minutos)
### **PARTE 3: DEMO EN VIVO** (4-5 minutos)
### **PARTE 4: CIERRE** (1 minuto)

---

## 📝 GUION COMPLETO

---

## **PARTE 1: INTRODUCCIÓN Y CONTEXTO** (1 minuto)

### 🎤 **Lo que vas a decir:**

> "Hola, soy Julián González y este es mi video de sustentación para la prueba técnica Backend.
> 
> El desafío consistía en desarrollar una API REST para gestionar documentos empresariales con flujos de validación jerárquica. Los documentos debían poder ser aprobados o rechazados por múltiples niveles de aprobadores según la estructura organizacional de cada empresa.
> 
> Voy a explicar primero cómo abordé la solución, las tecnologías que utilicé y las decisiones de diseño más importantes. Luego les mostraré el sistema funcionando en vivo."

### 📹 **Lo que vas a mostrar:**

- Tu pantalla (puede ser el README del proyecto o el código abierto en VS Code)

---

## **PARTE 2: EXPLICACIÓN DE LA SOLUCIÓN** (2-3 minutos)

### 🎤 **Sección 2.1: Arquitectura General** (1 minuto)

> "Para resolver este problema, diseñé una arquitectura basada en Django REST Framework con los siguientes componentes principales:
> 
> **Backend**: Django 5.0.1 con Django REST Framework
> - Elegí Django por su robustez, el ORM potente, y las capacidades de migración de base de datos
> 
> **Autenticación**: JWT usando Simple JWT
> - Implementé autenticación basada en tokens para APIs stateless y escalables
> 
> **Base de datos**: PostgreSQL en Railway
> - Usé PostgreSQL por su soporte robusto de transacciones y relaciones complejas
> 
> **Despliegue**: Railway con variables de entorno
> - Railway me permitió desplegar rápidamente con integración continua desde GitHub
> 
> **Almacenamiento**: AWS S3 (modo demo)
> - Diseñé la integración con S3, aunque en esta demo uso URLs simuladas"

### 📹 **Lo que vas a mostrar:**

- Puedes mostrar el archivo `settings.py` brevemente
- O un diagrama si lo tienes preparado

---

### 🎤 **Sección 2.2: Modelo de Datos** (1 minuto)

> "El modelo de datos tiene varias entidades clave:
> 
> **1. Company**: Representa cada empresa en el sistema multi-tenant
> 
> **2. User**: Los usuarios del sistema con autenticación
> 
> **3. Membership**: Relaciona usuarios con empresas (un usuario puede pertenecer a varias empresas)
> 
> **4. Document**: El documento en sí, con información de entidad asociada, bucket key para S3, y estado de validación
> 
> **5. ValidationFlow**: El flujo de aprobación configurado para cada documento
> 
> **6. ValidationStep**: Cada paso del flujo con su orden y aprobador asignado
> 
> **7. ValidationInstance**: Representa el estado actual de cada paso (pendiente, aprobado, rechazado)
> 
> **8. DocumentAudit**: Registro inmutable de todas las acciones sobre el documento
> 
> Este diseño permite tener flujos de aprobación completamente flexibles y configurables por documento."

### 📹 **Lo que vas a mostrar:**

- Puedes mostrar el archivo `models.py` con los modelos
- O mostrar las tablas en Railway Database

---

### 🎤 **Sección 2.3: Características Destacadas** (30 segundos)

> "Implementé tres características que considero destacadas:
> 
> **1. Aprobación en Cascada**: Cuando un aprobador de nivel superior aprueba, automáticamente se aprueban todos los niveles inferiores. Esto es útil para casos de emergencia o cuando el CEO tiene autoridad total.
> 
> **2. Estados Terminales**: Un documento rechazado no puede ser aprobado después, evitando conflictos de estado y garantizando integridad.
> 
> **3. Auditoría Inmutable**: Cada acción queda registrada con actor, timestamp y razón para compliance y trazabilidad completa.
> 
> Ahora vamos a ver todo esto funcionando en vivo."

### 📹 **Lo que vas a mostrar:**

- Transición a Postman para la demo

---

## **PARTE 3: DEMO EN VIVO** (4-5 minutos)

---

## **DEMO 3.1: AUTENTICACIÓN** (30 segundos)

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

## **DEMO 3.2: CREAR DOCUMENTO CON VALIDACIÓN** (1 minuto)

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

## **DEMO 3.3: VERIFICAR DOCUMENTOS PENDIENTES** (20 segundos)

### 🎤 **Lo que vas a decir:**

> "Podemos verificar que el documento está pendiente de aprobación consultando todos los documentos con estado PENDING."

### 📹 **Lo que vas a hacer:**

1. **Ir a**: "Listar Documentos PENDIENTES"
2. **Hacer clic en "Send"**
3. **Mostrar la respuesta** (debe aparecer el documento recién creado)

### 🎤 **Lo que vas a decir:**

> "Aquí vemos nuestro documento esperando aprobación."

---

## **DEMO 3.4: APROBACIÓN EN CASCADA** ⭐ (1 minuto 30 segundos)

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

## **DEMO 3.5: VER AUDITORÍA** (1 minuto)

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

## **DEMO 3.6: RECHAZO DE DOCUMENTO** (1 minuto)

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

## **DEMO 3.7: LISTAR DOCUMENTOS FINALES** (30 segundos)

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

## **PARTE 4: CIERRE Y CONCLUSIONES** (1 minuto)

### 🎤 **Lo que vas a decir:**

> "Para resumir, la solución que implementé cumple con todos los requisitos de la prueba técnica:
> 
> **✅ Funcionalidades Core:**
> - Autenticación robusta con JWT
> - CRUD completo de documentos
> - Flujos de validación jerárquicos configurables
> - Aprobación y rechazo con control de permisos
> - Auditoría inmutable de todas las acciones
> 
> **✅ Características Adicionales:**
> - Multi-tenancy con control de acceso por empresa
> - Aprobación en cascada para casos especiales
> - Estados terminales para evitar conflictos
> - Integración preparada con AWS S3
> - Validación de permisos (solo el aprobador asignado puede aprobar)
> 
> **✅ Aspectos Técnicos:**
> - Código limpio y bien estructurado siguiendo mejores prácticas
> - Migraciones de base de datos versionadas
> - Variables de entorno para configuración
> - Desplegado en producción y funcionando
> 
> El código completo está en GitHub y la API está desplegada en Railway lista para usar.
> 
> Gracias por su tiempo. Quedo atento a cualquier pregunta o feedback."

### 📹 **Lo que vas a mostrar:**

- Puedes mostrar brevemente:
  - La URL de Railway funcionando
  - El repositorio de GitHub
  - O simplemente tu rostro hablando a cámara

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

## 🎯 PUNTOS CLAVE PARA LA SUSTENTACIÓN

### **1. Decisiones de Diseño** 💡
> "Elegí Django por su ORM robusto y capacidades de migración. El modelo de ValidationFlow separado de ValidationInstance permite reusabilidad y flexibilidad."

### **2. Aprobación en Cascada** ⭐
> "Esta es la característica estrella: cuando el CEO aprueba, automáticamente aprueba todos los niveles inferiores. La implementé con una query que actualiza todos los steps con order menor al del aprobador."

### **3. Auditoría Inmutable**
> "Cada acción crea un registro en DocumentAudit que nunca se elimina ni modifica. Esto es crucial para compliance y permite trazabilidad completa de quién hizo qué y cuándo."

### **4. Estados Terminales**
> "Los documentos rechazados no pueden ser aprobados después. Esto se valida a nivel de API y evita conflictos de estado."

### **5. Multi-tenancy**
> "Cada empresa tiene sus documentos completamente aislados. Los usuarios solo ven documentos de empresas a las que pertenecen vía Membership."

### **6. Desafíos Superados** 🚀
> "El principal desafío fue diseñar el modelo de validación que permitiera tanto aprobación secuencial como en cascada. Lo resolví con ValidationInstance que trackea el estado de cada step independientemente."

---

## ⏱️ TIMING SUGERIDO (VERSIÓN COMPLETA)

| Sección | Tiempo | Acumulado |
|---------|--------|-----------|
| **PARTE 1: INTRODUCCIÓN** |
| Presentación y contexto | 1m | 1:00 |
| **PARTE 2: EXPLICACIÓN** |
| Arquitectura general | 1m | 2:00 |
| Modelo de datos | 1m | 3:00 |
| Características destacadas | 30s | 3:30 |
| **PARTE 3: DEMO** |
| Autenticación | 30s | 4:00 |
| Crear documento | 1m | 5:00 |
| Ver pendientes | 20s | 5:20 |
| Aprobar cascada | 1m 30s | 6:50 |
| Ver auditoría | 1m | 7:50 |
| Rechazar documento | 1m | 8:50 |
| Listar finales | 30s | 9:20 |
| **PARTE 4: CIERRE** |
| Conclusiones | 1m | 10:20 |

**Total**: ~10 minutos (ideal para sustentación completa)

---

## 🎬 VERSIÓN CORTA (5-6 MINUTOS)

Si necesitas una versión más corta para la sustentación:

| Sección | Tiempo |
|---------|--------|
| Introducción + explicación rápida | 1m 30s |
| Login | 20s |
| Crear documento | 40s |
| Aprobar en cascada | 1m |
| Ver auditoría | 1m |
| Rechazar documento (opcional) | 40s |
| Cierre | 30s |

**Total**: ~5.5 minutos

### 🎤 **Script versión corta:**

> "Desarrollé una API REST en Django con validación jerárquica de documentos. Destaca la aprobación en cascada donde un CEO puede aprobar todos los niveles automáticamente. Usa JWT, PostgreSQL, está desplegada en Railway y tiene auditoría completa. Vamos a verlo funcionando..."

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
