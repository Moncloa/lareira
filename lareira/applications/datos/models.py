from django.db import models

# Create your models here.
class Sensor(models.Model):
    nombre = models.CharField('Sensor',max_length=8)

class Muestra(models.Model):
    temp = models.DecimalField('Temperatura',max_digits=3,decimal_places=1)
    hum = models.DecimalField('Humedad',max_digits=3,decimal_places=1)
    temp_cpu = models.DecimalField('Temperatura CPU',max_digits=4,decimal_places=2)
    temp_gpu = models.DecimalField('Temperatura GPU',max_digits=4,decimal_places=2)
    disk_cap = models.DecimalField('Uso del disco',max_digits=3,decimal_places=0)
    fecha_hora = models.DateTimeField('Fecha y hora')
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    def __str__(self):
        return self.fecha_hora

