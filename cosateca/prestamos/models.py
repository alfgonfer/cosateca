from django.db import models
from usuarios.models import Usuario

class Prestamo(models.Model):
    prestador = models.CharField(max_length=30)
    objeto = models.TextField()
    recibidor = models.CharField(max_length=30)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contraparte = models.CharField(max_length=30)
    objeto = models.TextField()
    telefono = models.CharField(max_length=9, null=True, default=0)
    oferta_id = models.IntegerField(null=True)
    fecha_notificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
