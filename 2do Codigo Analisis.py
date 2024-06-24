# Importación de librerías necesarias
import os
import re
import random
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ifcopenshell

# Definición de constantes para rangos de temperatura y luz por zona y estación
RANGOS_TEMPERATURA = {
    "Zona Norte": {"Invierno": (2, 22), "Otoño": (3, 24), "Primavera": (4, 24), "Verano": (7, 24)},
    "Zona Central": {"Invierno": (3, 18), "Otoño": (5, 27), "Primavera": (5, 28), "Verano": (12, 31)},
    "Zona Sur": {"Invierno": (6, 14), "Otoño": (7, 22), "Primavera": (6, 20), "Verano": (11, 23)},
    "Zona Austral": {"Invierno": (3, 11), "Otoño": (3, 18), "Primavera": (4, 16), "Verano": (10, 18)},
}

RANGOS_LUZ_SOLAR = {
    "Zona Norte": {"Invierno": (4500, 6500), "Otoño": (4500, 6500), "Primavera": (5500, 7000), "Verano": (5500, 6500)},
    "Zona Central": {"Invierno": (2000, 4000), "Otoño": (2000, 5500), "Primavera": (4000, 7000), "Verano": (5500, 7000)},
    "Zona Sur": {"Invierno": (3000, 4000), "Otoño": (3000, 5000), "Primavera": (4000, 6500), "Verano": (5000, 6500)},
    "Zona Austral": {"Invierno": (1000, 2500), "Otoño": (1000, 2000), "Primavera": (2500, 3500), "Verano": (2000, 3500)},
}

# Función para abrir el archivo IFC
def abrir_archivo_ifc(ruta_archivo):
    try:
        archivo_ifc = ifcopenshell.open(ruta_archivo)
        print("Archivo IFC abierto correctamente.")
        return archivo_ifc
    except Exception as e:
        print("Error al abrir el archivo IFC:", e)
        return None

# Función para obtener el rango de temperatura según la zona y la estación
def obtener_rango_temperatura(zona, estacion):
    try:
        return RANGOS_TEMPERATURA[zona][estacion]
    except KeyError:
        print(f"No se encontró el rango de temperatura para zona '{zona}' y estación '{estacion}'.")
        return None

# Función para calcular el rango de luz solar según la zona y la estación
def calcular_luz_solar(zona, estacion):
    try:
        return RANGOS_LUZ_SOLAR[zona][estacion]
    except KeyError:
        print(f"No se encontró el rango de luz solar para zona '{zona}' y estación '{estacion}'.")
        return None

# Función para calcular la presión de vapor saturado
def calcular_presion_vapor_saturado(temperatura):
    return 6.11 * 10**(7.5 * temperatura / (237.3 + temperatura))

# Función para calcular la humedad relativa
def calcular_humedad_relativa(temperatura, temperatura_rocio, numero_personas):
    es = calcular_presion_vapor_saturado(temperatura)
    e = calcular_presion_vapor_saturado(temperatura_rocio)
    e += 0.3 * numero_personas
    return (e / es) * 100

# Función para cambiar el valor de un parámetro en el archivo IFC
def cambiar_valor_parametro(ruta_archivo, parametro, nuevo_valor):
    try:
        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        if parametro in archivo_texto:
            archivo_modificado = re.sub(f'{parametro}\((\d+\.)\)', f'{parametro}({nuevo_valor}.)', archivo_texto)
            with open(ruta_archivo, 'w') as file:
                file.write(archivo_modificado)
        else:
            print(f"El parámetro '{parametro}' no está presente en el archivo IFC. No se realizaron cambios.")
    except Exception as e:
        print(f"Error al cambiar el valor del parámetro '{parametro}':", e)

