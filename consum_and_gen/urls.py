from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('consum_and_gen',views.index)]