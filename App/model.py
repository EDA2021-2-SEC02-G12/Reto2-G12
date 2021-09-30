"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

from DISClib.Algorithms.Sorting import mergesort as mg

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el catálogo.

    Crea una lista vacia para guardar todas las artworks.

    Se crean indices (Maps) por los siguientes criterios:
    Medio

    Retorna el catalogo inicializado.
    """
    catalog = {'artworks': None,
               'Medium': None}

    """
    Esta lista contiene todas las artworks encontradas
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['artworks'] = lt.newList('SINGLE_LINKED')

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """

    """
    Este indice crea un map cuya llave es el identificador del libro
    """
    catalog['Medium'] = mp.newMap(138000,
                                   maptype='CHAINING',
                                   loadfactor=4.0)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    """
    """
    lt.addLast(catalog['artworks'], artwork)
    medium = artwork['Medium']  # Se obtienen la tecnica
    addArtworkMedium(catalog, medium.strip(), artwork)

# Funciones para creacion de datos

def addArtworkMedium(catalog, mediumname, artwork):
    """
    Esta función adiciona un libro a la lista de libros publicados
    por un autor.
    Cuando se adiciona el libro se actualiza el promedio de dicho autor
    """
    mediums = catalog['Medium']
    existmedium = mp.contains(mediums, mediumname)
    if existmedium:
        entry = mp.get(mediums, mediumname)
        medium_lst = me.getValue(entry)
        lt.addLast(medium_lst , artwork)
    else:
        empty_lst = lt.newList()
        lt.addLast(empty_lst , artwork) 
        mp.put(mediums, mediumname, empty_lst)

# Funciones de consulta

def find_medium(catalog , medium):
    art_list = mp.get(catalog["Medium"] , medium)
    art_list2 = me.getValue(art_list)
    new_list = sort_art_list(art_list2)
    return new_list


# Funciones utilizadas para comparar elementos dentro de una lista

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    f1 = artwork1["Date"].strip()
    f2 = artwork2["Date"].strip()
    
    if (len(f1) == 0) or (len(f2) == 0):
        if f1 == f2:
            return 1
        elif len(f1) < len(f2):
            return 1
        else:
            return 0
    
    f1 = int(f1)
    f2 = int(f2)

    if f1 < f2:
        return 1
    elif f1 > f2:
        return 0
    else:
        return 1
# Funciones de ordenamiento
def sort_art_list (art_list):
    sub_list = lt.subList(art_list , 1 , lt.size(art_list))
    sorted_list = sa.sort(sub_list , cmpArtworkByDateAcquired)
    return sorted_list