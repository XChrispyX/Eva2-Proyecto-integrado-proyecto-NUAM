from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_calificaciones, name='listar'),
    path('crear/', views.crear_calificacion, name='crear'),
    path('editar/<int:id>/', views.editar_calificacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_calificacion, name='eliminar'),
]
