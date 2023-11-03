import os
import random
from tabulate import tabulate
import datetime

def venta():
    listar_clientes()
    id_cliente = str(input("Ingrese cliente: "))
    try:
        with open("clientes.txt", "r") as archivo:
            for line in archivo:
                lista_campos = line.split(",")
                if lista_campos[0] == id_cliente:
                    # print(lista_campos[1], lista_campos[2], lista_campos[4])
                    pass
    except FileNotFoundError:
        pass
    venta2()

def mostrar_productos_filtrados(categoria):
    def filtro(categoria, linea):
        return categoria in linea

    tabla = []
    try:
        with open("productos.txt", "r", encoding="UTF-8") as archivo:
            filtradas = filter(lambda linea: filtro(categoria, linea), archivo)
            for linea in filtradas:
                productos = linea.split(",")
                tabla.append(productos)

        print(tabulate(tabla))

    except FileNotFoundError as error:
        print(error)

def venta2():
    categorias, _ = listar_productos()
    
    for i in categorias:
        print(i)
    categoria = input("Ingrese el nombre de la categoria: ")
    categoria = categoria.upper()
    mostrar_productos_filtrados(categoria)
    
def validar_CUIT():
    while True:
        CUIT = input("Ingrese CUIT de cliente (Enter para omitir): ")
        if CUIT.isnumeric() and len(CUIT) == 11 and CUIT != "":
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

        print(f"\n{tabulate(tabla, headers=['ID', 'Nombre', 'Apellido', 'DNI', 'CUIT', 'Creado', 'Modificado'],tablefmt='presto')}\n")
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
    #Borrado logico
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

def validar_dni():# Agregar excepciones
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
        nombre_cliente = input("Ingrese nombre de cliente: ").capitalize() #Agregar not isnumeric
        apellido_cliente = input("Ingrese apellido de cliente: ").capitalize()
        dni = validar_dni()
        cuit = validar_CUIT()

        cliente = {
            "ID": id_cliente,
            "Nombre": nombre_cliente,
            "Apellido": apellido_cliente,
            "DNI": dni,
            "CUIT": cuit,
            "Creado": timestamp(),
            "Modificado": timestamp()
        }

        data_cliente = f"{cliente['ID']},{cliente['Nombre']},{cliente['Apellido']},{cliente['DNI']},{cliente['CUIT']},{cliente['Creado']},{cliente['Modificado']}\n"

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
  nombre_proveedor = input("Ingrese nombre de proveedor: ") #Agregar proveedor a proveedores.txt
  pass

def ing_prod_valor():
  valor_prod = float(input("Ingrese precio: "))
  pass

def ing_prod_cant():
  id = buscar_max("productos.txt")
  nombre = input("Ingrese nombre del producto: ").upper()
  rubro = input("Ingrese rubro: ").upper()
  marca = input("Ingrese marca: ")
  proveedor = input("Ingrese proveedor: ")
  cantidad = int(input("Ingrese cantidad: "))
  productos = {"ID": id, "Nombre": nombre, "Rubro": rubro, "Marca": marca, "Proveedor": proveedor, "Cantidad": cantidad} #Agregar campo precio

  data_productos = f"{productos['ID']},{productos['Nombre']},{productos['Rubro']},{productos['Proveedor']}, {productos['Cantidad']}\n"

  try:
      with open("productos.txt", "a") as archivo:
          archivo.write(data_productos)
      print("Registro guardado")
  except Exception as error:
      print("Ocurrió un error al escribir en el archivo:", error)

def listar_productos():
    tabla = []
    categorias = []
    try:
        archivo = open("productos.txt", "r", encoding="UTF-8")
        for linea in archivo:
            palabra = linea.split(",")
            tabla.append(palabra)
            if not palabra[2] in categorias:
                categorias.append(palabra[2])
        
        
    except FileNotFoundError as error:
        print (error)
    finally:
        return categorias, (f"\n{tabulate(tabla, headers=['ID','Nombre','Rubro','Proveedor', 'Cantidad'],tablefmt='presto', showindex='never', maxcolwidths=[None, 60])}\n")
        try:
            archivo.close()
        except NameError as error:
            pass



def ingresos():
    opciones_ingresos = [
        "1- Ingresar cliente",
        "2- Ingresar proveedor",
        "3- Ingresar producto",
    ]

    for opcion in opciones_ingresos:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-3): "))

            if 1 <= choice <= 3:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-3).")

        except ValueError:

            print("Entrada inválida. Ingrese un número del 1 al 3.")
    if choice == 1:
        ing_cliente()
    elif choice == 2:
        ing_proveedor()
    elif choice == 3:
        ing_prod_valor()

def actualizaciones():
    opciones_actualizaciones = [

        "1- Actualizar precios de productos",
        "2- Actualizar clientes",
    ]

    for opcion in opciones_actualizaciones:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-2): "))

            if 1 <= choice <= 2:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-2).")

        except ValueError:

            print("Entrada inválida. Ingrese un número del 1 al 2.")
    if choice == 1:
        ing_prod_valor()
    elif choice == 2:
        listar_clientes()
        id_busqueda = input("Ingrese ID a editar: ")
        nuevo_nombre = input("Ingrese nuevo nombre: ")
        nuevo_apellido = input("Ingrese nuevo apellido: ")
        nuevo_DNI = validar_dni()
        nuevo_cuit = validar_CUIT
        editar_cliente(id_busqueda,nuevo_nombre,nuevo_apellido,nuevo_DNI,nuevo_cuit)
        main_menu()
        
def listados():
    opciones_listados = [
        "1- Listar clientes",
        "2- Listar productos",
        
    ]

    for opcion in opciones_listados:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-2): "))

            if 1 <= choice <= 2:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-2).")

        except ValueError:

            print("Entrada inválida. Ingrese un número del 1 al 2.")
    if choice == 1:
        listar_clientes()
    elif choice == 2:
        a, b = listar_productos()
        print (b)

def borrar():
        opciones_borrar =[
        "1- Borrar registro clientes",
        "2- Borrar todos los productos",
        "3- Borrar todos los clientes",
    ]

        for opcion in opciones_borrar:
            print(opcion)

        while True:
            try:
                choice = int(input("Seleccione una opción (1-3): "))

                if 1 <= choice <= 3:
                    break
                else:
                    print("Opción fuera de rango. Seleccione una opción válida (1-3).")

            except ValueError:

                print("Entrada inválida. Ingrese un número del 1 al 3.")
        if choice == 1:
            listar_clientes()
            borrar_registro_clientes()
        elif choice == 2:
            eliminar_archivo("productos.txt")
        elif choice ==3:
            eliminar_archivo("clientes.txt") 




def main_menu():

    os.system("cls")

    opciones_main = [
        "1- Ingresos",
        "2- Actualizaciones",
        "3- Listados",
        "4- Borrar",
        "5- Venta",
    ]

    

    for opcion in opciones_main:
        print(opcion)

    while True:
        try:
            choice = int(input("Seleccione una opción (1-5): "))

            if 1 <= choice <= 5:
                break
            else:
                print("Opción fuera de rango. Seleccione una opción válida (1-5).")
        except ValueError:
            print("Entrada inválida. Ingrese un número del 1 al 5.")

    if choice == 1:
            ingresos()
    elif choice == 2:
            actualizaciones()
    elif choice == 3:
            listados()
    elif choice == 4:
            borrar()
    elif choice == 5:
            venta() 
    else:
        print("Opción no válida")


main_menu()
