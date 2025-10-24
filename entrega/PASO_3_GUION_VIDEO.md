# 🎬 PASO 3: GUION PARA VIDEO DE 10 MINUTOS

> **Requisito:** Haber completado PASO 1 y PASO 2 (conocer el sistema)

---

## ⏱️ Duración Total: 10 minutos exactos

**Estructura del video:**
- Introducción: 1 minuto
- Arquitectura (VS Code): 2 minutos  
- Demo en Postman: 4 minutos
- Código clave: 2 minutos
- Django Admin: 30 segundos
- Cierre: 30 segundos

---

## 📋 CHECKLIST PRE-GRABACIÓN (Hacer 5 minutos antes)

### ✅ Configuración Técnica

- [ ] **Servidor Django corriendo**
  ```powershell
  cd C:\Users\Desktop\Documents\Julian\GitHub\PruebaTecnicaBackend
  .venv\Scripts\Activate.ps1
  python manage.py runserver
  ```

- [ ] **Postman abierto** con la colección "ERP Documents - Demo"
  - Variables configuradas
  - Token de `uploader` listo (Request 1 ejecutado)
  - Token de `juan` listo (ejecutar Login con juan/test123 y copiar token manualmente)

- [ ] **VS Code abierto** en la carpeta del proyecto
  - Panel de archivos visible (lado izquierdo)
  - Ningún archivo abierto (cerrar todas las pestañas)

- [ ] **Navegador con pestaña del Django Admin**
  - http://127.0.0.1:8000/admin/
  - Ya logueado con admin/admin123

- [ ] **Grabadora de pantalla lista**
  - OBS Studio, Zoom, Loom, o cualquier herramienta
  - Audio funcionando
  - Cámara opcional (no necesaria)

- [ ] **Pantalla limpia**
  - Cerrar notificaciones
  - Cerrar aplicaciones innecesarias
  - Modo No Molestar activado
  - Ocultar barra de tareas si es posible

### ✅ Contenido Listo

- [ ] Este archivo abierto en otra pantalla o impreso
- [ ] Archivos clave identificados:
  - `validation/services.py` (líneas 140-180)
  - `documents/models.py` (líneas 1-50)
  - `validation/models.py` (líneas 1-80)

---

## 🎬 GUION MINUTO A MINUTO

---

## [0:00 - 1:00] INTRODUCCIÓN (1 minuto)

### 📺 Pantalla: Tu cara (opcional) o pantalla del proyecto en VS Code

### 🗣️ QUÉ DECIR (palabra por palabra):

> "Hola, buenos días/tardes. Mi nombre es [TU NOMBRE] y voy a presentar el sistema de gestión de documentos para ERP que desarrollé como prueba técnica.
>
> Este sistema implementa cinco características principales:
>
> **Uno:** Gestión de documentos con almacenamiento en buckets de S3 o Google Cloud Storage usando URLs prefirmadas para seguridad.
>
> **Dos:** Un flujo de validación jerárquico con aprobaciones en cascada, que es la característica central del sistema.
>
> **Tres:** Multi-tenancy por empresa, donde cada empresa tiene sus propios usuarios y documentos.
>
> **Cuatro:** Auditoría completa de todas las acciones: cambios de estado, aprobaciones y descargas.
>
> **Y cinco:** API REST completa con Django REST Framework y autenticación mediante JSON Web Tokens.
>
> La tecnología principal es Django 5 con PostgreSQL, y voy a demostrar el funcionamiento en vivo."

### ✋ QUÉ HACER:
- Habla con confianza pero natural
- No leas, habla como si explicaras a un colega
- Sonríe si tienes cámara
- Muestra entusiasmo pero profesional

---

## [1:00 - 3:00] ARQUITECTURA (2 minutos)

### 📺 Pantalla: VS Code con estructura de carpetas visible

### 🗣️ QUÉ DECIR:

> "Empecemos con la arquitectura del proyecto. Está organizado en aplicaciones de Django siguiendo el principio de separación de responsabilidades."

### ✋ QUÉ HACER:
1. **Muestra el panel de archivos** (lado izquierdo de VS Code)

---

### 📂 APP 1: CORE (30 segundos)

### 🗣️ QUÉ DECIR:

