"""
Management command para crear usuario de demostración
Ejecutar en Railway: python manage.py create_demo_user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un usuario administrador para demos'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@test.com'
        password = 'admin123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'⚠️  El usuario {username} ya existe'))
            return

        user = User.objects.create_superuser(
            username=username, 
            email=email, 
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ Superusuario creado exitosamente!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'   Username: {username}')
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Password: {password}')
        self.stdout.write(self.style.SUCCESS('=' * 50))
