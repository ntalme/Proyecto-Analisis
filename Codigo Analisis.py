#LIBRERIA PARA RUTAS DE ARCHIVOS
import os
#LIBRERIA IFC
import ifcopenshell
#LIBRERIA PARA EXPRESIONES REGULARES
import re
#LIBRERIA PARA GENERAR NUMEROS ALEATORIOS
import random
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

#Funcion para cambiar el valor de temperatura
def cambiar_valor_temperatura(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de temperatura está presente en el archivo IFC
        if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de temperatura
            archivo_texto_modificado = re.sub(r'IFCTHERMODYNAMICTEMPERATUREMEASURE\((\d+\.)\)', f'IFCTHERMODYNAMICTEMPERATUREMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_texto_modificado)
        else:
            print("El parámetro de temperatura no está presente en el archivo IFC. No se realizaron cambios.")

    except Exception as e:
        print("Error al cambiar el valor de temperatura:", e)

def cambiar_valor_humedad(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de humedad está presente en el archivo IFC
        if "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de humedad
            archivo_texto_modificado = re.sub(r'IFCPOSITIVERATIOMEASURE\((\d+\.)\)', f'IFCPOSITIVERATIOMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_texto_modificado)
        else:
            print("El sensor de humedad no está presente en el archivo IFC. No se realizaron cambios.")

    except Exception as e:
        print("Error al cambiar el valor de humedad:", e)

#Funcion main
if __name__ == "__main__":
    
    #Pedir al usuario la ruta
    ruta_archivo_ifc = input("Por favor, ingresa la ruta del archivo IFC: ").strip('"')

    archivo_ifc = abrir_archivo_ifc(ruta_archivo_ifc)

    if archivo_ifc:
        # Leer el archivo IFC una vez
        with open(ruta_archivo_ifc, 'r') as file:
            archivo_texto = file.read()

        #Preguntar la cantidad de documentos con valores de temperatura y humedad diferentes que se quieren crear
        cantidad_documentos = int(input("Ingrese la cantidad de documentos con valores de temperatura y humedad diferentes que desea crear: "))
        
        #Directorio para guardar los documentos
        carpeta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Simulaciones IFC")
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        #Generar los documentos con valores de temperatura y humedad diferentes
        for i in range(1, cantidad_documentos + 1):
            # Generar valores aleatorios entre 0 y 100 para la temperatura y la humedad
            nuevo_valor_temperatura = random.randint(0, 100) # Valor entero entre 0 y 100
            nuevo_valor_humedad = random.randint(0, 100) # Valor entero entre 0 y 100
            
            # Crear una copia del archivo IFC
            nombre_archivo_original = os.path.basename(ruta_archivo_ifc)
            
            #Nombre del archivo
            if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}_H{nuevo_valor_humedad}.ifc"
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}.ifc"
            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_H{nuevo_valor_humedad}.ifc"
            else:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{i}.ifc"
                
            ruta_archivo_copia = os.path.join(carpeta_destino, nombre_archivo_copia)
            shutil.copyfile(ruta_archivo_ifc, ruta_archivo_copia)
        
            # Verificar si el parámetro de humedad está presente en el archivo IFC
            if  "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
            
                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
                
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius y un valor de humedad de {nuevo_valor_humedad}%:", ruta_archivo_copia)
            
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
    
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius. El parámetro de humedad no está presente en el archivo IFC:", ruta_archivo_copia)

            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:

                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
                
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_humedad} grados Celsius. El parámetro de humedad no está presente en el archivo IFC:", ruta_archivo_copia)