> "Primero tenemos la app **CORE**, que contiene los modelos base del sistema."

### ✋ QUÉ HACER:
1. **Click en la carpeta `core/`**
2. **Abre `core/models.py`**
3. **Scroll para mostrar las clases mientras hablas**

### 🗣️ QUÉ DECIR:

> "Aquí tenemos tres modelos fundamentales:
>
> **Company:** Representa cada empresa en el sistema multi-tenant. Cada empresa tiene sus propios datos aislados.
>
> **CompanyMembership:** La relación entre usuarios y empresas, donde se define el rol de cada usuario dentro de la empresa: puede ser APPROVER o UPLOADER.
>
> **Y AuditMixin:** Un mixin reutilizable que agrega campos de auditoría - created_at, updated_at, created_by, updated_by - a cualquier modelo que lo herede."

---

### 📂 APP 2: DOCUMENTS (45 segundos)

### 🗣️ QUÉ DECIR:

> "La segunda app es **DOCUMENTS**, el corazón del sistema."

### ✋ QUÉ HACER:
1. **Cierra `core/models.py`**
2. **Abre `documents/models.py`**
3. **Scroll para mostrar el modelo Document**

### 🗣️ QUÉ DECIR:

> "El modelo **Document** es clave. Fíjense que NO guardamos archivos binarios en la base de datos. En su lugar guardamos:
>
> - **bucket_provider:** Si es S3, Google Cloud Storage, u otro
> - **bucket_key:** La ruta del archivo en el bucket
> - **content_type y object_id:** Una referencia genérica a cualquier entidad del sistema - puede ser un vehículo, un empleado, lo que sea
> - **validation_status:** El estado actual del documento
>
> También tenemos **DocumentStateAudit** que registra cada cambio de estado del documento, y **DocumentDownloadAudit** que registra cada vez que alguien descarga un archivo."

---

### 📂 APP 3: VALIDATION (45 segundos)

### 🗣️ QUÉ DECIR:

> "Y la tercera app es **VALIDATION**, donde está la lógica de aprobaciones jerárquicas."

### ✋ QUÉ HACER:
1. **Cierra `documents/models.py`**
2. **Abre `validation/models.py`**
3. **Scroll para mostrar los modelos**

### 🗣️ QUÉ DECIR:

> "Aquí tenemos cuatro modelos:
>
> **ValidationFlow:** El flujo completo de validación asociado a un documento.
>
> **ValidationStep:** Cada paso del flujo con su orden jerárquico. Por ejemplo: orden 1 = Supervisor, orden 2 = Gerente, orden 3 = Director.
>
> **ValidationInstance:** La instancia activa del flujo mientras el documento está en validación.
>
> **Y ValidationAction:** Cada acción de aprobar o rechazar que toma un usuario.
>
> La magia está en la cascada: cuando un aprobador de nivel superior aprueba, automáticamente aprueba todos los niveles inferiores. Esto lo veremos en código en un momento."

---

## [3:00 - 7:00] DEMO EN POSTMAN (4 minutos)

### 📺 Pantalla: Postman abierto con la colección

### 🗣️ QUÉ DECIR:

> "Ahora voy a demostrar el sistema en funcionamiento usando Postman."

---

### 🔐 REQUEST 1: Autenticación (30 segundos)

### ✋ QUÉ HACER:
1. **Click en "1. Login - Get JWT Token"**
2. **Muestra el Body** (username: uploader, password: test123)
3. **Click en "Send"**

### 🗣️ QUÉ DECIR:

> "Primero nos autenticamos. Este request envía credenciales y recibe un JSON Web Token. Vean que el token se guarda automáticamente en las variables de la colección gracias a un script de Postman, y se usará en todos los demás requests."

---

### 📄 REQUEST 2: Listar Documentos (20 segundos)

### ✋ QUÉ HACER:
1. **Click en "2. List Documents"**
2. **Muestra que el header Authorization ya tiene el token**
3. **Click en "Send"**

### 🗣️ QUÉ DECIR:

> "Listamos los documentos existentes. Vean que el token va automáticamente en el header Authorization. Si ya hay documentos de pruebas anteriores, aquí aparecen."

---

### 📝 REQUEST 3: Crear Documento SIN Validación (30 segundos)

