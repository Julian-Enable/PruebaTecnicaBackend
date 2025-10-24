# 🚂 Deploy en Railway.app - Guía Paso a Paso

> **Tiempo estimado:** 10-15 minutos  
> **Resultado:** Tu API funcionando en una URL pública

---

## ⚡ ¿Por Qué Railway?

✅ **Deploy automático** desde GitHub  
✅ **PostgreSQL gratis** incluido  
✅ **HTTPS automático**  
✅ **500 horas gratis/mes** (suficiente para demo)  
✅ **Cero configuración** de servidor  
✅ **URL pública** para tu demo

---

## 📋 Pre-requisitos

- [x] Código subido a GitHub ✅ (ya lo hiciste)
- [ ] Cuenta en Railway.app (gratis)
- [ ] Navegador web

---

## 🚀 Paso a Paso

### 1️⃣ Crear Cuenta en Railway (2 minutos)

1. Ve a: **https://railway.app/**
2. Click en **"Start a New Project"** o **"Login"**
3. Opciones de login:
   - ⭐ **GitHub** (recomendado - deploy automático)
   - Google
   - Email

**Usa GitHub** para conectar automáticamente tus repositorios.

---

### 2️⃣ Crear Nuevo Proyecto (1 minuto)

1. En el dashboard de Railway, click en **"New Project"**

2. Selecciona **"Deploy from GitHub repo"**

3. **Autoriza Railway** a acceder a tus repositorios (solo la primera vez)

4. Busca y selecciona: **`PruebaTecnicaBackend`**

5. Railway detectará automáticamente que es un proyecto Django ✅

---

### 3️⃣ Agregar PostgreSQL (1 minuto)

1. En tu proyecto de Railway, click en **"+ New"**

2. Selecciona **"Database"** → **"Add PostgreSQL"**

3. Railway creará automáticamente:
   - ✅ Base de datos PostgreSQL
   - ✅ Variables de entorno conectadas

**¡Listo!** La base de datos está conectada automáticamente.

---

### 4️⃣ Configurar Variables de Entorno (3 minutos)

1. Click en tu servicio **"PruebaTecnicaBackend"**

2. Ve a la pestaña **"Variables"**

3. Agrega estas variables (click en **"+ New Variable"**):

```bash
# Django
DJANGO_SECRET_KEY=tu-clave-super-secreta-cambiala-123456789
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*

# Las variables de DB ya están configuradas automáticamente por Railway:
# DATABASE_URL (automático cuando agregas PostgreSQL)
```

**Nota:** Railway ya configura automáticamente:
- `DATABASE_URL`
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

4. Click en **"Add"** después de cada variable

---

### 5️⃣ Actualizar settings.py para Railway (Ya está listo)

**Ya incluí estos cambios en el código:**

```python
# Railway detecta automáticamente DATABASE_URL
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.environ['DATABASE_URL'],
        conn_max_age=600
    )

# ALLOWED_HOSTS para Railway
if 'RAILWAY_PUBLIC_DOMAIN' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RAILWAY_PUBLIC_DOMAIN'])
```

---

### 6️⃣ Hacer Commit y Push (1 minuto)

Los archivos ya están listos en tu repo:
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Versión de Python
- ✅ `railway.json` - Configuración Railway
- ✅ `requirements.txt` - Con gunicorn

Ahora solo sube los cambios:

```powershell
git add .
git commit -m "⚙️ Add Railway.app deployment config"
git push
```

---

### 7️⃣ Deploy Automático (3-5 minutos)

1. Railway detectará el push automáticamente
2. Verás el **build en progreso** en el dashboard
3. Railway ejecutará:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   gunicorn erpdocs.wsgi
   ```

**Logs en tiempo real:**
- Click en tu servicio
- Ve a **"Deployments"**
- Click en el deployment activo
- Ve los logs en vivo

**✅ Cuando veas:**
```
[INFO] Listening at: http://0.0.0.0:8000
```
**¡Está listo!**

---

### 8️⃣ Obtener tu URL Pública (30 segundos)

1. Click en tu servicio **"PruebaTecnicaBackend"**

2. Ve a la pestaña **"Settings"**

3. Scroll hasta **"Domains"**

4. Click en **"Generate Domain"**

5. Railway te dará una URL como:
   ```
   https://pruebatecnicabackend-production-XXXX.up.railway.app
   ```

**¡Copia esta URL!** La usarás en Postman.

---

### 9️⃣ Cargar Datos de Prueba en Railway (2 minutos)

**Opción A: Desde Railway CLI** (recomendado)

1. Instala Railway CLI:
   ```powershell
   # Windows (con PowerShell como admin)
   iwr https://railway.app/install.ps1 | iex
   ```

2. Login:
   ```powershell
   railway login
   ```

3. Conecta con tu proyecto:
   ```powershell
   railway link
   ```

4. Ejecuta el shell de Django:
   ```powershell
   railway run python manage.py shell
   ```

5. Pega el contenido de `entrega/load_data.py`

**Opción B: Crear superuser desde CLI**

```powershell
railway run python manage.py createsuperuser
```

**Opción C: Usar el Django Admin**

1. Ve a: `https://tu-url.railway.app/admin/`
2. Login con las credenciales que creaste
3. Crea usuarios manualmente

