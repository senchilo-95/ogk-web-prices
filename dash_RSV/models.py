from django.db import models

# Create your models here.

class prices_all(models.Model):
    station=models.TextField('Станция')
    price=models.FloatField('Цена')
    gen_company=models.TextField('Станция')
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.station

    class Meta:
        verbose_name = 'Цены РСВ для всех компаний'
        verbose_name_plural = 'Цены РСВ для всех компаний'




