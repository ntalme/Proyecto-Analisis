#LIBRERIA PARA RUTAS DE ARCHIVOS
import os
#LIBRERIA IFC
import ifcopenshell
#LIBRERIA PARA COPIAR ARCHIVOS
import shutil

#Funcion para abrir el archivo
def abrir_archivo_ifc(ruta_archivo):
    try:
        #Abrir archivo
        archivo_ifc = ifcopenshell.open(ruta_archivo)

        print("Archivo IFC abierto correctamente.")
        return archivo_ifc
    
    #Si es que hay algun error
    except Exception as e:
        print("Error al abrir el archivo IFC:", e)
        return None

#Funcion para mostrar las primeras lineas
def mostrar_primeras_lineas(ruta_archivo, num_lineas=5):
    try:
        #Leer las lineas
        with open(ruta_archivo, 'r') as file:
            for i in range(num_lineas):
                print(file.readline().strip())

    #Si es que hay algun error
    except Exception as e:
        print("Error al mostrar las primeras líneas del archivo:", e)

#Funcion para generar los achivos de copia
def generar_copias_ifc(ruta_archivo_original, cantidad_copias, carpeta_destino):
    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        #Generar las copias segun lo pedido por el usuario
        for i in range(1, cantidad_copias + 1):
            nombre_archivo_copia = f"prueba{i}.ifc"
            ruta_archivo_copia = os.path.join(carpeta_destino, nombre_archivo_copia)
            shutil.copyfile(ruta_archivo_original, ruta_archivo_copia)

            print(f"Copia {i} del archivo IFC creada correctamente como:", ruta_archivo_copia)

    #Si es que hay algun error
    except Exception as e:
        print("Error al generar las copias del archivo IFC:", e)

#Funcion main
if __name__ == "__main__":
    
    #Pedir al usuario la ruta
    ruta_archivo_ifc = input("Por favor, ingresa la ruta del archivo IFC: ").strip('"')

    archivo_ifc = abrir_archivo_ifc(ruta_archivo_ifc)
    mostrar_primeras_lineas(ruta_archivo_ifc)

    if archivo_ifc:
        #Mostrar la cantidad de elementos
        cantidad_elementos = len(archivo_ifc.by_type("IfcProduct"))
        print("Cantidad de elementos en el archivo IFC:", cantidad_elementos)

        #Preguntar la cantidad de copias
        cantidad_copias = int(input("Ingrese la cantidad de copias que desea hacer: "))

        #Generar una carpeta en el escritorio llamada Copias_IFC
        carpeta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Copias_IFC")
        generar_copias_ifc(ruta_archivo_ifc, cantidad_copias, carpeta_destino)