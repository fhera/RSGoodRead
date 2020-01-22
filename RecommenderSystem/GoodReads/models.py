from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Libro(models.Model):
    idLibro = models.IntegerField(primary_key=True)
    Titulo = models.CharField(max_length=100)
    Autor = models.CharField(max_length=30)
    Isbn = models.CharField(max_length=30)
    Idioma = models.CharField(max_length=30)
    NumPuntuaciones1 = models.PositiveIntegerField()
    NumPuntuaciones2 = models.PositiveIntegerField()
    NumPuntuaciones3 = models.PositiveIntegerField()
    NumPuntuaciones4 = models.PositiveIntegerField()
    def __str__(self):
        return self.Titulo

class Usuario(models.Model):
    idUsuario = models.IntegerField(primary_key=True)

class Puntuacion(models.Model):
    idUsuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    idLibro = models.ForeignKey("Libro", on_delete=models.CASCADE)
    Puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return self.Puntuacion
