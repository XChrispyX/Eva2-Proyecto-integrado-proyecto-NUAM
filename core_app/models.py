from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class CalificacionTributaria(models.Model):
    rut_empresa = models.CharField(max_length=12)
    anio = models.IntegerField()
    instrumento = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.CharField(max_length=3, choices=[('CLP', 'Peso Chileno'), ('PEN', 'Sol Peruano'), ('COP', 'Peso Colombiano')], default='CLP')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.rut_empresa} - {self.anio} ({self.moneda})"

class DeclaracionJurada(models.Model):
    anio = models.IntegerField()
    total = models.DecimalField(max_digits=14, decimal_places=2)
    fecha_envio = models.DateField()
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"DJ {self.anio}"

class Factor(models.Model):
    descripcion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_vigencia = models.DateField()
    calificacion = models.ForeignKey(CalificacionTributaria, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class LogSeguridad(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion}"