from django.contrib import admin
from django.urls import path, re_path, include

from . import views

app_name = 'home.app'
urlpatterns = [

    path('index/', views.IndexView.as_view(), name='index'),
    path('libros/', views.Lista.as_view(), name='lista'),
]