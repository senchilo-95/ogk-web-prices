from django.shortcuts import render
from .models import generation_types
# Create your views here.
def index(request):
    gen_sources = generation_types.objects.all()
    return render(request,'gen_types/index.html', {'gen_types':gen_sources})


