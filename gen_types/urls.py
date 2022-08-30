from django.urls import path
from . import views
from .gen_types_app import app_gen
urlpatterns = [
    path('',views.index),
    path('gen_types',views.index)]