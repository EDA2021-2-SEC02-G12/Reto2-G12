"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1 - Inicializar Catálogo")
    print("2 - Cargar información en el catálogo")
    print("3 - Encontrar obras más antiguas para un medio")
    print("4 - Contar el número total de obras de una nacionalidad")
    print("5 - Listar cronológicamente los artistas")
    print("6 - Listar cronológicamente las adquisiciones")
    print("7 - Clasificar las obras de un artista por técnica")
    print("8 - Clasificar las obras por la nacionalidad de sus creadores")
catalog = None


def printAntiguas(sorted_list , numero_obras):
    print("Las"  + str(numero_obras) + " mas antiguas son: ")
    if numero_obras <= lt.size(sorted_list):
        for i in range(1 , numero_obras + 1):
            artwork = lt.getElement(sorted_list , i)
            print("Titulo: " + str(artwork["Title"]) + " Año: " + str(artwork["Date"]))
    else:
        print("n es muy grande")

def print_artworks_by_nationality(numero_obras , nationality):
    """
    Imprime el numero de obras dado un país.
    
    """
    print("El número de obras de nacionalidad " + str(nationality) + " es " + str(numero_obras))

def print_req_1(list_artists):
    print("El numero de artistas en el rango seleccionado es: " + str(lt.size(list_artists)))
    print("Los 3 primeros artistas son: ")
    for i in range(1 , 4):
        element = lt.getElement(list_artists , i)
        print("Nombre: " + str(element["DisplayName"]) + " Año de Nacimiento: " + str(element["BeginDate"])
        + " Año de Fallecimiento: " + str(element["EndDate"]) + "Nacionalidad: " + str(element["Nationality"])
        + " Género: " + str(element["Gender"]))
    
    print("Los 3 últimos artistas son: ")
    for j in range (lt.size(list_artists) , lt.size(list_artists)-3 , -1):
        element = lt.getElement(list_artists , j)
        print("Nombre: " + str(element["DisplayName"]) + " Año de Nacimiento: " + str(element["BeginDate"])
        + " Año de Fallecimiento: " + str(element["EndDate"]) + "Nacionalidad: " + str(element["Nationality"])
        + " Género: " + str(element["Gender"]))

def print_req2(list_adq , list_pur):
    print("El número total de obras en el rango cronólógico es: " + str(lt.size(list_adq)))
    print("El numero de obras adquiridas por purchase es: " + str(lt.size(list_pur)))
    print("Las 3 primeras obras son: ")
    for i in range(1, 4):
        artwork = lt.getElement(list_adq , i)
        print("Titulo: " + str(artwork["Title"]) + "Fechas: " + str(artwork["DateAcquired"])
        + " Medio: " + str(artwork["Medium"]) + " Dimensiones: "
        + str(artwork["Dimensions"]))
    print("Las 3 ultimas son: ")
    for j in range(lt.size(list_adq)-3, lt.size(list_adq)):
        artwork = lt.getElement(list_adq , j)
        print("Titulo: " + str(artwork["Title"]) + "Fechas: " + str(artwork["DateAcquired"])
        + " Medio: " + str(artwork["Medium"]) + " Dimensiones: "
        + str(artwork["Dimensions"]))

def print_countries_ranked(dict_countries , list_countries_ranked):
    print("El top 10 de paises en el moma es: ")
    sample = len(list_countries_ranked) - 10
    counter = len(list_countries_ranked)
    biggest_country = list_countries_ranked[counter - 1]
    while counter > sample:
        country = list_countries_ranked[counter - 1]
        print(country)
        counter -= 1
    print("Las 3 primeras y las 3 ultimas obras de " + biggest_country[0] + " son: ")
    biggest = dict_countries[biggest_country[0]]
    index = 1
    while index < 4:
        artwork = lt.getElement(biggest , index)
        print('Titulo: ' + artwork["Title"] + ' Fecha de la obra: ' +
                artwork["DateAcquired"] + ' Medio: ' + artwork["Medium"] +  ' Dimensiones ' + artwork["Dimensions"])
        index += 1

    index = lt.size(biggest)
    while index > (lt.size(biggest) - 3):
        artwork = lt.getElement(biggest , index)
        print('Titulo: ' + artwork["Title"] + ' Fecha de la obra: ' +
                artwork["DateAcquired"] + ' Medio: ' + artwork["Medium"] +  ' Dimensiones ' + artwork["Dimensions"])
        index -= 1

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        time1 = controller.loadData(catalog)
        print("El tiempo es:" , str(time1))
    
    elif int(inputs[0]) == 3:
        medio = input("Ingrese el nombre del medio: ")
        numero_obras = int(input("Ingrese el valor de n"))
        sorted_list = controller.find_medium(catalog , medio.strip())
        printAntiguas(sorted_list , numero_obras)
    
    elif int(inputs[0]) == 4:
        nationality = input("Ingrese la nacionalidad: ")
        numero_obras = controller.count_artworks(catalog , nationality)
        print_artworks_by_nationality(numero_obras , nationality)
    
    elif int(inputs[0]) == 5:
        initial_year = int(input("Ingrese el año inicial: "))
        final_year = int(input("Ingrese el año final: "))
        list = controller.artists_year_listing(initial_year , final_year , catalog)
        print_req_1(list)
    
    elif int(inputs[0]) == 6:
        initial_date = input("Ingrese la fecha inicial: ")
        final_date = input("Ingrese la fecha final: ")
        initial_date_list = initial_date.split("-")
        final_date_list = final_date.split("-")
        list_adq = controller.req2(catalog , initial_date_list , final_date_list)
        print_req2(list_adq[0] , list_adq[1])
    
    elif int(inputs[0]) == 7:

        artist = input("Ingrese el nombre: ")
        list = controller.rank_nationality(catalog , artist)
        print("Total de obras: " + str(list[0]))
        print("Total de tecnicas: " + str(list[1]))
        

    elif int(inputs[0]) == 8:

        list = controller.medium(catalog)
        print_countries_ranked(list[0] , list[1])
        

    else:
        sys.exit(0)
sys.exit(0)
