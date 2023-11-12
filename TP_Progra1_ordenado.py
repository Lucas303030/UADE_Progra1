import os
import random
import datetime

COLUMNAS_PRODUCTOS = ['ID', 'Nombre', 'Cat.', 'Marca', 'proov.', 'Precio', 'Stock']
COLUMNAS_CLIENTES = ['id', 'Nombre', 'Apellido', 'DNI', 'CUIL', 'Fecha alta', 'Fecha modificacion']
COLUMNAS_VENTAS = []

def tabulador(registros, columnas):
    anchos = []
    for columna in range(len(columnas)):
        ancho = 7
        for linea in registros:
            if columna < len(linea):  # Verifica que el índice sea válido
                ancho_palabra = len(str(linea[columna]))
                if ancho_palabra > ancho:
                    ancho = ancho_palabra
        anchos.append(ancho) 
    
    print(anchos)
    
    encabezado = " | ".join(f'{columnas[x]:{anchos[x]}}' for x in range(len(columnas)))
    separador = " + ".join("-"*anchos[x] for x in range(len(columnas)))

    filas_datos = []
    for fila in registros:
        fila_datos = " | ".join(f'{fila[x]:{anchos[x]}}' if x < len(fila) else ' ' * anchos[x] for x in range(len(columnas)))
        filas_datos.append(fila_datos)

    tabla = f'{encabezado}\n{separador}\n' + '\n'.join(filas_datos)

    return tabla

def carrito(num_carrito):
    print(f"\nNumero de orden: {num_carrito}\n")
    with open("ventas.txt", "r", encoding="UTF-8") as archivo:
        total = 0   
        for linea in archivo:
            campos = linea.split(",")
            if campos[0] == str(num_carrito):
                total += float(campos[4])
                print(f"Producto: {campos[2]}, Unidad/es: {campos[3]}, Total: $ {campos[4]}")
        print (f"Total: $ {total}")

def venta():
    clientes = leer_clientes()
    print(tabulador(clientes, COLUMNAS_CLIENTES))
    cliente_encontrado = 0
    id = input('Ingrese id de cliente')
    while cliente_encontrado == 0: 
        for cliente in clientes:
            if cliente[0] == id:
                cliente_encontrado = id
        if cliente_encontrado == 0:
            print('No se encontró el cliente')
            id = input('Ingrese id de cliente')

    num_carrito = buscar_max("ventas.txt")
    print(f"Numero de orden: {num_carrito}")
    continuar = "S"
    while continuar == "S":
        categorias, productos = leer_productos()
        
        print(tabulador([[x] for x in categorias], ['Categorias']))

        categoria_encontrada = 0
        categoria = f'"{input("Ingrese el nombre de la categoria: ").upper()}"'
        
        while categoria_encontrada == 0:
            if categoria in categorias:
                categoria_encontrada = categoria
            else:
                print('No se encontró la categoría')
                categoria = input("Ingrese el nombre de la categoria: ")

        def filtro(categoria, linea):
            return categoria in linea
        productos_filtrados = list(filter(lambda linea: filtro(categoria, linea), productos)) 
        print(tabulador(productos_filtrados,COLUMNAS_PRODUCTOS))
        
        producto_encontrado = 0
        id = input('Ingrese id de producto')
        while producto_encontrado == 0: 
            for producto in productos_filtrados:
                if producto[0] == id:
                    producto_encontrado = id
                    nombre_prdo = producto[1]
                    precio_unidad = producto[5]
            if producto_encontrado == 0:
                print('No se encontró el producto')
                id = input('Ingrese id de producto')

        print('Producto seleccionado exitosamente: '+id)

        while True:
            try:
                cantidad = int(input('Ingrese cantidad vendida '))
                break
            except TypeError:
                print('introduzca una cantidad valida ') 

        total = float(precio_unidad) * cantidad
        id = buscar_max('ventas.txt')
        data_venta =  f"{num_carrito},{cliente_encontrado},{nombre_prdo},{cantidad},{total},{timestamp()},{timestamp()}\n"
        print(f"Datos venta:\n{data_venta}" )

    
        try:
            archivo = open("ventas.txt", "a")
            archivo.write(data_venta)
            print("Registro guardado")
        except Exception as error:
            print("Ocurrió un error al escribir en el archivo:", error)
        finally:
            try:
                archivo.close()
                continuar = input("¿Continuar? ")
            except FileNotFoundError as error:
                pass

        carrito(num_carrito)
           

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

def leer_clientes():
    try:
        registros = []
        archivo = open("clientes.txt", "r")
        for linea in archivo:
            palabra = linea.split(",")
            registros.append(palabra)
        return registros
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
        with open(archivo, "r",encoding="UTF-8") as archivo:
            for line in archivo:
                list_id.append(int(line.split(",")[0]))
            if len(list_id) != 0:
                maximo = max(list_id) + 1
                return maximo
            else: 
                return "1"
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
    
    
def validar_nombre_cliente():
    while True:
        nombre = input("Ingrese nombre de cliente: ").capitalize()
        
        if nombre.isalpha():

            return nombre
        else:
            print("El nombre debe contener solo letras. Inténtelo nuevamente.")


