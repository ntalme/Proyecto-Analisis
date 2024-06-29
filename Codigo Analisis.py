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
#LIBRERIA PARA CREAR PESTAÑAS INTERACTIVAS
import tkinter as tk
#IMPORTACIONES DE TKINTER
from tkinter import filedialog, messagebox, ttk

# Función para abrir el archivo
def abrir_archivo_ifc(ruta_archivo):
    try:
        # Abrir archivo
        archivo_ifc = ifcopenshell.open(ruta_archivo)
        print("Archivo IFC abierto correctamente.")
        return archivo_ifc
    except Exception as e:
        print("Error al abrir el archivo IFC:", e)
        return None

# Función para obtener el rango de temperatura según la zona y la estación
# Datos sacado de weatherspark.com
def obtener_rango_temperatura(zona, estacion):
    #ZONA NORTE
    #TOMANDO LOS DATOS EN CALAMA
    if zona == "Zona Norte":
        if estacion == "Invierno":
            return (2, 22)
        elif estacion == "Otoño":
            return (3, 24)
        elif estacion == "Primavera":
            return (4, 24)
        elif estacion == "Verano":
            return (7, 24)
    #ZONA CENTRAL
    #TOMANDO LOS DATOS EN SANTIAGO
    elif zona == "Zona Central":
        if estacion == "Invierno":
            return (3, 18)
        elif estacion == "Otoño":
            return (5, 27)
        elif estacion == "Primavera":
            return (5, 28)
        elif estacion == "Verano":
            return (12, 31)
    #ZONA SUR
    #TOMANDO LOS DATOS DE CONCEPCION
    elif zona == "Zona Sur":
        if estacion == "Invierno":
            return (6, 14)
        elif estacion == "Otoño":
            return (7, 22)
        elif estacion == "Primavera":
            return (6, 20)
        elif estacion == "Verano":
            return (11, 23)
    #ZONA AUSTRAL
    elif zona == "Zona Austral":
        if estacion == "Invierno":
            return (3, 11)
        elif estacion == "Otoño":
            return (3, 18)
        elif estacion == "Primavera":
            return (4, 16)
        elif estacion == "Verano":
            return (10, 18)
    return None

# Función para calcular la cantidad de luz solar
# Datos sacado de Revista Stratus
def calcular_luz_solar(zona, estacion):
    luz_solar = 0
    #ZONA NORTE
    if zona == "Zona Norte":
        #ESTACIONES
        if estacion == "Invierno":
                luz_solar = (4500, 6500) 

        elif estacion == "Otoño":
                luz_solar = (4500, 6500) 

        elif estacion == "Primavera":
                luz_solar = (5500, 7000)

        elif estacion == "Verano":
                luz_solar = (5500, 6500)

    #ZONA CENTRAL
    elif zona == "Zona Central":
        #ESTACIONES
        if estacion == "Invierno":
                luz_solar = (2000, 4000) 

        elif estacion == "Otoño":
                luz_solar = (2000, 5500) 

        elif estacion == "Primavera":
                luz_solar = (4000, 7000)

        elif estacion == "Verano":
                luz_solar = (5500, 7000)

    #ZONA SUR
    elif zona == "Zona Sur":
        #ESTACIONES
        if estacion == "Invierno":
                luz_solar = (3000, 4000) 
               
        elif estacion == "Otoño":
                luz_solar = (3000, 5000) 

        elif estacion == "Primavera":
                luz_solar = (4000, 6500)

        elif estacion == "Verano":
                luz_solar = (5000, 6500)

    #ZONA AUSTRAL
    elif zona == "Zona Austral":
        #ESTACIONES
        if estacion == "Invierno":
                luz_solar = (1000, 2500) 

        elif estacion == "Otoño":
                luz_solar = (1000, 2000) 

        elif estacion == "Primavera":
                luz_solar = (2500,3500)

        elif estacion == "Verano":
                luz_solar = (2000, 3500)
    return luz_solar

# Función para obtener el rango de humedad base
# Formula sacada de National Weather Service
def calcular_presion_vapor_saturado(temperatura):
    return 6.11 * 10**(7.5 * temperatura / (237.3 + temperatura))

def calcular_humedad_relativa(temperatura, temperatura_rocio, numero_personas):
    es = calcular_presion_vapor_saturado(temperatura)
    e = calcular_presion_vapor_saturado(temperatura_rocio)
    
    # Ajustar la humedad absoluta (presión de vapor real) por la cantidad de personas
    e += 0.3 * numero_personas
    
    return (e / es) * 100