---

### 🔟 Probar tu API en Producción (2 minutos)

1. **Actualiza Postman:**
   - Variable `base_url`: Cambia a tu URL de Railway
   - Ejemplo: `https://pruebatecnicabackend-production.up.railway.app`

2. **Ejecuta Request 1:** Login (obtener token)

3. **Ejecuta Request 4:** Crear documento con validación

4. **Ejecuta Request 5:** Aprobar con cascada

**✅ ¡FUNCIONA EN PRODUCCIÓN!** 🎉

---

## ✅ Checklist de Verificación

Marca cada paso completado:

- [ ] Cuenta Railway creada
- [ ] Proyecto creado desde GitHub
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] Código con configuración Railway pusheado
- [ ] Deploy exitoso (sin errores en logs)
- [ ] URL pública generada
- [ ] Datos de prueba cargados
- [ ] API funciona en Postman con URL de Railway

---

## 🎬 Para tu Video - Con Railway

**Ahora tu demo es MÁS IMPRESIONANTE:**

```
[0:00-1:00] Introducción
"Desarrollé este sistema y lo desplegué en producción 
usando Railway.app con PostgreSQL en la nube."

[3:00-7:00] Demo en Postman
- URL: https://tu-proyecto.railway.app/api/...
- "Como pueden ver, está funcionando en producción real"
- Crear documento
- Aprobar con cascada
- Todo funciona en vivo ✨

[Cierre]
"El sistema está desplegado y funcionando. 
Pueden probar la API en esta URL pública."
```

**VS demo local:**
```
"Está corriendo en mi localhost..." ❌
- Menos profesional
- Solo tú lo ves
- Puede fallar
```

---

## 📊 Monitoreo en Railway

**Railway te da:**

1. **Métricas en tiempo real:**
   - CPU usage
   - Memory usage
   - Network traffic

2. **Logs en vivo:**
   - Ver cada request
   - Errores en tiempo real
   - Debugging fácil

3. **Deploys automáticos:**
   - Cada push → nuevo deploy
   - Rollback fácil si algo falla

---

## 🆘 Problemas Comunes

### "Build failed"
**Solución:**
- Revisa los logs en Railway
- Verifica que `requirements.txt` esté correcto
- Asegúrate que `Procfile` existe

### "Application Error" al abrir la URL
**Solución:**
- Revisa logs: `railway logs`
- Verifica que las migraciones corrieron: `railway run python manage.py migrate`
- Verifica variables de entorno

### "Could not connect to PostgreSQL"
**Solución:**
- Verifica que agregaste el servicio PostgreSQL
- Railway configura `DATABASE_URL` automáticamente
- Revisa que `psycopg[binary]` está en requirements.txt

### "Bad Request (400)" en todas las requests
**Solución:**
- Verifica `ALLOWED_HOSTS` en variables de entorno
- Debe incluir `*` o tu dominio de Railway

---

## 💡 Tips Pro

1. **Usa Railway CLI** para debugging rápido:
   ```powershell
   railway logs        # Ver logs en vivo
   railway run <cmd>   # Ejecutar comandos
   railway shell       # SSH al contenedor
   ```

2. **Rollback fácil:**
   - Si algo falla, Railway te deja volver a un deploy anterior
   - Click en "Deployments" → Elige uno anterior → "Redeploy"

3. **Variables de entorno por servicio:**
   - Puedes tener diferentes configs para diferentes servicios
   - Útil si tienes frontend y backend separados

---

## 🎯 Resultado Final

**Tu sistema ahora está:**
- ✅ Funcionando en producción
- ✅ Con URL pública HTTPS
- ✅ PostgreSQL en la nube
- ✅ Deploy automático con cada push
- ✅ Listo para demos profesionales

**URL de ejemplo:**
```
API: https://pruebatecnicabackend-production.up.railway.app/api/
Admin: https://pruebatecnicabackend-production.up.railway.app/admin/
Docs: https://pruebatecnicabackend-production.up.railway.app/api/schema/swagger-ui/
```

---

## 📝 Para tu Entrega

Ahora puedes entregar:

1. **Repositorio GitHub:**
   ```
   https://github.com/Julian-Enable/PruebaTecnicaBackend
   ```

2. **API en Producción:**
   ```
   https://tu-proyecto.railway.app
   ```

3. **Video demostrando:**
   - Sistema funcionando EN PRODUCCIÓN
   - Mucho más impresionante que localhost

4. **Colección Postman:**
   - Con `base_url` apuntando a Railway
   - Cualquiera puede probar tu API

---

## 🚀 Próximo Paso

**Ejecuta estos comandos para subir los cambios:**

```powershell
git add .
git commit -m "⚙️ Add Railway.app deployment config"
git push
```

**Luego sigue esta guía para deployar en Railway.**

**Tiempo total: ~15 minutos** ⚡

---

**¡Éxito con tu deploy!** 🎉
