from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])