# FUNCION PARA CAMBIAR EL VALOR DE LA TEMPERATURA
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
    #ERROR
    except Exception as e:
        print("Error al cambiar el valor de temperatura:", e)

# FUNCION PARA CAMBIAR EL VALOR DE LA HUMEDAD
def cambiar_valor_humedad(ruta_archivo, nuevo_valor):
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        # Verificar si el sensor de humedad está presente en el archivo IFC
        if "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            # Buscar y reemplazar el valor de humedad
            archivo_modificado = re.sub(r'IFCPOSITIVERATIOMEASURE\((\d+\.)\)', f'IFCPOSITIVERATIOMEASURE({nuevo_valor}.)', archivo_texto)

            # Escribir el archivo modificado
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_modificado)
        else:
            print("El sensor de humedad no está presente en el archivo IFC. No se realizaron cambios.")
    #ERROR
    except Exception as e:
        print("Error al cambiar el valor de humedad:", e)

# FUNCION PARA CAMBIAR EL VALOR DE LA LUZ
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
    #ERROR
    except Exception as e:
        print("Error al cambiar el valor de luz:", e)

# Función para manejar la creación de archivos
def crear_archivos():
    ruta_archivo_ifc = entry_ruta.get()
    archivo_ifc = abrir_archivo_ifc(ruta_archivo_ifc)

    if archivo_ifc:

        # Leer el archivo IFC una vez
        with open(ruta_archivo_ifc, 'r') as file:
            archivo_texto = file.read()

        #TEMPERATURA, HUMEDAD Y LUZ
        if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de TEMPERATURA y LUZ
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Temperatura y la Luz:")
            label_condiciones_temperatura.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            label_zona = tk.Label(ventana_parametros, text="Zona:")
            label_zona.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona.set("Zona Norte")
            combo_zona.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion = tk.Label(ventana_parametros, text="Estación:")
            label_estacion.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion.set("Invierno")
            combo_estacion.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Parámetros de HUMEDAD
            label_condiciones_humedad = tk.Label(ventana_parametros, text="Condiciones para la Humedad:")
            label_condiciones_humedad.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            label_personas = tk.Label(ventana_parametros, text="Número de personas:")
            label_personas.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            entry_personas = tk.Entry(ventana_parametros)
            entry_personas.grid(row=4, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona.get(), combo_estacion.get(), entry_personas.get()))
            button_generar.grid(row=7, column=0, columnspan=2, pady=10)
            
        #TEMPERATURA Y HUMEDAD
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:

            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de TEMPERATURA
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Temperatura:")
            label_condiciones_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_zona_temp = tk.Label(ventana_parametros, text="Zona:")
            label_zona_temp.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona_temp = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona_temp.set("Zona Norte")
            combo_zona_temp.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion_temp = tk.Label(ventana_parametros, text="Estación:")
            label_estacion_temp.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion_temp = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion_temp.set("Invierno")
            combo_estacion_temp.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Parámetros de HUMEDAD
            label_condiciones_humedad = tk.Label(ventana_parametros, text="Condiciones para la Humedad:")
            label_condiciones_humedad.grid(row=3, column=0, padx=5, pady=5, sticky="w")

            label_personas_humedad = tk.Label(ventana_parametros, text="Número de personas:")
            label_personas_humedad.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            entry_personas_humedad = tk.Entry(ventana_parametros)
            entry_personas_humedad.grid(row=4, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar_temp_hum = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona_temp.get(), combo_estacion_temp.get(), entry_personas_humedad.get()))
            button_generar_temp_hum.grid(row=5, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()

        #TEMPERATURA Y LUZ
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:

            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de TEMPERATURA y LUZ
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Temperatura y la Luz:")
            label_condiciones_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_zona_temp_luz = tk.Label(ventana_parametros, text="Zona:")
            label_zona_temp_luz.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona_temp_luz = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona_temp_luz.set("Zona Norte")
            combo_zona_temp_luz.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion_temp_luz = tk.Label(ventana_parametros, text="Estación:")
            label_estacion_temp_luz.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion_temp_luz = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion_temp_luz.set("Invierno")
            combo_estacion_temp_luz.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar_temp_luz = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona_temp_luz.get(), combo_estacion_temp_luz.get()))
            button_generar_temp_luz.grid(row=5, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()

        #HUMEDAD Y LUZ
        elif "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:

            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de  Luz
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Luz:")
            label_condiciones_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_zona_temp = tk.Label(ventana_parametros, text="Zona:")
            label_zona_temp.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona_temp = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona_temp.set("Zona Norte")
            combo_zona_temp.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion_temp = tk.Label(ventana_parametros, text="Estación:")
            label_estacion_temp.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion_temp = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion_temp.set("Invierno")
            combo_estacion_temp.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Parámetros de HUMEDAD
            label_condiciones_humedad = tk.Label(ventana_parametros, text="Condiciones para la Humedad:")
            label_condiciones_humedad.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_personas_humedad_luz = tk.Label(ventana_parametros, text="Número de personas:")
            label_personas_humedad_luz.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            entry_personas_humedad_luz = tk.Entry(ventana_parametros)
            entry_personas_humedad_luz.grid(row=1, column=1, padx=5, pady=5, sticky="we")


            # Botón para generar archivos
            button_generar_humedad_luz = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, entry_personas_humedad_luz.get(), combo_zona_temp_luz.get(), combo_estacion_temp_luz.get()))
            button_generar_humedad_luz.grid(row=4, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()

        #TEMPERATURA
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de TEMPERATURA
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Temperatura:")
            label_condiciones_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_zona_temp = tk.Label(ventana_parametros, text="Zona:")
            label_zona_temp.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona_temp = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona_temp.set("Zona Norte")
            combo_zona_temp.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion_temp = tk.Label(ventana_parametros, text="Estación:")
            label_estacion_temp.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion_temp = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion_temp.set("Invierno")
            combo_estacion_temp.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar_temp = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona_temp.get(), combo_estacion_temp.get()))
            button_generar_temp.grid(row=4, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()

        #HUMEDAD
        elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            # Parámetros de HUMEDAD
            label_condiciones_humedad = tk.Label(ventana_parametros, text="Condiciones para la Humedad:")
            label_condiciones_humedad.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_personas_humedad = tk.Label(ventana_parametros, text="Número de personas:")
            label_personas_humedad.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            entry_personas_humedad = tk.Entry(ventana_parametros)
            entry_personas_humedad.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar_humedad = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, entry_personas_humedad.get()))
            button_generar_humedad.grid(row=4, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()

        #LUZ
        elif "IFCILLUMINANCEMEASURE" in archivo_texto:  
            # Crear una nueva ventana para solicitar todos los parámetros
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

           # Parámetros de LUZ
            label_condiciones_temperatura = tk.Label(ventana_parametros, text="Condiciones para la Luz:")
            label_condiciones_temperatura.grid(row=0, column=0, padx=5, pady=5, sticky="w")

            label_zona_temp = tk.Label(ventana_parametros, text="Zona:")
            label_zona_temp.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_zona_temp = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona_temp.set("Zona Norte")
            combo_zona_temp.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_estacion_temp = tk.Label(ventana_parametros, text="Estación:")
            label_estacion_temp.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            combo_estacion_temp = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion_temp.set("Invierno")
            combo_estacion_temp.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            # Botón para generar archivos
            button_generar_luz = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona_temp_luz.get(), combo_estacion_temp_luz.get()))
            button_generar_luz.grid(row=4, column=0, columnspan=2, pady=10)

            # Cerrar la ventana principal
            root.withdraw()
            
        else:
            messagebox.showwarning("Advertencia", "El archivo IFC no contiene parámetros de temperatura.")

