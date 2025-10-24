# Management script for Django project

Write-Host "ERP Documents Management Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$action = $args[0]

switch ($action) {
    "migrate" {
        Write-Host "Running migrations..." -ForegroundColor Green
        .\.venv\Scripts\python.exe manage.py makemigrations
        .\.venv\Scripts\python.exe manage.py migrate
    }
    "seed" {
        Write-Host "Seeding database..." -ForegroundColor Green
        .\.venv\Scripts\python.exe manage.py shell -c @"
from django.contrib.auth.models import User
from core.models import Company, CompanyMembership
import uuid

# Create test users
users = {}
for username in ['sebastian', 'camilo', 'juan', 'uploader']:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': f'{username}@example.com'}
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'Created user: {username}')
    users[username] = user

# Create test company
company, created = Company.objects.get_or_create(
    name='Test Company',
    defaults={'is_active': True}
)
if created:
    print(f'Created company: {company.name}')

# Create memberships
for username, role in [('sebastian', 'APPROVER'), ('camilo', 'APPROVER'), 
                        ('juan', 'APPROVER'), ('uploader', 'UPLOADER')]:
    membership, created = CompanyMembership.objects.get_or_create(
        user=users[username],
        company=company,
        defaults={'role': role, 'is_active': True}
    )
    if created:
        print(f'Created membership: {username} - {role}')

print('')
print('Seed data created successfully!')
print(f'Company ID: {company.id}')
print('Users:')
for username, user in users.items():
    print(f'  - {username}: {user.id}')
"@
    }
    "test" {
        Write-Host "Running tests..." -ForegroundColor Green
        .\.venv\Scripts\python.exe -m pytest tests/ -v
    }
    "lint" {
        Write-Host "Running linters..." -ForegroundColor Green
        .\.venv\Scripts\python.exe -m ruff check .
        .\.venv\Scripts\python.exe -m black --check .
    }
    "format" {
        Write-Host "Formatting code..." -ForegroundColor Green
        .\.venv\Scripts\python.exe -m black .
        .\.venv\Scripts\python.exe -m isort .
    }
    "run" {
        Write-Host "Starting development server..." -ForegroundColor Green
        .\.venv\Scripts\python.exe manage.py runserver
    }
    "shell" {
        Write-Host "Starting Django shell..." -ForegroundColor Green
        .\.venv\Scripts\python.exe manage.py shell
    }
    default {
        Write-Host "Usage: .\scripts\manage.ps1 [command]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Cyan
        Write-Host "  migrate  - Run database migrations"
        Write-Host "  seed     - Seed database with test data"
        Write-Host "  test     - Run test suite"
        Write-Host "  lint     - Check code quality"
        Write-Host "  format   - Format code"
        Write-Host "  run      - Start development server"
        Write-Host "  shell    - Start Django shell"
    }
}
