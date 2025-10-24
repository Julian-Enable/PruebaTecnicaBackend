# 📤 Subir Proyecto a GitHub

## ✅ Estado Actual

- ✅ Repositorio Git inicializado
- ✅ Commit inicial creado (61 archivos, 4,961 líneas)
- ✅ `.venv` excluido correctamente
- ⏳ Falta: Subir a GitHub

---

## 🚀 Pasos para Subir a GitHub

### 1️⃣ Crear Repositorio en GitHub

1. Ve a: **https://github.com/new**

2. Configura el repositorio:
   - **Repository name:** `PruebaTecnicaBackend`
   - **Description:** `Sistema de gestión de documentos ERP con validación jerárquica y aprobación en cascada`
   - **Visibility:** 
     - ✅ **Public** (si quieres que sea público)
     - ⭐ **Private** (recomendado para prueba técnica)
   
3. **⚠️ IMPORTANTE:** NO marques estas opciones:
   - ❌ Add a README file (ya tienes uno)
   - ❌ Add .gitignore (ya tienes uno)
   - ❌ Choose a license

4. Click en **"Create repository"**

---

### 2️⃣ Conectar con el Repositorio Remoto

Después de crear el repo, GitHub te mostrará instrucciones. Usa estas:

```powershell
# Conectar con el repositorio remoto (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/PruebaTecnicaBackend.git

# Renombrar rama de 'master' a 'main' (estándar actual)
git branch -M main

# Subir el código
git push -u origin main
```

**Ejemplo con usuario real:**
```powershell
git remote add origin https://github.com/juliandev/PruebaTecnicaBackend.git
git branch -M main
git push -u origin main
```

---

### 3️⃣ Verificar que Subió Correctamente

1. Recarga la página de tu repositorio en GitHub
2. Deberías ver:
   - ✅ 61 archivos
   - ✅ README.md con toda la documentación
   - ✅ Carpeta `entrega/` con las guías
   - ✅ Código fuente completo
   - ✅ Commit inicial con mensaje descriptivo

---

## 📂 Estructura que Verás en GitHub

```
PruebaTecnicaBackend/
├── 📄 README.md                    # Documentación principal
├── 📄 requirements.txt             # Dependencias
├── 📄 manage.py                    # Comando Django
├── 📄 docker-compose.yml           # Docker setup
│
├── 📁 entrega/                     # Documentación y scripts
│   ├── INICIO_AQUI.md
│   ├── PASO_1_CONFIGURACION.md
│   ├── PASO_2_PRUEBAS_POSTMAN.md
│   ├── PASO_3_GUION_VIDEO.md
│   ├── ERP_Documents_Postman_Collection.json
│   └── *.ps1, *.py
│
├── 📁 core/                        # App: Modelos base
├── 📁 documents/                   # App: Gestión documentos
├── 📁 validation/                  # App: Validación jerárquica
├── 📁 storageapp/                  # App: Storage abstracto
└── 📁 erpdocs/                     # Configuración Django
```

---

## 🔐 Autenticación en GitHub

Si te pide usuario/contraseña:

### Opción 1: HTTPS con Token (Recomendado)

1. Ve a: **https://github.com/settings/tokens**
2. Click en **"Generate new token"** → **"Classic"**
3. Nombre: `PruebaTecnicaBackend`
4. Selecciona permisos:
   - ✅ `repo` (todos los sub-permisos)
5. Click en **"Generate token"**
6. **COPIA EL TOKEN** (no lo volverás a ver)
7. Cuando Git pida password, **pega el token** (no tu contraseña)

### Opción 2: SSH

```powershell
# Generar clave SSH (si no tienes)
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Copiar clave pública
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard

# Agregar en GitHub:
# https://github.com/settings/keys → New SSH key
```

Luego usa URL SSH:
```powershell
git remote add origin git@github.com:TU_USUARIO/PruebaTecnicaBackend.git
```

---

## 🎯 Comandos Completos (Copia y Pega)

```powershell
# 1. Configurar tu identidad (si no lo has hecho)
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@example.com"

# 2. Conectar con GitHub (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/PruebaTecnicaBackend.git

# 3. Renombrar rama a 'main'
git branch -M main

# 4. Subir código
git push -u origin main
```

---

## ✅ Checklist Post-Subida

Después de subir, verifica en GitHub:

- [ ] El README.md se ve correctamente formateado
- [ ] Carpeta `entrega/` tiene los 8 archivos
- [ ] Código fuente completo (core, documents, validation, storageapp)
- [ ] No hay carpeta `.venv` (debe estar excluida)
- [ ] No hay archivos `.env` con contraseñas reales
- [ ] El commit tiene mensaje descriptivo

---

## 🔄 Comandos Git Útiles para el Futuro

```powershell
# Ver estado
git status

# Ver historial de commits
git log --oneline

# Agregar cambios
git add .
git commit -m "Descripción del cambio"
git push

# Ver remotes configurados
git remote -v

# Crear nueva rama
git checkout -b nombre-rama

# Cambiar entre ramas
git checkout main
```

---

## 📝 Para tu Entrega de Prueba Técnica

Cuando envíes el proyecto, incluye:

1. **URL del repositorio GitHub**
   ```
   https://github.com/TU_USUARIO/PruebaTecnicaBackend
   ```

2. **Video de demostración**
   - Sube a YouTube, Loom, o Google Drive
   - Usa el guión de `entrega/PASO_3_GUION_VIDEO.md`

3. **Instrucciones de configuración**
   - Están en `entrega/PASO_1_CONFIGURACION.md`
   - Ya están completas y detalladas

4. **Colección Postman**
   - Está en `entrega/ERP_Documents_Postman_Collection.json`
   - Ya incluida en el repositorio

---

## 🆘 Problemas Comunes

### "remote origin already exists"
```powershell
# Eliminar remote existente
git remote remove origin

# Agregar el correcto
git remote add origin <URL-CORRECTA>
```

### "failed to push some refs"
```powershell
# Forzar push (solo en repo nuevo)
git push -u origin main --force
```

### "Authentication failed"
- Si usas HTTPS: Usa un **Personal Access Token**, no tu contraseña
- Si usas SSH: Verifica que tu clave SSH esté agregada en GitHub

---

## ✨ ¡Listo!

Tu proyecto está listo para ser subido a GitHub.

**Próximos pasos:**
1. Crear repo en GitHub
2. Ejecutar los comandos de conexión
3. Verificar que todo subió correctamente
4. ¡Enviar el enlace en tu prueba técnica! 🚀

---

**Commit actual:**
```
8ff6564 🎉 Initial commit: Sistema de Gestión de Documentos ERP
```

**Archivos:** 61  
**Líneas de código:** 4,961  
**Estado:** ✅ Listo para GitHub
