from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='devices/', permanent=False), name='home'),

    # ŚCIEŻKI SZCZEGÓŁOWE muszą być zdefiniowane PRZED ścieżką ogólną
    path('devices/add/', views.device_add, name='device_add'),
    path('devices/stats/', views.device_stats_page, name='device_stats_page'),
    path('devices/stats/plot.png', views.device_stats, name='device_stats'),
    path('devices/<int:pk>/edit/', views.device_edit, name='device_edit'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),

    # OGÓLNA ścieżka listy na samym końcu grupy 'devices'
    path('devices/', views.device_list, name='device_list'),

    # Pozostałe ścieżki (logowanie, rejestracja itd.)
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]