### ✋ QUÉ HACER:
1. **Click en "3. Create Document (No Validation)"**
2. **Muestra el Body** - señala los campos importantes
3. **Click en "Send"**
4. **Muestra la respuesta** - señala `validation_status: "approved"`

### 🗣️ QUÉ DECIR:

> "Creamos un documento simple. Vean que NO incluye validation_config. Este tipo de documento se aprueba automáticamente - su estado es 'approved' inmediatamente. Es útil para documentos que no requieren aprobación."

---

### 📋 REQUEST 4: Crear Documento CON Validación (1 minuto)

### ✋ QUÉ HACER:
1. **Click en "4. Create Document (With 3-Level Validation)"**
2. **Scroll en el Body para mostrar validation_config**
3. **Señala con el cursor los 3 pasos (orders 1, 2, 3)**
4. **Click en "Send"**
5. **Scroll en la respuesta para mostrar los 3 steps en "pending"**

### 🗣️ QUÉ DECIR:

> "Ahora creamos un documento que SÍ requiere validación. En el validation_config definimos tres pasos jerárquicos:
>
> Orden 1 es el Supervisor - Sebastian.
> Orden 2 es el Gerente - Camilo.
> Orden 3 es el Director - Juan.
>
> [Click en Send]
>
> Vean la respuesta: el validation_status es 'pending_validation', y en el validation_flow vemos los tres pasos, todos en estado 'pending'. Ninguno ha sido aprobado todavía."

---

### ✅ REQUEST 5: Aprobar con Cascada - ⭐ MOMENTO CLAVE (1 minuto 30 segundos)

### ✋ QUÉ HACER:
1. **Click en "5. Approve Document (Juan - Level 3 CASCADE)"**
2. **Muestra el Body** con el comentario
3. **Explica que este request usa el token de Juan (nivel 3)**
4. **Click en "Send"**
5. **Scroll LENTAMENTE en la respuesta**
6. **SEÑALA con el cursor cada step que cambió a "approved"**

### 🗣️ QUÉ DECIR:

> "Aquí viene la característica CENTRAL del sistema: la aprobación en cascada.
>
> Voy a aprobar el documento como Juan, que es el Director - el nivel MÁS ALTO con orden 3.
>
> [Click en Send]
>
> ¡Miren lo que pasó! 
>
> [Señala cada step mientras hablas]
>
> El step de orden 3 - Juan - está aprobado, porque él lo aprobó.
>
> PERO... el step de orden 2 - Camilo - TAMBIÉN está aprobado, automáticamente.
>
> Y el step de orden 1 - Sebastian - TAMBIÉN está aprobado, automáticamente.
>
> Esto es la CASCADA: cuando un aprobador de nivel superior aprueba, automáticamente aprueba todos los niveles inferiores a él. No necesitan aprobar Sebastian ni Camilo porque ya lo hizo alguien de mayor jerarquía.
>
> Y vean el validation_status del documento: ahora es 'approved'. Es un estado TERMINAL, no se puede cambiar más."

---

### 📊 REQUEST 6: Auditoría (40 segundos)

### ✋ QUÉ HACER:
1. **Click en "6. Get Document Audit History"**
2. **Click en "Send"**
3. **Scroll en la respuesta mostrando state_audit y validation_actions**

### 🗣️ QUÉ DECIR:

> "Ahora veamos el historial de auditoría. Aquí está TODO lo que pasó con el documento:
>
> En state_audit vemos los cambios de estado: de null a pending_validation, y luego a approved.
>
> En validation_actions vemos las acciones tomadas: Juan aprobó el step de orden 3 con su comentario.
>
> Todo queda registrado: quién, cuándo, qué hizo, y sus comentarios."

---

### ❌ REQUEST 7: Rechazar (Error Intencional) (30 segundos)

### ✋ QUÉ HACER:
1. **Click en "7. Reject Document (Will Fail)"**
2. **Click en "Send"**
3. **Muestra el error**

### 🗣️ QUÉ DECIR:

> "Ahora intentemos rechazar el documento. 
>
> [Click en Send]
>
> Vean el error: 'El documento ya está en un estado terminal'. Una vez que un documento está aprobado o rechazado, NO se puede cambiar más. Esto es una característica de seguridad del sistema para mantener la integridad de los registros."

