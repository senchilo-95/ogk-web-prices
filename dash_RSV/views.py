from django.shortcuts import render
from . import plotly_app
from .models import prices_RSV_from_ATS
# Create your views here.
def index(request):
    prices =prices_RSV_from_ATS.objects.all()
    return render(request,'dash_RSV/index.html', {'prices':prices})

def about(request):
    prices = prices_RSV_from_ATS.objects.all()
    return render(request, 'dash_RSV/index.html', {'prices': prices})

