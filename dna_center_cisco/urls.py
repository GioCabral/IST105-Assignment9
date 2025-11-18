from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth_view'),
    path('devices/', views.devices_view, name='devices_view'),
    path('interfaces/', views.interfaces_view, name='interfaces_view'),
    path('logs/', views.logs_view, name='logs_view'),
]
