from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import CalificacionTributaria, Usuario

# LISTAR
def listar_calificaciones(request):
    calificaciones = CalificacionTributaria.objects.all()
    return render(request, 'calificaciones/listar.html', {'calificaciones': calificaciones})

# CREAR
def crear_calificacion(request):
    if request.method == 'POST':
        rut_empresa = request.POST['rut_empresa']
        anio = request.POST['anio']
        instrumento = request.POST['instrumento']
        monto = request.POST['monto']
        moneda = request.POST['moneda']
        usuario = Usuario.objects.first()  # temporal, simula un usuario logueado

        CalificacionTributaria.objects.create(
            rut_empresa=rut_empresa,
            anio=anio,
            instrumento=instrumento,
            monto=monto,
            moneda=moneda,
            usuario=usuario
        )
        return redirect('listar')
    return render(request, 'calificaciones/crear.html')

# EDITAR
def editar_calificacion(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        calificacion.rut_empresa = request.POST['rut_empresa']
        calificacion.anio = request.POST['anio']
        calificacion.instrumento = request.POST['instrumento']
        calificacion.monto = request.POST['monto']
        calificacion.moneda = request.POST['moneda']
        calificacion.save()
        return redirect('listar')
    return render(request, 'calificaciones/editar.html', {'calificacion': calificacion})

# ELIMINAR
def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(CalificacionTributaria, id=id)
    if request.method == 'POST':
        calificacion.delete()
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})
