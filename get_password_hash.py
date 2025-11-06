"""
Generar password hash correcto para admin123
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'erpdocs.settings'
os.environ['SECRET_KEY'] = 'temp-key-for-hash-generation'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = '*'
os.environ['DATABASE_URL'] = 'postgresql://temp:temp@localhost/temp'

import django
from django.conf import settings

# Configurar Django mínimamente
if not settings.configured:
    settings.configure(
        SECRET_KEY='temp-secret-key',
        PASSWORD_HASHERS=[
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        ],
        USE_TZ=True,
    )

django.setup()

from django.contrib.auth.hashers import make_password

# Generar el hash
password = "admin123"
hash_result = make_password(password)

print("\n" + "="*80)
print("PASSWORD HASH GENERADO")
print("="*80)
print(f"\nPassword original: {password}")
print(f"\nHash generado:\n{hash_result}")
print("\n" + "="*80)
print("\nUSA ESTE HASH EN EL SQL:")
print("="*80)
print(f"\n'{hash_result}'")
print("\n")