def validar_apellido_cliente():
    while True:
        apellido = input("Ingrese apellido de cliente: ").capitalize()
        
        if apellido.isalpha():

            return apellido
        else:
            print("El apellido debe contener solo letras. Inténtelo nuevamente.")


def validar_nombre_proveedores():
    while True:
        nombre = input("Ingrese nombre de proveedor: ").capitalize()
        
        if nombre.isalpha():

            return nombre
        else:
            print("El nombre debe contener solo letras. Inténtelo nuevamente.")

def validar_apellido_proveedores():
    while True:
        apellido = input("Ingrese apellido de proveedor: ").capitalize()
        
        if apellido.isalpha():

            return apellido
        else:
            print("El apellido debe contener solo letras. Inténtelo nuevamente.")


def ing_cliente():
    continuar = "S"

    while continuar == "S":
        id_cliente = buscar_max("clientes.txt")
        nombre_cliente = validar_nombre_cliente()
        apellido_cliente = validar_apellido_cliente()
        dni = validar_dni()
        cuit = validar_CUIT()
        dni_existe = False

        cliente = {
            "ID": id_cliente,
            "Nombre": nombre_cliente,
            "Apellido": apellido_cliente,
            "DNI": dni,
            "CUIT": cuit,
            "Creado": timestamp(),
            "Modificado": timestamp(),
            "isactive": True
        }

        try:
            with open("clientes.txt", "r") as archivo:
                for linea in archivo:
                    campo = linea.split(",")
                    if campo[3] == dni:
                        print(f'Ya existe un cliente con el DNI "{campo[3]}".')
                        dni_existe = True
        except FileNotFoundError:
            print("No existe el archivo")
        except IOError as e:
            print(f"Error de entrada/salida: {e}")

        data_cliente = f"{cliente['ID']},{cliente['Nombre']},{cliente['Apellido']},{cliente['DNI']},{cliente['CUIT']},{cliente['Creado']},{cliente['Modificado']},{cliente['isactive']}\n"

        try:
            if not dni_existe:
                with open("clientes.txt", "a") as archivo:
                    archivo.write(data_cliente)
                    print("Registro guardado")
        except IOError as e:
            print(f"Ocurrió un error al escribir en el archivo: {e}")

        if continuar == "S":
            continuar = input("¿Agregar otro registro (S/N)?: ").upper()


def ing_proveedor():
  nombre_proveedor = input("Ingrese nombre de proveedor: ") #Agregar proveedor a proveedores.txt
  pass

def ing_prod_valor():
    _, productos = leer_productos()
    print(tabulador(productos, COLUMNAS_PRODUCTOS))

    id_modificar = int(input("Ingrese ID de producto a modificar: "))

    with open("productos.txt", "r+", encoding="UTF-8") as archivo:
        encontrado = False
        while not encontrado:
            pos_actual = archivo.tell()
            linea = archivo.readline()
            
            if not linea:
                print(f"No se encontró un producto con el ID {id_modificar}.")
                break

            campos = linea.strip().split(",")
            id_actual = campos[0]

            if str(id_modificar) == id_actual:
                encontrado = True
                print(f"El artículo se encuentra en la línea {pos_actual}.")
                print(f"Contenido de la línea: {linea}")
                nuevo_valor = float(input(f"Ingrese el nuevo valor para el campo precio. Precio actual: {campos[5]}: "))
                campos[5] = str(nuevo_valor)
                archivo.seek(pos_actual)
                archivo.write(",".join(campos))

                print("Campo modificado exitosamente.")

def ing_prod_cant():
  id = buscar_max("productos.txt")
  nombre = input("Ingrese nombre del producto: ").upper()
  rubro = input("Ingrese rubro: ").upper()
  marca = input("Ingrese marca: ")
  proveedor = input("Ingrese proveedor: ")
  precio = float(input("Ingrese precio: "))
  cantidad = int(input("Ingrese cantidad: "))

  data_productos = f'{id},"{nombre}","{rubro}","{marca}",{proveedor},{precio},{cantidad}\n'

  try:
      with open("productos.txt", "a") as archivo:
          archivo.write(data_productos)
      print("Registro guardado")
  except Exception as error:
      print("Ocurrió un error al escribir en el archivo:", error)

def leer_productos():
    productos = []
    categorias = []
    try:
        archivo = open("productos.txt", "r", encoding="UTF-8")
        for registro in archivo:
            palabra = registro.split(",")
            productos.append(palabra)
            if not palabra[2] in categorias:
                categorias.append(palabra[2])
        
        
    except FileNotFoundError as error:
        print (error)
    finally:
        return categorias, productos
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
        ing_prod_cant()

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
        clientes = leer_clientes()
        print(tabulador(clientes, COLUMNAS_CLIENTES))
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
        clientes = leer_clientes()
        print(tabulador(clientes, COLUMNAS_CLIENTES))
    elif choice == 2:
        _, productos = leer_productos()
        print(tabulador(productos, COLUMNAS_PRODUCTOS))

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
            print(leer_clientes())
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
