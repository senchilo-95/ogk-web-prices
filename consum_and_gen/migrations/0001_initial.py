# Generated by Django 3.2.14 on 2022-07-30 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='generation_and_consumption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('generation', models.FloatField(verbose_name='generation')),
                ('consumption', models.FloatField(verbose_name='consumption')),
                ('ups', models.TextField(verbose_name='ups')),
            ],
            options={
                'verbose_name': 'Потребление и генерация с сайта СО ЕЭС',
                'verbose_name_plural': 'Потребление и генерация с сайта СО ЕЭС',
            },
        ),
    ]