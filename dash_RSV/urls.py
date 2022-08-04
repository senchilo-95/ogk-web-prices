from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('dash_RSV',views.index)
]
