# %% [markdown]
# <a href="https://colab.research.google.com/github/Lucas303030/UADE_Progra1/blob/main/Progra_UADE_jnpy.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %%
import csv
import os
import random
# import pandas
from tabulate import tabulate
import datetime
from barcode import EAN13

# %%
def rnm_num():
    return ''.join([str(random.randint(0, 9)) for i in range(13)])

# %%
def timestamp():
    modificado = datetime.datetime.now()
    return modificado

# %%
def buscar_max(archivo):
    list_id = []
    try:
        with open(archivo, "r") as archivo:
            puntero = csv.DictReader(archivo)
            for line in puntero:
                list_id.append(line["id"])
            print(list_id)
            if len(list_id) != 0:
                maximo = int(max(list_id)) + 1
                return maximo
            else:
                return "1"
    except FileNotFoundError as error:
        print("No se puede leer el archivo")
        return "1"

# %%
def validar_dni():
    while True:
        dni = input("Ingrese DNI de cliente (Enter para omitir): ")
        if dni.strip() == "":
            return None  
        elif dni.isnumeric() and len(dni) == 8:
            return dni  # DNI válido, se retorna el valor ingresado
        else:
            print("DNI inválido. Debe contener 8 dígitos numéricos.")


# %%
def ing_cliente(): # Carga en archivo CSV
  id_cliente = buscar_max("clientes.csv")
  nombre_cliente = input("Ingrese nombre de cliente: ").capitalize()
  apellido_cliente = input("Ingrese apellido de cliente: ").capitalize()
  dni = validar_dni()

  # Diccionario que se inserta en cada linea de archivo clientes.csv

  cliente = {"id": id_cliente, 
             "nombre": nombre_cliente, 
             "apellido": apellido_cliente, 
             "dni": dni,
             "creado": timestamp(), 
             "modificado": timestamp()}
  
  encabezado = ["id", "nombre", "apellido", "dni", "creado", "modificado"]
  
  try:
    with open('clientes.csv', 'r', newline="") as archivo:
      """   
      lector = csv.reader(archivo)   
      for linea in lector:   
        print(linea)   
      """     
      pass

  except FileNotFoundError as error: # Si no existe, se crea archivo clientes
    # os.system("cls")
    print("\nEl archivo no existe, se crea nuevo\n")
    
    # print(error)

    with open("clientes.csv", "w", newline="") as archivo:
      puntero = csv.DictWriter(archivo, fieldnames=encabezado)
      puntero.writeheader()

  try:
    with open("clientes.csv", "a", newline="") as archivo:
      puntero = csv.DictWriter(archivo, fieldnames=encabezado)
      puntero.writerow(cliente)
      print("Registro guardado")
      
  except Exception as error:
    print("Ocurrió un error al escribir en el archivo CSV:", error) 

# %%
def ing_proveedor():
  nombre_proveedor = input("Ingrese nombre de proveedor: ")
  pass

# %%
def ing_prod_valor():
  valor_prod = float(input("Ingrese precio: "))
  pass

# %%
def ing_prod_cant():
  encabezado = ["id","codigo", "producto", "cantidad"]
  id = buscar_max("productos.csv")
  sku_prod = rnm_num()
  producto = input("Ingrese nombre: ").upper()
  cant_prod = input("Ingrese cantidad: ")
  productos = {"id": id, "codigo": sku_prod, "producto": producto, "cantidad": cant_prod}

  # Genera Codigo de Barras en ./barcodes

  ean = EAN13(sku_prod)
  ean.save("./barcodes/"f"{sku_prod}_barcode")

  try:
    with open("productos.csv", "r") as archivo:
      """lector = csv.reader(archivo)
      for linea in lector:
        print (linea)"""
  except FileNotFoundError as error:
    with open("productos.csv", "w", newline="") as archivo:
      puntero = csv.DictWriter(archivo, fieldnames=encabezado)
      puntero.writeheader()
  with open("productos.csv", "a", newline="") as archivo:
    puntero = csv.DictWriter(archivo, fieldnames=encabezado)
    puntero.writerow(productos)

# %%
def listar_clientes():
    tabla = []
    encabezado = ["id", "nombre", "apellido"]
    with open("clientes.csv", "r") as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            tabla.append(linea)

    print(f"\n{tabulate(tabla, headers='firstrow',tablefmt='presto')}\n")
    

# %%
def listar_productos():
    tabla = []
    encabezado = ["id","codigo", "producto", "cantidad"]
    with open("productos.csv", "r") as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            tabla.append(linea)

    print(f"\n{tabulate(tabla, headers='firstrow',tablefmt='presto')}\n")

# %%
def main_menu():

    os.system("cls")

    opciones_main = [
        "1- Ingresar cliente",
        "2- Ingresar proveedor",
        "3- Ingresar precio de producto",
        "4- Listar clientes",
        "5- Listar productos",
        "6- Ingresar producto",
        "7- Actualizar proveedores",
    ]

    for opcion in opciones_main:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-7): "))

            if 1 <= choice <= 7:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-7).")
        except ValueError:
            print("Entrada inválida. Ingrese un número del 1 al 7.")

    if choice == 1:
        ing_cliente()
    elif choice == 2:
        ing_proveedor()
    elif choice == 3:
        ing_prod_valor()
    elif choice == 4:
        listar_clientes()
    elif choice == 5:
        try:
            with open("productos.csv", "r") as archivo:
                listar_productos()
        except FileNotFoundError as error:
            print("No se encuentra el archivo")
    elif choice == 6:
        ing_prod_cant()
        pass
    elif choice == 7:
        pass
    else:
        print("Opción no válida")


# %%
main_menu()


