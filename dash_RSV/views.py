from django.shortcuts import render
from . import plotly_app
from .models import prices_RSV_from_ATS,prices_all
# Create your views here.
def index(request):
    prices = prices_RSV_from_ATS.objects.all()
    prices_comp_all =prices_all.objects.all()
    return render(request,'dash_RSV/index.html', {'prices':prices,'prices_comp_all':prices_comp_all})



