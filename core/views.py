from django.shortcuts import render, redirect, get_object_or_404
from .models import Device
from .forms import DeviceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import io
from django.http import HttpResponse
from .models import Device
import matplotlib.pyplot as plt
from django.core.paginator import Paginator

# Views

@login_required
def device_list(request):
    """Display the device list with optional pagination."""

    all_devices = Device.objects.all().order_by("id")
    show_all = request.GET.get("all") == "1"

    if show_all:
        devices = all_devices
        page_obj = None
    else:
        paginator = Paginator(all_devices, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        devices = page_obj

    context = {
        "devices": devices,
        "page_obj": page_obj,
        "show_all": show_all,
    }
    return render(request, "core/device_list.html", context)

@login_required
def device_add(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'core/device_form.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatyczne zalogowanie po rejestracji
            return redirect('device_list')
    else:
        form = UserCreationForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def device_stats(request):
    # Liczba urządzeń wg typu
    device_types = dict(Device.DEVICE_TYPES)
    stats = {k: 0 for k in device_types.keys()}
    for dev in Device.objects.all():
        stats[dev.device_type] += 1

    types = [device_types[k] for k in stats.keys()]
    counts = list(stats.values())

    # Tworzymy wykres
    fig, ax = plt.subplots()
    ax.bar(types, counts)
    ax.set_ylabel('Liczba urządzeń')
    ax.set_title('Urządzenia wg typu')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')

# Widok HTML z osadzeniem wykresu:
@login_required
def device_stats_page(request):
    return render(request, 'core/device_stats.html')


@login_required
def device_edit(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'core/device_form.html', {'form': form})

@login_required
def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'core/device_confirm_delete.html', {'device': device})
