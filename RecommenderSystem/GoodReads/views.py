from django.shortcuts import render

#  CONJUNTO DE VISTAS
def index(request):
    return render(request, 'index.html')