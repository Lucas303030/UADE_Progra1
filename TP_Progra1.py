import os
import random
from tabulate import tabulate
import datetime

def validar_CUIT():
    while True:
        CUIT = input("Ingrese CUIT de cliente (Enter para omitir): ")
        if CUIT.isnumeric() and len(CUIT) == 11:
            return CUIT
        else:
            print("CUIT inválido. Debe contener exactamente 11 dígitos numéricos.")

def eliminar_archivo(ruta):
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

def listar_clientes():
    
    try:
        tabla = []
        archivo = open("clientes.txt", "r")
        for linea in archivo:
            palabra = linea.split(",")
            tabla.append(palabra)

        print(f"\n{tabulate(tabla, headers=['id', 'mombre', 'apellido', 'DNI', 'CUIT', 'creado', 'modificado'],tablefmt='presto')}\n")
    except FileNotFoundError as error:
        print ("No se puede abrir el archivo", error)
    finally:
        try:
            archivo.close()
        except FileNotFoundError as error:
            pass

def timestamp():
    modificado = datetime.datetime.now()
    return modificado

def borrar_registro_clientes():
    registro = input("Seleccionar registro a eliminar: ")
    
    archivo_original = "clientes.txt"
    archivo_temporal = "clientes_temp.txt"
    
    encontrado = False
    
    try:
        entrada = open(archivo_original, 'r')
        salida = open(archivo_temporal, 'w')
        
        for linea in entrada:
            if linea[0] == registro:
                encontrado = True
            else:
                salida.write(linea)
        
        entrada.close()
        salida.close()
        
        if encontrado:
            print(f"Registro '{registro}' eliminado con éxito.")
        else:
            print(f"Registro '{registro}' no encontrado en el archivo.")
        
        os.remove(archivo_original)
        os.rename(archivo_temporal,archivo_original)

    except FileNotFoundError:
        print(f"El archivo '{archivo_original}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

def editar_cliente(id_cliente, nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_cuit):

    with open("clientes.txt", "r") as archivo:
        lineas = archivo.readlines()

    encontrado = False

    with open("clientes.txt", "w") as archivo:

        for linea in lineas:
            datos = linea.strip().split(',')
            if datos[0] == id_cliente:
                # Editar los campos del cliente
                datos[1] = nuevo_nombre
                datos[2] = nuevo_apellido
                datos[3] = nuevo_dni
                datos[4] = nuevo_cuit
                datos[-1] = str(timestamp()) 
                nueva_linea = ','.join(datos) + '\n'
                archivo.write(nueva_linea)
                encontrado = True
            else:
                archivo.write(linea)

    if encontrado:
        print("\nCliente editado con éxito.\n")
    else:
        print(f"No se encontró un cliente con el ID {id_cliente}.")


def rnm_num():
    return ''.join([str(random.randint(0, 9)) for i in range(13)])

def buscar_max(archivo):
    list_id = []
    try:
        with open(archivo, "r") as archivo:
            for line in archivo:
                list_id.append(line[0])
            print(list_id)
            if len(list_id) != 0:
                maximo = int(max(list_id)) + 1
                return maximo
    except FileNotFoundError as error:
        print("No se puede leer el archivo")
        return "1"

def validar_dni():
    while True:
        dni = input("Ingrese DNI de cliente (Enter para omitir): ")
        if dni.strip() == "":
            return None 
        elif dni.isnumeric() and len(dni) == 8:
            return dni
        else:
            print("DNI inválido. Debe contener exactamente 8 dígitos numéricos.")

def ing_cliente():

    continuar = "S"

    while continuar == "S":
        id_cliente = buscar_max("clientes.txt")
        nombre_cliente = input("Ingrese nombre de cliente: ").capitalize()
        apellido_cliente = input("Ingrese apellido de cliente: ").capitalize()
        dni = validar_dni()
        cuit = validar_CUIT()

        cliente = {
            "id": id_cliente,
            "nombre": nombre_cliente,
            "apellido": apellido_cliente,
            "dni": dni,
            "cuit": cuit,
            "creado": timestamp(),
            "modificado": timestamp()
        }

        data_cliente = f"{cliente['id']},{cliente['nombre']},{cliente['apellido']},{cliente['dni']},{cliente['cuit']},{cliente['creado']},{cliente['modificado']}\n"

        try:
            archivo = open("clientes.txt", "a")
            archivo.write(data_cliente)
            print("Registro guardado")

        except Exception as error:
            print("Ocurrió un error al escribir en el archivo:", error)

        finally:
            if continuar == "S":
                try:
                    archivo.close()
                    continuar = input("¿Agregar otro registro (S/N) ?: ").upper()
                except FileNotFoundError as error:
                    pass
            else:
                try:
                    archivo.close()
                except FileNotFoundError as error:
                    pass

def ing_proveedor():
  nombre_proveedor = input("Ingrese nombre de proveedor: ")
  pass

def ing_prod_valor():
  valor_prod = float(input("Ingrese precio: "))
  pass

def ing_prod_cant():
  id = buscar_max("productos.txt")
  sku_prod = rnm_num()
  producto = input("Ingrese SKU: ").upper()
  cant_prod = input("Ingrese cantidad: ")
  productos = {"id": id, "sku": sku_prod, "producto": producto, "cantidad": cant_prod}

  data_productos = f"{productos['id']},{productos['sku']},{productos['producto']},{productos['cantidad']}\n"

  try:
      with open("productos.txt", "a") as archivo:
          archivo.write(data_productos)
      print("Registro guardado")
  except Exception as error:
      print("Ocurrió un error al escribir en el archivo:", error)

def listar_productos():
    tabla = []
    try:
        archivo = open("productos.txt", "r")
        for linea in archivo:
            palabra = linea.split(",")
            tabla.append(palabra)
        print(f"\n{tabulate(tabla, headers=['ID','SKU','Producto','Cantidad'],tablefmt='presto')}\n")
    except FileNotFoundError as error:
        print (error)
    finally:
        try:
            archivo.close()
        except NameError as error:
            pass

def main_menu():

    os.system("cls")

    opciones_main = [
        "1- Ingresar cliente",
        "2- Ingresar proveedor",
        "3- Actualizar precios de productos",
        "4- Listar clientes",
        "5- Listar productos",
        "6- Ingresar producto",
        "7- Actualizar clientes",
        "8- Borrar registro clientes",
        "9- Borrar todos los productos",
        "10- Borrar todos los clientes"
    ]

    for opcion in opciones_main:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-10): "))

            if 1 <= choice <= 10:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-10).")
        except ValueError:
            print("Entrada inválida. Ingrese un número del 1 al 10.")

    if choice == 1:
        ing_cliente()
    elif choice == 2:
        ing_proveedor()
    elif choice == 3:
        ing_prod_valor()
    elif choice == 4:
        listar_clientes()
    elif choice == 5:
        listar_productos()
    elif choice == 6:
        ing_prod_cant()
        pass
    elif choice == 7:
        listar_clientes()
        id_busqueda = input("Ingrese ID a editar: ")
        nuevo_nombre = input("Ingrese nuevo nombre: ")
        nuevo_apellido = input("Ingrese nuevo apellido: ")
        nuevo_DNI = validar_dni()
        nuevo_cuit = validar_CUIT
        editar_cliente(id_busqueda,nuevo_nombre,nuevo_apellido,nuevo_DNI,nuevo_cuit)
        main_menu()
    elif choice == 8:
        listar_clientes()
        borrar_registro_clientes()
    elif choice == 9:
        eliminar_archivo("productos.txt")
    elif choice == 10:
        eliminar_archivo("clientes.txt")    
    else:
        print("Opción no válida")


main_menu()


