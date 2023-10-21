import random

# FUNCIONES:
# 1) Función para agregar clientes al archivo "CLIENTES.TXT":
def clientes(archivo="CLIENTES.TXT"):
    try:
        # Verifica si el archivo está vacío (no contiene ningún carácter).
        with open(archivo, "r") as f:
            primer_caracter = f.read(1)

        # Si el archivo está vacío, agrega encabezados.
        if not primer_caracter:
            with open(archivo, "a") as f:
                f.write("ID_cliente\tNombre_cliente\tApellido_cliente\tDNI_cliente\n\n")

        continuar = True
        while continuar:
            # Solicito información de los clientes.
            nombre_cliente = input("Ingrese el nombre del CLIENTE: ")
            print()
            apellido_cliente = input("Ingrese el apellido del CLIENTE: ")
            print()
            DNI_cliente = input("Ingrese el DNI del CLIENTE: ")
            ID_cliente = random.randint(1,99)

            # Agrega la información a archivo "CLIENTES.TXT"
            with open(archivo, "a") as f:
                f.write(f"{ID_cliente: <12}\t{nombre_cliente: <16}\t{apellido_cliente: <18}\t{DNI_cliente}\n")
            print()
            print("REGISTRO GUARDADO")

            # Pregunto si quiero continuar cargando clientes al archivo "CLIENTES.TXT"
            respuesta = input("¿Desea ingresar otro CLIENTE? (S/N): ")
            continuar = respuesta.lower() == 's'

    except Exception as error:
        print("ERROR AL GUARDAR EL REGISTRO:", error)

#2)Función para agregar proveedores al archivo "PROVEEDORES.TXT":
def proveedores(archivo="PROVEEDORES.TXT"):
    try:
        # Verifica si el archivo está vacío (no contiene ningún carácter).
        with open(archivo, "r") as f:
            primer_caracter = f.read(1)

        # Si el archivo está vacío, agrega encabezados.
        if not primer_caracter:
            with open(archivo, "a") as f:
                f.write("ID_proveedor\tProveedor\tCUIT/Dirección\tTelefono\n\n")

        continuar = True
        while continuar:
            # Solicito información de los proveeodres.
            proveedor = input("Ingrese el nombre del PROVEEDOR: ")
            print()
            CUIT = input("Ingrese el nro de CUIT, Ejemplo:20-8 digitos: ")
            print()
            dire= input("Ingrese la dirección: ")
            telefono=int(input("Ingrese el número de telefono:"))
            ID_proveedor = random.randint(100, 999)

            # Agrega la información a archivo "PROVEEDORES.TXT"
            with open(archivo, "a") as f:
                f.write(f"{ID_proveedor: <12}\t{proveedor: <16}\t{CUIT: <18}\t{dire}\t{telefono}\n")
            print()
            print("REGISTRO GUARDADO")

            # Pregunto si quiero continuar cargando proveedores al archivo "PROVEEDORES.TXT".
            respuesta = input("¿Desea ingresar otro PROVEEDOR? (S/N): ")
            continuar = respuesta.lower() == 's'

    except Exception as error:
        print("ERROR AL GUARDAR EL REGISTRO:", error)




# Llamada a la función
clientes()
proveedores()
