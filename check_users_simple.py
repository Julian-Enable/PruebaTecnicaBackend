from django.contrib.auth import get_user_model

User = get_user_model()

print("\n=== USUARIOS EXISTENTES ===\n")
for user in User.objects.all():
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Activo: {user.is_active}")
    print(f"Staff: {user.is_staff}")
    print("-" * 40)

print(f"\nTotal: {User.objects.count()} usuarios")
