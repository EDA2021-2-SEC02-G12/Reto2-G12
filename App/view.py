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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1 - Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3 - Encontrar obras más antiguas para un medio")
    print("4 - Contar el número total de obras de una nacionalidad")

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
        controller.loadData(catalog)
    
    elif int(inputs[0]) == 3:
        medio = input("Ingrese el nombre del medio: ")
        numero_obras = int(input("Ingrese el valor de n"))
        sorted_list = controller.find_medium(catalog , medio.strip())
        printAntiguas(sorted_list , numero_obras)
    
    elif int(inputs[0]) == 4:
        nationality = input("Ingrese la nacionalidad: ")
        numero_obras = controller.count_artworks(catalog , nationality)
        print_artworks_by_nationality(numero_obras , nationality)

    else:
        sys.exit(0)
sys.exit(0)
