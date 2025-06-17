from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    DEVICE_TYPES = [
        ('laptop', 'Laptop'),
        ('phone', 'Telefon'),
        ('monitor', 'Monitor'),
        ('printer', 'Drukarka'),
        ('server', 'Serwer'),
        ('router', 'Router'),
        ('other', 'Inne'),
    ]
    STATUS_CHOICES = [
        ('available', 'Dostępny'),
        ('in_use', 'Używany'),
        ('in_repair', 'W naprawie'),
        ('retired', 'Wycofany'),
    ]
    name = models.CharField(max_length=128)
    device_type = models.CharField(max_length=32, choices=DEVICE_TYPES)
    inventory_number = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=128, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"

class DeviceHistory(models.Model):
    OPERATION_TYPES = [
        ('assigned', 'Przypisanie'),
        ('unassigned', 'Zwolnienie'),
        ('repair', 'Naprawa'),
        ('retired', 'Wycofanie'),
        ('other', 'Inne'),
    ]
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    operation_date = models.DateTimeField(auto_now_add=True)
    operation_type = models.CharField(max_length=32, choices=OPERATION_TYPES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='performed_operations')
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.device} - {self.operation_type} ({self.operation_date})"
