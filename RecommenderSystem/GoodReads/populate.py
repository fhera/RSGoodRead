from GoodReads.models import Libro, Puntuacion, Usuario
import csv
import os

path = "dataset"


def delete_tables():
    Puntuacion.objects.all().delete()
    Libro.objects.all().delete()


def populate_usuarios():
    print("Loading usuarios...")

    Usuario.objects.all().delete()
    dict = {}
    lista = []
    for i in range(53425):
        u = Usuario(idUsuario=i)
        lista.append(u)
        dict[i] = u
    Usuario.objects.bulk_create(lista)
    print("Users inserted: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populate_libros():
    print("Loading Libros...")

    dict = {}
    lista = []
    with open(os.path.join(path, 'books.csv'), newline='', encoding="ISO-8859-1") as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        next(linereader)
        for row in linereader:
            id_libro = row[0].strip()
            l = Libro(
                idLibro=id_libro,
                Titulo=row[9],
                Autor=row[7],
                Isbn=row[5],
                Idioma=row[11],
                NumPuntuaciones1=row[16],
                NumPuntuaciones2=row[17],
                NumPuntuaciones3=row[18],
                NumPuntuaciones4=row[19]
            )
            lista.append(l)
            dict[int(id_libro)] = l
    Libro.objects.bulk_create(lista)

    print("Libros inserted: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populate_puntuaciones(u, l):
    print("Loading puntuaciones...")

    lista = []
    fileobj = open(os.path.join(path, "ratings.csv"), "r")
    id_libro = 1
    count = 0
    for line in fileobj.readlines()[1:]:
        rip = line.split(',')
        if len(rip) != 3:
            continue

        libro = int(rip[0].strip())
        if id_libro != libro:
            count = 0
            id_libro = libro
        else:
            count += 1

        if count <= 10:
            lista.append(
                Puntuacion(
                    usuario=u[int(rip[1].strip())],
                    libro=l[int(rip[0].strip())],
                    Puntuacion=int(rip[2].strip())
                )
            )

    fileobj.close()
    # bulk_create hace la carga masiva para acelerar el proceso
    Puntuacion.objects.bulk_create(lista)

    print("Puntuaciones inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")


def populate_database():
    delete_tables()
    u = populate_usuarios()
    l = populate_libros()
    populate_puntuaciones(u, l)
    print("Finished database population")


if __name__ == '__main__':
    populate_database()
