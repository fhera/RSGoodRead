from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from GoodReads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('populate/', views.populate_db),
    path('loadRS', views.load_rs),
    path('books/', views.LibrosPuntuados.as_view(), name="books"),
    path('topBooks/', views.TopBooks.as_view(), name="topBooks"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
