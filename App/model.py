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


from DISClib.DataStructures.chaininghashtable import nextPrime
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
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
                'artists' : None ,
               'Medium': None , 
               "Nationality" : None}

    """
    Esta lista contiene todas las artworks encontradas
    en los archivos de carga.  Estos libros no estan
    ordenados por ningun criterio.  Son referenciados
    por los indices creados a continuacion.
    """
    catalog['artworks'] = lt.newList('SINGLE_LINKED')
    catalog['artists'] = lt.newList('SINGLE_LINKED')
    

    """
    A continuacion se crean indices por diferentes criterios
    para llegar a la informacion consultada.  Estos indices no
    replican informacion, solo referencian los libros de la lista
    creada en el paso anterior.
    """
    
    """
    Este indice crea un map cuya llave es el "Constituent ID" del artista.
    """
    catalog["ID_artists_map"] =  mp.newMap(138000,
                                   maptype='CHAINING',
                                   loadfactor=1)
    """
    Este indice crea un map cuya llave es el medio.
    """
    catalog['Medium'] = mp.newMap(138000,
                                   maptype='CHAINING',
                                   loadfactor=1)
    """
    Este indice crea un map cuya llave es la nacionalidad de la obra.
    """

    catalog['Nationality'] = mp.newMap(300,
                                   maptype='CHAINING',
                                   loadfactor=1)
    """
    Este indice crea un map cuya llave es el año de nacimiento del artista.
    """
    catalog['Artist_Year'] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)


    catalog['Authors_Artwork'] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)
    
    catalog["Name_Artworks"] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)
    
    catalog["Adquisition_Artwork"] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)
    
    catalog["Adquisition_Date"] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)

    catalog["Artist_Artworks"] = mp.newMap(500,
                                   maptype='CHAINING',
                                   loadfactor=1)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    """
    """
    lt.addLast(catalog['artworks'], artwork)
    medium = artwork['Medium']  # Se obtienen la tecnica
    cons_id = artwork["ConstituentID"]

    
    addArtworkMedium(catalog, medium.strip(), artwork)
    addArtworksID(catalog, cons_id, artwork)
    create_name_map(catalog)
    adquisition_artwork(catalog , artwork)
    map_adquisition_date(catalog , artwork)

def map_adquisition_date(catalog , artwork):
    adq_date = artwork["DateAcquired"]
    exist = mp.contains(catalog["Adquisition_Date"] , adq_date)
    if exist:
        entry1 = mp.get(catalog["Adquisition_Date"] , adq_date)
        value = me.getValue(entry1)
    else:
        value = create_adq_entry(adq_date)
        mp.put(catalog["Adquisition_Date"] , adq_date , value)
    lt.addLast(value["artworks"] , artwork)

