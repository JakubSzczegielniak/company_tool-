from django import forms
from .models import Device, Department, DeviceHistory

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_type', 'inventory_number', 'status', 'location', 'department', 'assigned_user']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']

class DeviceHistoryForm(forms.ModelForm):
    class Meta:
        model = DeviceHistory
        fields = ['device', 'operation_type', 'performed_by', 'comment']