---

## [7:00 - 9:00] CÓDIGO CLAVE (2 minutos)

### 📺 Pantalla: VS Code con el archivo de services

### 🗣️ QUÉ DECIR:

> "Ahora les muestro el código que hace posible la cascada de aprobación."

### ✋ QUÉ HACER:
1. **Vuelve a VS Code**
2. **Abre `validation/services.py`**
3. **Busca el método `approve_step`** (línea ~140)
4. **Scroll para mostrarlo completo**

---

### 📝 Explicación del Código (1 minuto 30 segundos)

### ✋ QUÉ HACER:
1. **Señala con el cursor cada sección mientras explicas**

### 🗣️ QUÉ DECIR:

> "Este es el método approve_step en la clase ValidationService. Veamos qué hace:
>
> [Señala la primera sección]
>
> Primero, aprueba el step actual del usuario que está aprobando. Cambia su status a 'approved' y guarda quién lo aprobó, cuándo, y sus comentarios.
>
> [Señala la sección de cascada]
>
> Luego viene la CASCADA. Busca todos los steps previos que estén pendientes - es decir, con un order menor al step actual y en estado 'pending'.
>
> Para cada uno de esos steps, los marca como 'approved' y los guarda. Esta es la magia: aprueba automáticamente todos los niveles inferiores.
>
> [Señala la sección de verificación]
>
> Después verifica si TODOS los steps del flujo están aprobados. Si es así, cambia el validation_status del documento a 'approved' y registra el cambio de estado en DocumentStateAudit.
>
> [Señala el return]
>
> Y finalmente registra la acción de validación y devuelve el resultado.
>
> Esta lógica hace que el sistema sea flexible: puedes tener 3, 5, 10 niveles de aprobación, y siempre funciona igual - un nivel superior puede aprobar por todos los inferiores."

---

### 🔄 Mención de Estados Terminales (30 segundos)

### ✋ QUÉ HACER:
1. **Scroll al método `reject_step`** (debajo de approve_step)

### 🗣️ QUÉ DECIR:

> "Y aquí abajo tenemos reject_step, que funciona similar pero marca el documento como 'rejected', que también es un estado TERMINAL.
>
> La validación de estados terminales está en las vistas: antes de permitir aprobar o rechazar, verifica que el documento NO esté ya en 'approved' o 'rejected'. Esto mantiene la integridad de los registros."

---

## [9:00 - 9:30] DJANGO ADMIN (30 segundos)

### 📺 Pantalla: Navegador con Django Admin

### 🗣️ QUÉ DECIR:

> "Rápidamente les muestro el panel de administración de Django."

