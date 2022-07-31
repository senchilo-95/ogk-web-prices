from django.shortcuts import render
from . import app_consum
from .models import generation_and_consumption
# Create your views here.
def index(request):
    generation = generation_and_consumption.objects.all()
    consumption = generation_and_consumption.objects.all()
    return render(request,'consum_and_gen/index.html', {'generation':generation,'consumption':consumption})