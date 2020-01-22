import shelve

from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView

from GoodReads.forms import BookForm, UserForm
from GoodReads.models import Libro, Puntuacion, Usuario
from GoodReads.populate import populate_database
from GoodReads.recommendations import (calculateSimilarItems,
                                       getRecommendations, getRecommendedItems,
                                       topMatches, transformPrefs)


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a libros. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def load_dict():
    prefs = {}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    puntuaciones = Puntuacion.objects.all()
    for puntuacion in puntuaciones:
        userid = int(puntuacion.usuario.idUsuario)
        bookid = int(puntuacion.libro.idLibro)
        puntuacion = int(puntuacion.Puntuacion)
        prefs.setdefault(userid, {})
        prefs[userid][bookid] = puntuacion
    shelf['Prefs'] = prefs
    shelf['ItemsPrefs'] = transformPrefs(prefs)
    shelf['SimItems'] = calculateSimilarItems(prefs, n=10)
    shelf.close()


#  CONJUNTO DE VISTAS
def index(request):
    return render(request, 'index.html')


def populate_db(request):
    populate_database()
    return render(request, 'populate.html')


def load_rs(request):
    load_dict()
    return render(request, 'loadRS.html')


# Ejercicio 1: Dado un usuario (Id),
# mostrar todos los libros que ha puntuado (Título) y su puntuación.
class LibrosPuntuados(FormView):
    template_name = "books.html"
    form_class = UserForm
    success_url = reverse_lazy("books")

    def form_valid(self, form):
        context = super().get_context_data()
        puntuaciones = None
        if self.request.POST:
            puntuaciones = Puntuacion.objects.filter(
                usuario_id=form.cleaned_data['id_usuario']
            )
        context["puntuaciones"] = puntuaciones
        return self.render_to_response(context)


# Ejercicio 2: Dado un usuario (Id), le recomiende cinco
# libros que no haya puntuado (Título). Usando un sistema
# de recomendación de tipo filtrado colaborativo basado en ítems.


# Ejercicio 3: Dado un usuario (Id), le recomiende cinco
# libros que no haya puntuado (Título). Usando un sistema
# de recomendación de tipo filtrado colaborativo basado en usuarios.


# Ejercicio 4: Dado un libro (Id), mostrar tres usuarios a los que se
# le recomendaría.


# Ejercicio 5: Dada un libro(Id), mostrar los tres libros (ISBN, título y autor)
# mejor puntuados.
class TopBooks(ListView):
    model = Libro
    template_name = "top_books.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libros = list(Libro.objects.all())
        for libro in libros:
            total = libro.NumPuntuaciones1 + \
                libro.NumPuntuaciones2 + libro.NumPuntuaciones3 + \
                libro.NumPuntuaciones4
            try:
                libro.media = libro.NumPuntuaciones1 / total + \
                    2 * (libro.NumPuntuaciones2 / total) + \
                    3 * (libro.NumPuntuaciones3 / total) + \
                    4 * (libro.NumPuntuaciones4 / total)
            except ZeroDivisionError:
                libro.media = 0
        libros.sort(key=lambda x: x.media, reverse=True)
        context['libros'] = libros[:3]
        return context
