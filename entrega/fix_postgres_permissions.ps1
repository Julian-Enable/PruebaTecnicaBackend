# =================================================================
# Script para arreglar permisos de PostgreSQL
# =================================================================

Write-Host ""
Write-Host "Arreglando permisos de PostgreSQL..." -ForegroundColor Yellow
Write-Host ""

# Agregar PostgreSQL al PATH
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

Write-Host "Ingresa la contrasena de PostgreSQL (usuario: postgres)" -ForegroundColor Cyan
$password = Read-Host -AsSecureString "Password"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

$env:PGPASSWORD = $plainPassword

# Conectar y arreglar permisos
Write-Host ""
Write-Host "Otorgando permisos..." -ForegroundColor Yellow

$commands = @"
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
"@

psql -U postgres -d erpdocs -c $commands

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Permisos configurados correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ahora puedes ejecutar:" -ForegroundColor Cyan
    Write-Host "  python manage.py migrate" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Error configurando permisos" -ForegroundColor Red
    Write-Host ""
}
