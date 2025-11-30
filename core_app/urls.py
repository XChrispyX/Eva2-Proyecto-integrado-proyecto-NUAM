from django.urls import path
from . import views

urlpatterns = [
    # CRUD 
    path('', views.listar_calificaciones, name='listar'),
    path('crear/', views.crear_calificacion, name='crear'),
    path('editar/<int:id>/', views.editar_calificacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar'),
    path('dashboard/', views.dashboard_monedas, name='dashboard'),
    # APIs 
    path('api/calificaciones/', views.api_calificaciones, name='api_calificaciones'),
    path('api/calificaciones/<int:id>/', views.api_calificacion_detalle, name='api_calificacion_detalle'),
    path('api/convertir-monto/', views.api_convertir_monto, name='api_convertir_monto'),
]
