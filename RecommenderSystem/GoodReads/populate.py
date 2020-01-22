from GoodReads.models import Libro, Puntuacion, Usuario
import csv
import os

path = "dataset"

def deleteTables():  
    Puntuacion.objects.all().delete()
    Libro.objects.all().delete()

def populateUsuarios():
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


def populateLibros():
    print("Loading Libros...")
    
    dict = {}
    lista=[]
    with open(os.path.join(path, 'books.csv'), newline='', encoding="ISO-8859-1") as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        next(linereader)
        for row in linereader:
            idLibro = row[0].strip()
            l = Libro(
                idLibro = idLibro, 
                Titulo = row[9],
                Autor = row[7],
                Isbn = row[5],
                Idioma = row[11],
                NumPuntuaciones1 = row[16],
                NumPuntuaciones2 = row[17],
                NumPuntuaciones3 = row[18],
                NumPuntuaciones4 = row[19]
            )
            lista.append(l)
            dict[int(idLibro)] = l
    Libro.objects.bulk_create(lista)
    
    print("Libros inserted: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")
    return(dict)


def populatePuntuaciones(u, l):
    print("Loading puntuaciones...")
        
    lista=[]
    fileobj=open(os.path.join(path, "ratings.csv"), "r")  
    for line in fileobj.readlines()[1:]:
        rip = line.split(',')
        if len(rip) != 3:
            continue
        lista.append(
            Puntuacion(
                idUsuario = u[int(rip[1].strip())],
                idLibro = l[int(rip[0].strip())],
                Puntuacion = int(rip[2].strip())
            )
        )
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Puntuaciones inserted: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")



def populateDatabase():
    deleteTables()
    u = populateUsuarios()
    l = populateLibros()
    populatePuntuaciones(u, l)  
    print("Finished database population")

    
if __name__ == '__main__':
   populateDatabase()