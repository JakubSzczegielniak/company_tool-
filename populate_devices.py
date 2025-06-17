import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_tool.settings')
django.setup()

from core.models import Device, Department
from django.contrib.auth.models import User

DEVICE_TYPES = [k for k, v in Device.DEVICE_TYPES]
STATUS_CHOICES = [k for k, v in Device.STATUS_CHOICES]

# Upewnij się, że masz przynajmniej jeden departament i jednego usera
if not Department.objects.exists():
    Department.objects.create(name="IT", description="Dział IT")
if not User.objects.exists():
    User.objects.create_user(username="testuser", password="testpass")

department = Department.objects.first()
user = User.objects.first()

N = 10000  # Liczba urządzeń

devices = []
for i in range(N):
    device = Device(
        name=f"Urządzenie {i+1}",
        device_type=random.choice(DEVICE_TYPES),
        inventory_number=f"INV{i+1:05}",
        status=random.choice(STATUS_CHOICES),
        location=f"Magazyn {random.randint(1, 5)}",
        department=department,
        assigned_user=user if random.random() < 0.7 else None
    )
    devices.append(device)
    # Bulk w porcjach po 1000, żeby nie zabić bazy naraz
    if len(devices) == 1000:
        Device.objects.bulk_create(devices)
        print(f"Utworzono {i+1} urządzeń")
        devices = []

# dodaj resztę
if devices:
    Device.objects.bulk_create(devices)
    print(f"Utworzono {N} urządzeń")

print("Gotowe!")

