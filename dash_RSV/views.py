from django.shortcuts import render
from . import plotly_app
from .models import prices_all
# Create your views here.
def index(request):
    prices_comp_all =prices_all.objects.all()
    return render(request,'dash_RSV/layout.html', {'prices_comp_all':prices_comp_all})



