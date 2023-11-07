from tabulate import tabulate
import archivos


def filtrar(categoria):
    def filtro(categoria, linea):
        return categoria in linea

    tabla = []
    try:
        with open("productos.txt", "r", encoding="UTF-8") as archivo:
            filtradas = filter(lambda linea: filtro(categoria, linea), archivo)
            for linea in filtradas:
                productos = linea.split(",")
                tabla.append(productos)
        return tabla

    except FileNotFoundError as error:
        print(error)
    finally:
        try: 
            archivo.close()
        except NameError:
            pass 
            

def listar(): 
    archivos.listar('productos.txt')

def listar_categorias(): 
    lista = archivos.listar('productos.txt', [2])
    elset= set(lista)
    print(elset)


listar_categorias()