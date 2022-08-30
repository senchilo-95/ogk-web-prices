from django.db import models

# Create your models here.
class generation_types(models.Model):
    station_type=models.TextField('station_type')
    genertion=models.FloatField('generation')
    date = models.DateTimeField('date')

    def __str__(self):
        return self.station

    class Meta:
        verbose_name = 'Генерация по источникам'
        verbose_name_plural = 'Генерация по источникам'
