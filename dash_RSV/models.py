from django.db import models

# Create your models here.
class prices_RSV_from_ATS(models.Model):
    date = models.DateTimeField('Дата')
    station=models.TextField('Станция')
    price=models.FloatField('Цена')

    def __str__(self):
        return self.station

    class Meta:
        verbose_name = 'Цена РСВ с сайта АТС'
        verbose_name_plural = 'Цена РСВ с сайта АТС'