### ✋ QUÉ HACER:
1. **Muestra la página principal del admin** (http://127.0.0.1:8000/admin/)
2. **Click en "Documents"** → **"Documents"**
3. **Muestra la lista de documentos**
4. **Click en uno de los documentos**
5. **Scroll para mostrar los campos**
6. **Vuelve atrás**
7. **Click en "Document state audits"**
8. **Muestra los registros de auditoría**

### 🗣️ QUÉ DECIR:

> "Desde el admin de Django podemos ver todos los registros. Aquí están los documentos con sus estados actuales.
>
> [Click en un documento]
>
> Vemos todos los detalles del documento.
>
> [Vuelve y abre Document state audits]
>
> Y aquí en Document State Audits vemos el historial completo de cambios con timestamps exactos. Todo queda registrado para auditorías."

---

## [9:30 - 10:00] CIERRE (30 segundos)

### 📺 Pantalla: VS Code con la estructura del proyecto o tu cara

### 🗣️ QUÉ DECIR:

> "Para resumir, este sistema implementa:
>
> **Uno:** Multi-tenancy por empresa con usuarios y roles.
>
> **Dos:** Almacenamiento abstracto en buckets con URLs prefirmadas para seguridad.
>
> **Tres:** Validación jerárquica con aprobación en cascada, que es la característica central.
>
> **Cuatro:** Estados terminales para mantener integridad de registros.
>
> **Cinco:** Y auditoría completa de todas las acciones.
>
> El código, la documentación, y la colección de Postman están disponibles en el repositorio.
>
> Gracias por su atención. Quedo atento a cualquier pregunta o comentario."

### ✋ QUÉ HACER:
- Sonríe
- Mantén contacto visual con la cámara (si tienes)
- Espera 2 segundos
- Detén la grabación

---

## ✅ CHECKLIST POST-GRABACIÓN

Antes de enviar el video, verifica:

- [ ] Duración entre 9:30 y 10:30 (máximo 11 minutos)
- [ ] Audio claro y sin ruido de fondo
- [ ] Pantalla legible (texto no muy pequeño)
- [ ] Mostraste la cascada de aprobación funcionando
- [ ] Mostraste el código de `approve_step`
- [ ] Explicaste los estados terminales
- [ ] Mencionaste la auditoría
- [ ] No hay interrupciones o distracciones visuales

---

## 💡 TIPS PARA HABLAR PROFESIONALMENTE

### ✅ HAZ:
- Habla pausado y claro
- Respira entre secciones
- Usa frases cortas
- Explica con tus propias palabras (no leas)
- Muestra entusiasmo por tu trabajo
- Si te trabas, respira y continúa (no es necesario reiniciar)

### ❌ EVITA:
- Hablar muy rápido
- Usar muletillas ("ehh", "mmm", "o sea", etc.)
- Leer textualmente
- Pedir disculpas por errores menores
- Explicaciones demasiado técnicas (asume que entienden Django)
- Divagar fuera del tema

---

## 🎯 LO MÁS IMPORTANTE A COMUNICAR

Si tuvieras que elegir solo 3 cosas para enfatizar en el video:

1. **La cascada de aprobación** - Es la característica única y principal
2. **Código limpio y bien estructurado** - Muestra profesionalismo
3. **Auditoría y seguridad** - Estados terminales, trazabilidad completa

---

## 🆘 PROBLEMAS DURANTE LA GRABACIÓN

### "Me trabé hablando"
- **Solución:** Respira, haz una pausa, y continúa. NO reinicies.

### "El servidor no responde"
- **Solución:** Pausa la grabación, reinicia el servidor, continúa.

### "Postman da error"
- **Solución:** Pausa la grabación, verifica el token, ejecuta Login de nuevo, continúa.

### "Me pasé de 10 minutos"
- **Solución:** Está bien hasta 11 minutos. Si te pasaste más, enfócate en hablar más conciso en las explicaciones de código.

### "Me quedé corto (menos de 9 minutos)"
- **Solución:** Agrega más detalle en la sección de código, o menciona casos de uso adicionales.

---

## 📊 ESTRUCTURA VISUAL RECOMENDADA

**Distribución de tiempo en pantalla:**
- VS Code: ~40% del video (arquitectura + código)
- Postman: ~40% del video (demo funcional)
- Django Admin: ~5% del video (auditoría)
- Cara/intro/cierre: ~15% del video (opcional)

---

## 🎬 PALABRAS CLAVE A MENCIONAR

Asegúrate de decir estas palabras en el video:

- [x] "Cascada" o "aprobación en cascada"
- [x] "Estado terminal"
- [x] "Auditoría"
- [x] "Multi-tenancy"
- [x] "URLs prefirmadas"
- [x] "Django REST Framework"
- [x] "JSON Web Token" o "JWT"
- [x] "PostgreSQL"
- [x] "Validación jerárquica"

---

## 🚀 EJEMPLO DE TIMING REAL

Si grabas y te das cuenta que vas en este tiempo:

- **Minuto 3:** Deberías estar terminando arquitectura
  - ✅ Bien: Empezando Postman
  - ⚠️ Lento: Todavía en Core app
  - ⚠️ Rápido: Ya en Request 3 de Postman

- **Minuto 5:** Deberías estar en medio del demo de Postman
  - ✅ Bien: Request 4 o 5
  - ⚠️ Lento: Request 2
  - ⚠️ Rápido: Ya en código

- **Minuto 8:** Deberías estar terminando código
  - ✅ Bien: Explicando approve_step
  - ⚠️ Lento: Recién empezando código
  - ⚠️ Rápido: Ya en Django Admin

---

**¡Éxito en tu grabación! 🎉 Confía en tu trabajo, está muy bien hecho.**
