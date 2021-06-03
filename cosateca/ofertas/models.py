from django.db import models
from usuarios.models import Usuario
class Oferta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=250)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.TextField()