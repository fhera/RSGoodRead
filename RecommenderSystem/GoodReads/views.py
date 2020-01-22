from django.shortcuts import render
from GoodReads.populate import populateDatabase

#  CONJUNTO DE VISTAS
def index(request):
    return render(request, 'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html') 