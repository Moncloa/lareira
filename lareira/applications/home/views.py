from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
# Create your views here.
class IndexView(TemplateView):
    template_name = 'home/index.html'

class Lista(ListView):
    template_name = 'home/lista.html'
    queryset = ['uno','dos','tres','cuatro']
    context_object_name = 'libros'

