import os
from tabulate import tabulate

def procesar(pathArchivo): #Pasar lista de columas si se quiere filtrar
    try:
        registros = []
        archivo = open(pathArchivo, "r")
        for linea in archivo:
            campos = linea.split(",")
            registros[-1] = registros[-1].rstrip()
            registros.append(campos)
        return registros
    except FileNotFoundError as error:
        print ("No se puede abrir el archivo", error)
        return []
    finally:
        try:
            archivo.close()
        except FileNotFoundError as error:
            pass


def eliminar(ruta):
    if os.path.exists(ruta):
        confirmacion = input(f"Ingresar nombre de archivo para confirmar: ({ruta})")
        if ruta == confirmacion:
            os.remove(ruta)
            print(f"El archivo {ruta} ha sido eliminado.")
        else: 
            print("Cancelado")
            return ""
    else:
        print(f"No se encuentra el archivo {ruta}.")