# Función para generar archivos con valores de temperatura, humedad y luz diferentes
def generar_archivos(ruta_archivo, zona, estacion, numero_personas=""):
    try:
        cantidad_documentos = int(entry_cantidad.get())
        archivo_texto = ""

        with open(ruta_archivo, 'r') as file:
            archivo_texto = file.read()

        carpeta_destino = os.path.join(os.path.expanduser("~"), "Desktop", "Simulaciones IFC")
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        documentos_creados = []
        temperatura_rocio_celsius = random.uniform(10, 20)

        for i in range(1, cantidad_documentos + 1):
            nuevo_valor_temperatura = random.uniform(*obtener_rango_temperatura(zona, estacion))
            nuevo_valor_humedad = calcular_humedad_relativa(nuevo_valor_temperatura, temperatura_rocio_celsius, int(numero_personas))
            nuevo_valor_luz = random.uniform(*calcular_luz_solar(zona, estacion))

            # Copiar el archivo original a uno nuevo
            nuevo_archivo = os.path.join(carpeta_destino, f"Documento_{i}.ifc")
            shutil.copyfile(ruta_archivo, nuevo_archivo)

            # Modificar los parámetros en el nuevo archivo
            cambiar_valor_parametro(nuevo_archivo, "IFCTHERMODYNAMICTEMPERATUREMEASURE", nuevo_valor_temperatura)
            cambiar_valor_parametro(nuevo_archivo, "IFCPOSITIVERATIOMEASURE", nuevo_valor_humedad)
            cambiar_valor_parametro(nuevo_archivo, "IFCILLUMINANCEMEASURE", nuevo_valor_luz)

            documentos_creados.append(nuevo_archivo)

        messagebox.showinfo("Información", f"Se generaron {cantidad_documentos} archivos en '{carpeta_destino}'.")
    except Exception as e:
        print("Error al generar archivos:", e)

# Función principal para manejar la creación de archivos
def crear_archivos():
    try:
        ruta_archivo_ifc = entry_ruta.get()
        archivo_ifc = abrir_archivo_ifc(ruta_archivo_ifc)

        if archivo_ifc:
            with open(ruta_archivo_ifc, 'r') as file:
                archivo_texto = file.read()

            parametros_presentes = [
                "IFCTHERMODYNAMICTEMPERATUREMEASURE" in archivo_texto,
                "IFCPOSITIVERATIOMEASURE" in archivo_texto,
                "IFCILLUMINANCEMEASURE" in archivo_texto
            ]

            if all(parametros_presentes):
                ventana_parametros = tk.Toplevel()
                ventana_parametros.title("Condiciones para los sensores")

                label_zona = tk.Label(ventana_parametros, text="Zona:")
                label_zona.grid(row=0, column=0, padx=5, pady=5, sticky="w")
                combo_zona = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
                combo_zona.set("Zona Norte")
                combo_zona.grid(row=0, column=1, padx=5, pady=5)

                label_estacion = tk.Label(ventana_parametros, text="Estación:")
                label_estacion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
                combo_estacion = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
                combo_estacion.set("Invierno")
                combo_estacion.grid(row=1, column=1, padx=5, pady=5)

                label_numero_personas = tk.Label(ventana_parametros, text="Número de personas:")
                label_numero_personas.grid(row=2, column=0, padx=5, pady=5, sticky="w")
                entry_numero_personas = tk.Entry(ventana_parametros)
                entry_numero_personas.grid(row=2, column=1, padx=5, pady=5)

                boton_generar = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(
                    ruta_archivo_ifc,
                    combo_zona.get(),
                    combo_estacion.get(),
                    entry_numero_personas.get()
                ))
                boton_generar.grid(row=3, columnspan=2, padx=5, pady=5)

                ventana_parametros.mainloop()
            else:
                messagebox.showerror("Error", "El archivo IFC no contiene los parámetros necesarios.")
    except Exception as e:
        print("Error al crear archivos:", e)

# Interfaz gráfica principal
ventana_principal = tk.Tk()
ventana_principal.title("Simulación de Archivos IFC")
ventana_principal.geometry("400x150")

label_ruta = tk.Label(ventana_principal, text="Ruta del archivo IFC:")
label_ruta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_ruta = tk.Entry(ventana_principal, width=50)
entry_ruta.grid(row=0, column=1, padx=5, pady=5)

boton_examinar = tk.Button(ventana_principal, text="Examinar", command=lambda: entry_ruta.insert(tk.END, filedialog.askopenfilename()))
boton_examinar.grid(row=0, column=2, padx=5, pady=5)

label_cantidad = tk.Label(ventana_principal, text="Cantidad de archivos:")
label_cantidad.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_cantidad = tk.Entry(ventana_principal)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

boton_crear = tk.Button(ventana_principal, text="Crear archivos", command=crear_archivos)
boton_crear.grid(row=2, columnspan=3, padx=5, pady=5)

ventana_principal.mainloop()