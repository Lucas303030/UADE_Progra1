import random

# FUNCIONES:

# 1) Función para agregar stock al archivo "STOCK.TXT":

def stock_y_precios(archivo="STOCK.TXT"):

    try:

        # Verifica si el archivo está vacío (no contiene ningún carácter).

        with open(archivo, "r") as f:

            primer_caracter = f.read(1)

        # Si el archivo está vacío, agrega encabezados.
        if not primer_caracter:

            with open(archivo, "a") as f:

                f.write("ID_producto\tNombre_producto\tDescripcion_producto\tClase_producto\tMarca_producto\tPrecio_producto\tStock_producto\n")


        continuar = True

        while continuar:

            # Solicito información de los productos.

            ID_producto = random.randint(1, 99)

            Nombre_producto = input("Ingrese el nombre del PRODUCTO: ").ljust(16)

            Descripcion_producto = input("Ingrese la descripcion del PRODUCTO: ").ljust(18)

            Clase_producto = input("Ingrese la clase del PRODUCTO: ")

            Marca_producto = input("Ingrese la marca del PRODUCTO: ")

            Precio_producto = input("Ingrese el precio del PRODUCTO: ")

            Stock_producto = input("Ingrese el stock del PRODUCTO: ")

            # Agrega la información al archivo "STOCK.TXT" utilizando un formato fijo.
            with open(archivo, "a") as f:

                f.write(f"{ID_producto:<12}\t{Nombre_producto:<16}\t{Descripcion_producto:<18}\t{Clase_producto:<16}\t{Marca_producto:<16}\t{Precio_producto:<12}\t{Stock_producto}\n")


            print("REGISTRO GUARDADO")


            # Pregunto si quieres continuar cargando productos al archivo "STOCK.TXT".

            respuesta = input("¿Desea ingresar otro PRODUCTO? (S/N): ")

            continuar = respuesta.lower() == 's'

    except Exception as error:
        
        print("ERROR AL GUARDAR EL REGISTRO:", error)

stock_y_precios()