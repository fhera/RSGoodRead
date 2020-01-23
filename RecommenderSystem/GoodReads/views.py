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
class LibrosRecomendadosItems(FormView):
    template_name = "recommended_books_items.html"
    form_class = UserForm
    success_url = reverse_lazy("similarBooks")

    def form_valid(self, form):
        context = super().get_context_data()
        id_user = form.cleaned_data['id_usuario']
        user = get_object_or_404(
            Usuario,
            pk=id_user
        )
        shelf = shelve.open("dataRS.dat")
        prefs = shelf['Prefs']
        sim_items = shelf['SimItems']
        shelf.close()
        rankings = getRecommendedItems(prefs, sim_items, int(id_user))
        recommended = rankings[:5]
        libros = []
        puntuaciones = []
        for re in recommended:
            libros.append(Libro.objects.get(pk=re[1]))
            puntuaciones.append(re[0])
        items = zip(libros, puntuaciones)
        context["user"] = user
        context["items"] = items
        return self.render_to_response(context)


# Ejercicio 3: Dado un usuario (Id), le recomiende cinco
# libros que no haya puntuado (Título). Usando un sistema
# de recomendación de tipo filtrado colaborativo basado en usuarios.
class LibrosRecomendados(FormView):
    template_name = "recommended_books_users.html"
    form_class = UserForm
    success_url = reverse_lazy("similarBooks")

    def form_valid(self, form):
        context = super().get_context_data()
        id_user = form.cleaned_data['id_usuario']
        user = get_object_or_404(
            Usuario,
            pk=id_user
        )
        shelf = shelve.open("dataRS.dat")
        prefs = shelf['Prefs']
        shelf.close()
        rankings = getRecommendations(prefs, int(id_user))
        recommended = rankings[:5]
        libros = []
        puntuaciones = []
        for re in recommended:
            libros.append(Libro.objects.get(pk=re[1]))
            puntuaciones.append(re[0])
        items = zip(libros, puntuaciones)
        context["user"] = user
        context["items"] = items
        return self.render_to_response(context)


# Ejercicio 4: Dado un libro (Id), mostrar tres usuarios a los que se
# le recomendaría.
class UsuariosRecomendados(FormView):
    template_name = "recommendation_users.html"
    form_class = BookForm
    success_url = reverse_lazy("recomendationUser")

    def form_valid(self, form):
        context = super().get_context_data()
        id_book = form.cleaned_data['id_book']
        user = get_object_or_404(
            Usuario,
            pk=id_book
        )
        shelf = shelve.open("dataRS.dat")
        prefs = shelf['ItemsPrefs']
        shelf.close()
        rankings = getRecommendations(prefs, int(id_book))
        recommended = rankings[:3]
        usuarios = []
        puntuaciones = []
        for re in recommended:
            usuarios.append(Usuario.objects.get(pk=re[1]))
            puntuaciones.append(re[0])
        items = zip(usuarios, puntuaciones)
        context["user"] = user
        context["items"] = items
        return self.render_to_response(context)



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
