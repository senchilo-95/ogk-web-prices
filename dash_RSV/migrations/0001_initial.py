# Generated by Django 3.2.14 on 2022-07-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='prices_RSV_from_ATS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('station', models.TextField(verbose_name='Станция')),
                ('price', models.FloatField(verbose_name='Цена')),
            ],
        ),
    ]