def create_adq_entry(adq_date):
    info = {'date': "", 
            'artworks' : None}
    info['date'] = adq_date
    info['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    
    return info




def adquisition_artwork(catalog , artwork):
    """
    Crea un map con la fecha de adquisición de cada artwork.
    """
    adq_date1 = artwork["DateAcquired"]
    year = 0
    month = 0
    day = 0
    if adq_date1 != "":
        adq_date = adq_date1.strip()
        adq_date_list = adq_date.split("-")
        year = int(adq_date_list[0])
        month = int(adq_date_list[1])
        day = int(adq_date_list[2])

    
    map = catalog["Adquisition_Artwork"]
    exist_year = mp.contains(map , year)
    if exist_year:
        key_value = mp.get(map , year)
        value_year = me.getValue(key_value)
    else:
        value_year = new_entry_year(year)
        mp.put(map , year , value_year)
    map_month = value_year["months"]
    try:
        exist_month = mp.contains(map_month , month)
    except:
        exist_month = False

    if exist_month:
        key_value_month = mp.get(map_month , month)
        value_month = me.getValue(key_value_month)

    else:
        value_month = new_entry_month(month)
        mp.put(map , month , value_month)
    
    map_days = value_month["days"]
    exist_day = mp.contains(map_days , day)

    if exist_day:
        key_value_day = mp.get(map_days , day)
        value_day = me.getValue(key_value_day)
    else:
        value_day = new_entry_day(day)
        mp.put(map_days , day , value_day)
    
    lt.addLast(value_day["artworks"] , artwork)

def new_entry_year(year):
    year_info = {'year': "", 'months' : None}
    year_info['year'] = year
    year_info['months'] = mp.newMap(500,
                            maptype='PROBING',
                            loadfactor=0.5 , comparefunction=compare_years)
    
    return year_info

def new_entry_month(month):
    month_info = {'months': "",
              "days": None}
    month_info['months'] = month
    month_info['days'] = mp.newMap(500,
                            maptype='CHAINING',
                            loadfactor=1 , comparefunction=compare_years)
    
    return month_info

def new_entry_day(day):
    day_info = {'day': "",
              "artworks": None}
    day_info['day'] = day
    day_info['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    return day_info

def create_name_map(catalog):
    map = catalog['Authors_Artwork']
    list_keys = mp.keySet(map)
    list_values = mp.valueSet(map)
    

def addArtist(catalog, artist):
    """
    """
    mp.put(catalog["ID_artists_map"] , artist["ConstituentID"] , artist)

    #Codigo para map año de nacimiento.
    year = int(artist["BeginDate"])
    add_map_year(catalog , year , artist)

def add_map_year(catalog , year , artist):
    map = catalog['Artist_Year']
    exist = mp.contains(map , year)
    if exist:
        entry = mp.get(map, year)
        info = me.getValue(entry)
    else:
        info = new_entry(year)
        mp.put(map , year , info)
    
    lt.addLast(info['artists'], artist)
    totalartists = lt.size(info['artists'])
    info['tot_artists'] = totalartists

def new_entry(year):
    """ 
    Crea una nueva estructura para modelar los artists que hallan nacido en
    un año en particular. Se crea una lista para guardar los
    artists en ese año.
    """

    year_info = {'year': "",
              "artists": None,
              "tot_artists": 0}
    year_info['year'] = year
    year_info['artists'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    return year_info

def create_artist_artwork_map(catalog):

    for artwork in lt.iterator(catalog["artworks"]):
        cons_id = artwork["ConstituentID"]
        cons_id = cons_id.strip("[] ")
        cons_id = cons_id.split(",")
        for author_id in cons_id:
            author_id_s = author_id
            #Se obtiene la llave valor del author de el map con indice cons id
            if mp.contains(catalog["ID_artists_map"] , author_id_s):
                author_key_value = mp.get(catalog["ID_artists_map"] , author_id_s)
                author_info = me.getValue(author_key_value)
                #Se obtiene la informacion del autor sacando el value del key-value
                name = author_info["DisplayName"]
                #Se saca la nacionalidad
                add_name(catalog , name , artwork)

def add_name(catalog , name , artwork):
    map_name = catalog["Artist_Artworks"]
    existname = mp.contains(map_name, name)
    if existname:
        entry = mp.get(map_name, name)
        name_info = me.getValue(entry)
    else:
        name_info = newName(name)
        mp.put(map_name, name, name_info)
    lt.addLast(name_info['artworks'], artwork)
    totalworks = lt.size(name_info['artworks'])
    name_info['tot_artworks'] = totalworks

    medium = artwork["Medium"]
    exist = mp.contains(name_info["Medium"] , medium)
    if exist:
        entry2 = mp.get(name_info["Medium"] , medium)
        medium_info = me.getValue(entry2)
    else:
        medium_info = new_medium(medium)
        mp.put(name_info["Medium"] , medium , medium_info)
    lt.addLast(medium_info["artworks"] , artwork)

def newName(nationality):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    name = {'name': "",
              "artworks": None,
              "Medium": None ,
              "tot_artworks": 0}
    name['name'] = nationality
    name['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    name["Medium"] = mp.newMap(500,
                    maptype='CHAINING',
                    loadfactor=1)
    return name

def new_medium(medium):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    medium = {'name': "",
              "artworks": None,
              "Medium": None ,
              "tot_artworks": 0}
    medium['name'] = medium
    medium['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    
    return medium


def create_nationality_map(catalog):

    for artwork in lt.iterator(catalog["artworks"]):
        cons_id = artwork["ConstituentID"]
        cons_id = cons_id.strip("[")
        cons_id = cons_id.strip("]")
        cons_id = cons_id.replace(" " , "")
        cons_id = cons_id.split(",")
        for author_id in cons_id:
            author_id_s = author_id
            #Se obtiene la llave valor del author de el map con indice cons id
            if mp.contains(catalog["ID_artists_map"] , author_id_s):
                author_key_value = mp.get(catalog["ID_artists_map"] , author_id_s)
                author_info = me.getValue(author_key_value)
                #Se obtiene la informacion del autor sacando el value del key-value
                nationality = author_info["Nationality"]
                #Se saca la nacionalidad
                add_nationality(catalog , nationality , artwork) #Funcion para añadir al map nationality


def add_nationality(catalog , nationality , artwork):
    map_nationality = catalog['Nationality']
    existnationality = mp.contains(map_nationality, nationality)
    if existnationality:
        entry = mp.get(map_nationality, nationality)
        nationality_info = me.getValue(entry)
    else:
        nationality_info = newNationality(nationality)
        mp.put(map_nationality, nationality, nationality_info)
    lt.addLast(nationality_info['artworks'], artwork)
    totalworks = lt.size(nationality_info['artworks'])
    nationality_info['tot_artworks'] = totalworks


def newNationality(nationality):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    nation = {'name': "",
              "artworks": None,
              "tot_artworks": 0}
    nation['name'] = nationality
    nation['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    return nation


def create_artists_map(catalog):

    for artwork in lt.iterator(catalog["artworks"]):
        cons_id = artwork["ConstituentID"].split(",")
        for author_id in cons_id:
            author_id_s = author_id.strip()
            #Se obtiene la llave valor del author de el map con indice cons id
            if mp.contains(catalog["ID_artists_map"] , author_id_s):
                author_key_value = mp.get(catalog["ID_artists_map"] , author_id_s)
                author_info = me.getValue(author_key_value)
                #Se obtiene la informacion del autor sacando el value del key-value
                nationality = author_info["Nationality"].strip()
                #Se saca la nacionalidad
                add_nationality(catalog , nationality , artwork) #Funcion para añadir al map nationality

# Funciones para creacion de datos

def addArtworkMedium(catalog, mediumname, artwork):
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


def addArtworksID(catalog, cons_id, artwork):
    map = catalog['Authors_Artwork']
    for id in cons_id:
        exist = mp.contains(map, id)
    if exist:
        entry = mp.get(map, id)
        info = me.getValue(entry)
    else:
        info = new_entry(id)
        mp.put(map , id , info)
    
    lt.addLast(info['artists'], artwork)
    totalartworks = lt.size(info['artists'])
    info['tot_artists'] = totalartworks

def newID(id):
 
    id_artist = {'id': "",
              "artworks": None,
              "tot_artworks": 0}
    id_artist['id'] = id
    id_artist['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksByName)
    return id_artist

# Funciones de consulta

def find_medium(catalog , medium):
    art_list = mp.get(catalog["Medium"] , medium)
    art_list2 = me.getValue(art_list)
    new_list = sort_art_list(art_list2)
    return new_list

def count_artworks(catalog , nationality):
    """
    Esta función recibe el catalogo y una nacionalidad y cuenta el numero de obras de arte
    asociadas a la nacionalidad (key) en su value (lista de artworks)
    """
    map_nationality = catalog["Nationality"]
    list_nationality = mp.get(map_nationality , nationality)
    value = me.getValue(list_nationality)
    list_artworks = value["artworks"]
    number_of_artworks = lt.size(list_artworks)
    return number_of_artworks

def artists_year_listing(initial_year , final_year , catalog):
    """
    Función del requerimiento 1 para encontrar artistas en rango de años.
    """

    artists_list = lt.newList("ARRAY_LIST")
    for year in range(initial_year , final_year + 1):
        entry = mp.get(catalog['Artist_Year'] , year)
        value = me.getValue(entry)
        artist_list = value["artists"]
        for artist in lt.iterator(artist_list):
            lt.addLast(artists_list , artist)
    
    return artists_list

def find_adq_date(catalog , initial_date_list , final_date_list):

    initial_year = int(initial_date_list[0])
    initial_month = int(initial_date_list[1])
    initial_day = int(initial_date_list[2])

    final_year = int(final_date_list[0])
    final_month = int(final_date_list[1])
    final_day = int(final_date_list[2])

    final_list = lt.newList()

    for year in range(initial_year , final_year + 1):
        if mp.contains(catalog["Adquisition_Artwork"] , year):
            key_value_year = mp.get(catalog["Adquisition_Artwork"] , year)
            value_year = me.getValue(key_value_year)
            i_m = 1
            f_m = 12
            i_d = 1
            f_d = 31
            if year == initial_year:
                i_m = initial_month
                i_d = initial_day
            if year == final_year:
                f_m = final_month
                f_d = final_day
            for month in range(i_m , f_m + 1):
                try:
                    if mp.contains(value_year["months"] , month):
                        key_value_month = mp.get(value_year["months"] , month)
                        value_month = me.getValue(key_value_month)
                        for day in range(i_d , f_d + 1):
                            key_value_day = mp.get(value_month["days"] , day)
                            value_day = me.getValue(key_value_day)
                            artwork = value_day["artworks"]
                            lt.addLast(final_list , artwork)
                except: 
                    continue
                    
    return final_list

def req2(catalog , initial_date_list , final_date_list):
    list_dates = mp.keySet(catalog["Adquisition_Date"])
    new_list = lt.newList()
    purchased_list = lt.newList()
    for date in lt.iterator(list_dates):
        if compare_dates(date , initial_date_list , final_date_list):
            key_value = mp.get(catalog["Adquisition_Date"] , date)
            value = me.getValue(key_value)
            for element in lt.iterator(value["artworks"]):
                lt.addLast(new_list , element)
    
    for element in lt.iterator(new_list):
        if element["CreditLine"] == "Purchase":
            lt.addLast(purchased_list , element)

    new_list_sorted = mer.sort(new_list, cmpArtworkByDateAcquired)

    return new_list_sorted , purchased_list

def rank_nationality(catalog):
    nationalities = mp.keySet(catalog["Nationality"])
    dict_countries_artworks = {}
    dict_countries = {}
    for nationality in lt.iterator(nationalities):
        nation_key_value = mp.get(catalog["Nationality"] , nationality)
        nation_value = me.getValue(nation_key_value)
        tot_artworks = lt.size(nation_value["artworks"])
        dict_countries[nationality] = tot_artworks
        dict_countries_artworks[nationality] = nation_value["artworks"]
    list_countries = list(dict_countries.items())
    list_countries.sort(key=lambda x:x[1])

    return dict_countries_artworks , list_countries



def compare_dates(fecha_map , initial_date_list , final_date_list):
    fecha_map_list = fecha_map.split("-")
    ret_value = False
    if fecha_map != "":
        if fecha_map_list[0] >= initial_date_list[0] and fecha_map_list[0] <= final_date_list[0]:
                ret_value = True
    return ret_value

def medium(catalog , artist):
    map = catalog["Artist_Artworks"]
    info = mp.get(map , artist)
    valor = me.getValue(info)
    size_artworks = lt.size(valor["artworks"])
    size_medium = mp.size(valor["Medium"])

    map_medium = valor["Medium"]
    keys = mp.keySet(map_medium)
    most_used_medium = None
    for medium_k in lt.iterator(keys):
        element = mp.get(map_medium , medium_k)
        value = me.getValue(element)
        size = lt.size(value["artworks"])
        


    return size_artworks , size_medium
    


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

def compareArtworksByName(keyname, author):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(author)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compare_years(keyname, artwork):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(artwork)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
def sort_art_list (art_list):
    sub_list = lt.subList(art_list , 1 , lt.size(art_list))
    sorted_list = sa.sort(sub_list , cmpArtworkByDateAcquired)
    return sorted_list

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menor que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    f1 = artwork1["DateAcquired"]
    f2 = artwork2["DateAcquired"]
    f1_lst = f1.split("-")
    f2_lst = f2.split("-")
    ret = None 

    if len(f1_lst) > len(f2_lst):
        ret = False
    elif len(f1_lst) < len(f2_lst):
        ret = True
    elif len(f1_lst) == 3 and len(f2_lst) == 3:
        if f1_lst[0] < f2_lst[0]:
            ret = True
        elif f1_lst[0] > f2_lst[0]:
            ret = False
        elif f1_lst[0] == f2_lst[0]:
            if f1_lst[1] < f2_lst[1]:
                ret = True
            elif f1_lst[1] > f2_lst[1]:
                ret = False
            else:
                if f1_lst[2] < f2_lst[2]:
                    ret = True
                elif f1_lst[2] > f2_lst[2]:
                    ret = False
                else:
                    ret = False
    return ret