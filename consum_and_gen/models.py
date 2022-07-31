from django.db import models

class generation_and_consumption(models.Model):
    date = models.DateTimeField('date')
    generation=models.FloatField('generation')
    consumption=models.FloatField('consumption')
    ups = models.TextField('ups')

    def __str__(self):
        return self.ups

    class Meta:
        verbose_name = 'Потребление и генерация с сайта СО ЕЭС'
        verbose_name_plural = 'Потребление и генерация с сайта СО ЕЭС'




