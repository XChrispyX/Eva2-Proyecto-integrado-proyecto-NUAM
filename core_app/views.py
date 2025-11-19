from django.shortcuts import render
import json
import logging
import requests

# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
        usuario = Usuario.objects.first()
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

# API
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_calificaciones(request):
    """
    GET  -> lista todas las calificaciones en JSON
    POST -> crea una nueva calificación desde JSON
    """
    if request.method == "GET":
        try:
            datos = []
            for c in CalificacionTributaria.objects.all():
                datos.append({
                    "id": c.id,
                    "rut_empresa": c.rut_empresa,
                    "anio": c.anio,
                    "instrumento": c.instrumento,
                    "monto": float(c.monto),
                    "moneda": c.moneda,
                    "fecha_creacion": c.fecha_creacion.isoformat(),
                    "usuario_id": c.usuario.id,
                })
            return JsonResponse(datos, safe=False, status=200)
        except Exception:
            logging.exception("Error listando calificaciones")
            return JsonResponse({"error": "Error interno del servidor"}, status=500)

    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            logging.warning("JSON inválido en POST /api/calificaciones")
            return HttpResponseBadRequest("JSON inválido")

        campos_obligatorios = ["rut_empresa", "anio", "instrumento", "monto", "moneda"]
        for campo in campos_obligatorios:
            if campo not in body:
                logging.warning(f"Falta campo obligatorio: {campo}")
                return HttpResponseBadRequest(f"Falta el campo: {campo}")

        try:
            usuario = Usuario.objects.first()
            if not usuario:
                logging.error("No hay usuarios registrados para asociar calificación")
                return JsonResponse({"error": "No hay usuario asociado"}, status=400)

            calif = CalificacionTributaria.objects.create(
                rut_empresa = body["rut_empresa"],
                anio        = int(body["anio"]),
                instrumento = body["instrumento"],
                monto       = body["monto"],
                moneda      = body["moneda"],
                usuario     = usuario
            )
            logging.info(f"Calificación creada vía API con id={calif.id}")
            return JsonResponse({"id": calif.id, "mensaje": "Calificación creada"}, status=201)
        except Exception:
            logging.exception("Error creando calificación vía API")
            return JsonResponse({"error": "Error interno al crear calificación"}, status=500)


@csrf_exempt
def api_calificacion_detalle(request, id):
    """
    GET    -> detalle de una calificación
    PUT    -> actualizar todos los campos
    PATCH  -> actualizar parcialmente
    DELETE -> eliminar registro
    """
    try:
        calif = CalificacionTributaria.objects.get(id=id)
    except CalificacionTributaria.DoesNotExist:
        return JsonResponse({"error": "No encontrada"}, status=404)

    if request.method == "GET":
        data = {
            "id": calif.id,
            "rut_empresa": calif.rut_empresa,
            "anio": calif.anio,
            "instrumento": calif.instrumento,
            "monto": float(calif.monto),
            "moneda": calif.moneda,
            "fecha_creacion": calif.fecha_creacion.isoformat(),
            "usuario_id": calif.usuario.id,
        }
        return JsonResponse(data, status=200)

    if request.method in ["PUT", "PATCH"]:
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            logging.warning("JSON inválido en actualización de calificación")
            return HttpResponseBadRequest("JSON inválido")

        calif.rut_empresa = body.get("rut_empresa", calif.rut_empresa)
        calif.anio        = int(body.get("anio", calif.anio))
        calif.instrumento = body.get("instrumento", calif.instrumento)
        calif.monto       = body.get("monto", calif.monto)
        calif.moneda      = body.get("moneda", calif.moneda)
        calif.save()

        logging.info(f"Calificación actualizada id={calif.id}")
        return JsonResponse({"mensaje": "Calificación actualizada"}, status=200)

    if request.method == "DELETE":
        calif.delete()
        logging.info(f"Calificación eliminada id={id}")
        return JsonResponse({"mensaje": "Calificación eliminada"}, status=204)

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])


@csrf_exempt
@require_http_methods(["POST"])
def api_convertir_monto(request):
    """
    POST:
    {
      "monto": 1000,
      "moneda_origen": "CLP",
      "moneda_destino": "PEN"
    }
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logging.warning("JSON inválido en /api/convertir-monto")
        return HttpResponseBadRequest("JSON inválido")

    try:
        monto = float(body["monto"])
        moneda_origen = body["moneda_origen"]
        moneda_destino = body["moneda_destino"]
    except KeyError as e:
        logging.warning(f"Falta campo en conversión de monto: {e}")
        return HttpResponseBadRequest("Faltan campos: monto, moneda_origen, moneda_destino")

    url = "https://api.exchangerate.host/convert"
    params = {
        "from": moneda_origen,
        "to": moneda_destino,
        "amount": monto
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        resultado = data.get("result", None)
        logging.info(f"Conversión realizada {monto} {moneda_origen} -> {resultado} {moneda_destino}")
    except Exception:
        logging.exception("Error llamando a API externa de conversión de moneda")
        return JsonResponse({"error": "No se pudo realizar la conversión"}, status=500)

    return JsonResponse({
        "monto_origen": monto,
        "moneda_origen": moneda_origen,
        "moneda_destino": moneda_destino,
        "monto_convertido": resultado
    }, status=200)