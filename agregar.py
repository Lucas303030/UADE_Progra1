# Nombre del archivo CSV
archivo_csv = "productos.txt"

from random import randint

# Valor adicional que deseas agregar al final de cada línea
valor_adicional = randint(1,200)

# Lista para almacenar las líneas modificadas
lineas_modificadas = []

# Leer el archivo CSV
try:
    with open(archivo_csv, "r", encoding="UTF-8") as archivo:
        lineas = archivo.readlines()

        for linea in lineas:
            # Agregar el valor adicional al final de cada línea
            linea_modificada = f"{linea.strip()},{valor_adicional}\n"
            lineas_modificadas.append(linea_modificada)
except FileNotFoundError:
    print(f"No se encontró el archivo {archivo_csv}")

# Escribir de nuevo al archivo CSV
try:
    with open(archivo_csv, "w", encoding="UTF-8") as archivo:
        archivo.writelines(lineas_modificadas)
except IOError as e:
    print(f"Error de entrada/salida al escribir en el archivo: {e}")
