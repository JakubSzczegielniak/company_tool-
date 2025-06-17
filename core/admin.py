from django.contrib import admin
from .models import Department, Device, DeviceHistory

admin.site.register(Department)
admin.site.register(Device)
admin.site.register(DeviceHistory)
