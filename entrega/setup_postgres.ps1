# =================================================================
# Script para configurar PostgreSQL para el proyecto
# =================================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Configuracion de PostgreSQL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Agregar PostgreSQL al PATH
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

Write-Host "Ingresa la contrasena de PostgreSQL (usuario: postgres)" -ForegroundColor Yellow
$password = Read-Host -AsSecureString "Password"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Crear base de datos
Write-Host ""
Write-Host "Creando base de datos 'erpdocs'..." -ForegroundColor Yellow

$env:PGPASSWORD = $plainPassword

try {
    psql -U postgres -c "DROP DATABASE IF EXISTS erpdocs;" 2>$null
    psql -U postgres -c "CREATE DATABASE erpdocs;"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Base de datos creada correctamente" -ForegroundColor Green
    } else {
        Write-Host "Error creando base de datos" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "PostgreSQL configurado correctamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes ejecutar:" -ForegroundColor Cyan
Write-Host "  python manage.py migrate" -ForegroundColor White
Write-Host ""