# Función para generar archivos con valores de temperatura, humedad y luz diferentes
def generar_archivos(ruta_archivo, zona, estacion, personas=""):

    cantidad_documentos = int(entry_cantidad.get())
    archivo_texto = ""

    with open(ruta_archivo, 'r') as file:
        archivo_texto = file.read()

    # Directorio para guardar los documentos
    carpeta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Simulaciones IFC")
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    documentos_creados = []

   # Generar temperatura de rocío aleatoria en un rango entre 10°C y 20°C
    temperatura_rocio_celsius = random.uniform(10, 20)

    # Inicializar nuevo_valor_luz como None
    nuevo_valor_luz = None

   # Generar los documentos con valores de temperatura, humedad y luz diferentes
    for i in range(1, cantidad_documentos + 1):
        if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
            # Generar valores aleatorios entre los rangos de temperatura según la zona y la estación
            rango_temperatura = obtener_rango_temperatura(zona, estacion)
            nuevo_valor_temperatura = round(random.uniform(rango_temperatura[0], rango_temperatura[1]))

        if "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            # Calcular la humedad relativa
            humedad_relativa  = calcular_humedad_relativa(nuevo_valor_temperatura, temperatura_rocio_celsius, int(personas))

            nuevo_valor_humedad = round(humedad_relativa)
            
        if "IFCILLUMINANCEMEASURE" in archivo_texto:
            # Calcular la cantidad de luz solar
            rango_luz = calcular_luz_solar(zona, estacion)
            nuevo_valor_luz = round(random.uniform(rango_luz[0], rango_luz[1]))

        # Crear una copia del archivo IFC
        nombre_archivo_original = os.path.basename(ruta_archivo)

        # Nombres del archivo
        #TEMPERATURA, HUMEDAD Y LUZ
        if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_T{nuevo_valor_temperatura}_H{nuevo_valor_humedad}_L{nuevo_valor_luz}.ifc"

        #TEMPERATURA Y HUMEDAD
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_T{nuevo_valor_temperatura}_H{nuevo_valor_humedad}.ifc"

        #TEMPERATURA Y LUZ
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_T{nuevo_valor_temperatura}_L{nuevo_valor_luz}.ifc"

        #HUMEDAD Y LUZ
        elif "IFCPOSITIVERATIOMEASURE" in archivo_texto and "IFCILLUMINANCEMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_H{nuevo_valor_humedad}_L{nuevo_valor_luz}.ifc"
        
        #TEMPERATURA
        elif "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_T{nuevo_valor_temperatura}.ifc"
        
        #HUMEDAD
        elif "IFCPOSITIVERATIOMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_H{nuevo_valor_humedad}.ifc"

        #LUZ
        elif "IFCILLUMINANCEMEASURE" in archivo_texto:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{zona}_{estacion}_L{nuevo_valor_luz}.ifc"

        #NINGUNO
        else:
            nombre_archivo_copia = f"{os.path.splitext(nombre_archivo_original)[0]}_{i}.ifc"

        # Crear una copia del archivo IFC
        ruta_archivo_copia = os.path.join(carpeta_destino, nombre_archivo_copia)
        shutil.copyfile(ruta_archivo, ruta_archivo_copia)

        # Cambiar los valores en el nuevo archivo IFC
        cambiar_valor_temperatura(ruta_archivo_copia, nuevo_valor_temperatura)
        cambiar_valor_humedad(ruta_archivo_copia, nuevo_valor_humedad)
        if nuevo_valor_luz is not None:  # Asegurar que nuevo_valor_luz tenga un valor antes de intentar usarlo
            cambiar_valor_luz(ruta_archivo_copia, nuevo_valor_luz)

        documentos_creados.append(nombre_archivo_copia)

    # Mensaje de confirmación
    mensaje_confirmacion = f"Se crearon {cantidad_documentos} documentos con los siguientes nombres:\n\n"
    for documento in documentos_creados:
        mensaje_confirmacion += f"{documento}\n"
    mensaje_confirmacion += f"\nLos documentos se guardaron en: {carpeta_destino}"
    messagebox.showinfo("Documentos creados", mensaje_confirmacion)

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de archivos IFC")

# Etiqueta y entrada para la ruta del archivo IFC
label_ruta = tk.Label(root, text="Ruta del archivo IFC:")
label_ruta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_ruta = tk.Entry(root, width=50)
entry_ruta.grid(row=0, column=1, padx=5, pady=5, sticky="we")
button_examinar = tk.Button(root, text="Examinar", command=lambda: entry_ruta.insert(tk.END, filedialog.askopenfilename(filetypes=[("Archivos IFC", "*.ifc")])))
button_examinar.grid(row=0, column=2, padx=5, pady=5)

# Etiqueta y entrada para la cantidad de archivos a generar
label_cantidad = tk.Label(root, text="Cantidad de archivos a generar:")
label_cantidad.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5, sticky="we")

# Botón para generar los archivos
button_generar = tk.Button(root, text="Elegir Parametros", command=crear_archivos)
button_generar.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()