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

#FUNCION PARA CAMBIAR EL VALOR DE LA TEMPERATURA
def cambiar_valor_temperatura(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de temperatura está presente en el archivo IFC
        if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de temperatura
            archivo_modificado = re.sub(r'IFCTHERMODYNAMICTEMPERATUREMEASURE\((\d+\.)\)', f'IFCTHERMODYNAMICTEMPERATUREMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_modificado)
        else:
            print("El parámetro de temperatura no está presente en el archivo IFC. No se realizaron cambios.")

    except Exception as e:
        print("Error al cambiar el valor de temperatura:", e)

#FUNCION PARA CAMBIAR EL VALOR DE LA HUMEDAD
def cambiar_valor_humedad(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de humedad está presente en el archivo IFC
        if "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de humedad
            archivo_modificado  = re.sub(r'IFCPOSITIVERATIOMEASURE\((\d+\.)\)', f'IFCPOSITIVERATIOMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_modificado)
        else:
            print("El sensor de humedad no está presente en el archivo IFC. No se realizaron cambios.")

    except Exception as e:
        print("Error al cambiar el valor de humedad:", e)

#FUNCION PARA CAMBIAR EL VALOR DE LA LUZ
def cambiar_valor_luz(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de luz está presente en el archivo IFC
        if "IFCILLUMINANCEMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de luz
            archivo_modificado = re.sub(r'IFCILLUMINANCEMEASURE\((\d+\.)\)', f'IFCILLUMINANCEMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_modificado)
        else:
            print("El parámetro de luz no está presente en el archivo IFC. No se realizaron cambios.")

    except Exception as e:
        print("Error al cambiar el valor de luz:", e)

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
        cantidad_documentos = int(input("Ingrese la cantidad de documentos con valores de sensores aleatorios: "))
        
        #Directorio para guardar los documentos
        carpeta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Simulaciones IFC")
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        #Generar los documentos con valores de temperatura, humedad y luz diferentes
        for i in range(1, cantidad_documentos + 1):
            # Generar valores aleatorios entre 0 y 100 para la temperatura, humedad y luz
            nuevo_valor_temperatura = random.randint(0, 100)
            nuevo_valor_humedad = random.randint(0, 100) 
            nuevo_valor_luz = random.randint(0, 100) 
            
            # Crear una copia del archivo IFC
            nombre_archivo_original = os.path.basename(ruta_archivo_ifc)
            
            #NOMBRES DEL ARCHIVO
            #Estan los sensores de temperatura, humedad y luz
            if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}_H{nuevo_valor_humedad}_L{nuevo_valor_luz}.ifc"

            #Estan solo los sensores de temperatura y humedad 
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}_H{nuevo_valor_humedad}.ifc"

            #Estan solo los sensores de temperatura y luz
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}_L{nuevo_valor_luz}.ifc"

            #Estan solo los sensores humedad y luz
            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_H{nuevo_valor_humedad}_L{nuevo_valor_luz}.ifc"

            #Esta solo el sensor de temperatura
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_T{nuevo_valor_temperatura}.ifc"

            #Esta solo el sensor de humedad 
            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_H{nuevo_valor_humedad}.ifc"

            #Esta solo el sensor de luz
            elif "IFCILLUMINANCEMEASURE" in archivo_texto:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_L{nuevo_valor_luz}.ifc"

            #No hay nada   
            else:
                nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{i}.ifc"
                
            ruta_archivo_copia = os.path.join(carpeta_destino, nombre_archivo_copia)
            shutil.copyfile(ruta_archivo_ifc, ruta_archivo_copia)
        
            #VERIFICAR LOS PARAMETROS 
            #Estan los sensores de temperatura, humedad y luz
            if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
            
                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
                
                # Cambiar el valor de luz en el nuevo archivo IFC
                cambiar_valor_luz(ruta_archivo_copia, nuevo_valor_luz)
                
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius, un valor de humedad de {nuevo_valor_humedad}% y un valor de luz de {nuevo_valor_luz}:", ruta_archivo_copia)
            
            #Estan solo los sensores de temperatura y humedad 
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
    
                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
                
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius, un valor de humedad de {nuevo_valor_humedad}%. El parámetro de luz no está presente en el archivo IFC:", ruta_archivo_copia)

            #Estan solo los sensores de temperatura y luz
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
    
                # Cambiar el valor de luz en el nuevo archivo IFC
                cambiar_valor_luz(ruta_archivo_copia, nuevo_valor_luz)
                
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius y un valor de luz de {nuevo_valor_luz}. El parámetro de humedad no está presente en el archivo IFC:", ruta_archivo_copia)
            
             #Estan solo los sensores de humedad y luz
            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:

                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
    
                # Cambiar el valor de luz en el nuevo archivo IFC
                cambiar_valor_luz(ruta_archivo_copia, nuevo_valor_luz)
                
                print(f"Documento {i} creado correctamente con un valor de humedad de {nuevo_valor_humedad}% y un valor de luz de {nuevo_valor_luz}. El parámetro de temperatura no está presente en el archivo IFC:", ruta_archivo_copia)
            
            #Esta solo el sensor de temperatura
            elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:

                # Cambiar el valor de temperatura en el nuevo archivo IFC
                cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
    
                print(f"Documento {i} creado correctamente con un valor de temperatura de {nuevo_valor_temperatura} grados Celsius. Los parámetros de humedad y luz no están presentes en el archivo IFC:", ruta_archivo_copia)

            #Esta solo el sensor de humedad
            elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:

                # Cambiar el valor de humedad en el nuevo archivo IFC
                cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
    
                print(f"Documento {i} creado correctamente con un valor de humedad de {nuevo_valor_humedad}%. Los parámetros de temperatura y luz no están presentes en el archivo IFC:", ruta_archivo_copia)

            #Esta solo el sensor de luz   
            elif "IFCILLUMINANCEMEASURE" in archivo_texto:

                # Cambiar el valor de luz en el nuevo archivo IFC
                cambiar_valor_luz(ruta_archivo_copia, nuevo_valor_luz)
    
                print(f"Documento {i} creado correctamente con un valor de luz de {nuevo_valor_luz}. Los parámetros de temperatura y humedad no están presentes en el archivo IFC:", ruta_archivo_copia)

            #No hay sensores
            else:
                print(f"Documento {i} creado correctamente como no se encontro ningun sensor el documento queda sin ningun cambio:", ruta_archivo_copia)