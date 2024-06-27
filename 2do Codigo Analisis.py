import os
import ifcopenshell
import re
import random
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def abrir_archivo_ifc(ruta_archivo):
    try:
        archivo_ifc = ifcopenshell.open(ruta_archivo)
        print("Archivo IFC abierto correctamente.")
        return archivo_ifc
    except Exception as e:
        print("Error al abrir el archivo IFC:", e)
        return None

def obtener_rango_temperatura(zona, estacion):
    if zona == "Zona Norte":
        if estacion == "Invierno":
            return (2, 22)
        elif estacion == "Otoño":
            return (3, 24)
        elif estacion == "Primavera":
            return (4, 24)
        elif estacion == "Verano":
            return (7, 24)
    elif zona == "Zona Central":
        if estacion == "Invierno":
            return (3, 18)
        elif estacion == "Otoño":
            return (5, 27)
        elif estacion == "Primavera":
            return (5, 28)
        elif estacion == "Verano":
            return (12, 31)
    elif zona == "Zona Sur":
        if estacion == "Invierno":
            return (6, 14)
        elif estacion == "Otoño":
            return (7, 22)
        elif estacion == "Primavera":
            return (6, 20)
        elif estacion == "Verano":
            return (11, 23)
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

def calcular_luz_solar(zona, estacion):
    luz_solar = 0
    if zona == "Zona Norte":
        if estacion == "Invierno":
            luz_solar = (4500, 6500)
        elif estacion == "Otoño":
            luz_solar = (4500, 6500)
        elif estacion == "Primavera":
            luz_solar = (5500, 7000)
        elif estacion == "Verano":
            luz_solar = (5500, 6500)
    elif zona == "Zona Central":
        if estacion == "Invierno":
            luz_solar = (2000, 4000)
        elif estacion == "Otoño":
            luz_solar = (2000, 5500)
        elif estacion == "Primavera":
            luz_solar = (4000, 7000)
        elif estacion == "Verano":
            luz_solar = (5500, 7000)
    elif zona == "Zona Sur":
        if estacion == "Invierno":
            luz_solar = (3000, 4000)
        elif estacion == "Otoño":
            luz_solar = (3000, 5000)
        elif estacion == "Primavera":
            luz_solar = (4000, 6500)
        elif estacion == "Verano":
            luz_solar = (5000, 6500)
    elif zona == "Zona Austral":
        if estacion == "Invierno":
            luz_solar = (1000, 2500)
        elif estacion == "Otoño":
            luz_solar = (1000, 2000)
        elif estacion == "Primavera":
            luz_solar = (2500, 3500)
        elif estacion == "Verano":
            luz_solar = (2000, 3500)
    return luz_solar

def calcular_presion_vapor_saturado(temperatura):
    return 6.11 * 10**(7.5 * temperatura / (237.3 + temperatura))

def calcular_humedad_relativa(temperatura, temperatura_rocio, numero_personas):
    es = calcular_presion_vapor_saturado(temperatura)
    e = calcular_presion_vapor_saturado(temperatura_rocio)
    e += 0.3 * numero_personas
    return (e / es) * 100

def obtener_posiciones_relevantes(ruta_archivo):
    posiciones = {"temperatura": [], "humedad": [], "luz": []}
    with open(ruta_archivo, 'r') as file:
        lineas = file.readlines()
        for i, linea in enumerate(lineas):
            if "IFCTHERMODYNAMICTEMPERATUREMEASURE" in linea:
                posiciones["temperatura"].append(i)
            elif "IFCPOSITIVERATIOMEASURE" in linea:
                posiciones["humedad"].append(i)
            elif "IFCILLUMINANCEMEASURE" in linea:
                posiciones["luz"].append(i)
    return posiciones, lineas

def modificar_valores(lineas, posiciones, tipo, nuevo_valor):
    valor_formateado = f'{nuevo_valor:.1f}'
    if tipo == "temperatura":
        for pos in posiciones["temperatura"]:
            lineas[pos] = re.sub(r'IFCTHERMODYNAMICTEMPERATUREMEASURE\(\d+\.\d+\)', f'IFCTHERMODYNAMICTEMPERATUREMEASURE({valor_formateado})', lineas[pos])
    elif tipo == "humedad":
        for pos in posiciones["humedad"]:
            lineas[pos] = re.sub(r'IFCPOSITIVERATIOMEASURE\(\d+\.\d+\)', f'IFCPOSITIVERATIOMEASURE({valor_formateado})', lineas[pos])
    elif tipo == "luz":
        for pos in posiciones["luz"]:
            lineas[pos] = re.sub(r'IFCILLUMINANCEMEASURE\(\d+\.\d+\)', f'IFCILLUMINANCEMEASURE({valor_formateado})', lineas[pos])

def generar_archivos(ruta_archivo_ifc, zona, estacion, num_archivos, numero_personas):
    try:
        posiciones, lineas = obtener_posiciones_relevantes(ruta_archivo_ifc)
        
        # Obtener la ruta del escritorio
        escritorio = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        # Crear la carpeta de simulaciones IFC si no existe
        carpeta_simulaciones = os.path.join(escritorio, 'Simulaciones IFC')
        if not os.path.exists(carpeta_simulaciones):
            os.makedirs(carpeta_simulaciones)
        
        for idx in range(num_archivos):
            lineas_copia = lineas.copy()
            if posiciones["temperatura"]:
                nuevo_valor_temperatura = random.uniform(*obtener_rango_temperatura(zona, estacion))
                modificar_valores(lineas_copia, posiciones, "temperatura", nuevo_valor_temperatura)
            if posiciones["humedad"]:
                nuevo_valor_humedad = random.uniform(30, 70)  # Ejemplo de rango para humedad
                temperatura_actual = float(re.search(r'IFCTHERMODYNAMICTEMPERATUREMEASURE\((\d+\.\d+)\)', lineas[posiciones["temperatura"][0]]).group(1))
                temperatura_rocio = calcular_temperatura_rocio(temperatura_actual, nuevo_valor_humedad)
                nuevo_valor_humedad = calcular_humedad_relativa(temperatura_actual, temperatura_rocio, numero_personas)
                modificar_valores(lineas_copia, posiciones, "humedad", nuevo_valor_humedad)
            if posiciones["luz"]:
                nuevo_valor_luz = random.uniform(*calcular_luz_solar(zona, estacion))
                modificar_valores(lineas_copia, posiciones, "luz", nuevo_valor_luz)

            # Determinar el nombre del archivo según los sensores presentes
            nombre_base = os.path.splitext(os.path.basename(ruta_archivo_ifc))[0]
            nombre_archivo = nombre_base

            if posiciones["temperatura"]:
                nombre_archivo += f"_T{nuevo_valor_temperatura:.1f}"
            if posiciones["humedad"]:
                nombre_archivo += f"_H{nuevo_valor_humedad:.1f}"
            if posiciones["luz"]:
                nombre_archivo += f"_L{nuevo_valor_luz:.1f}"
            
            nombre_archivo += ".ifc"

            # Guardar el archivo en la carpeta de simulaciones IFC
            ruta_archivo_guardado = os.path.join(carpeta_simulaciones, nombre_archivo)
            
            with open(ruta_archivo_guardado, 'w') as file:
                file.writelines(lineas_copia)
        
        messagebox.showinfo("Archivos generados", f"Se generaron {num_archivos} archivos adicionales con valores editados en '{carpeta_simulaciones}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al generar los archivos: {e}")



def crear_archivos():
    ruta_archivo_ifc = entry_ruta.get()
    archivo_ifc = abrir_archivo_ifc(ruta_archivo_ifc)

    if archivo_ifc:
        posiciones, lineas = obtener_posiciones_relevantes(ruta_archivo_ifc)
        
        if posiciones["temperatura"] or posiciones["humedad"] or posiciones["luz"]:
            ventana_parametros = tk.Toplevel()
            ventana_parametros.title("Condiciones para los sensores")

            label_zona = tk.Label(ventana_parametros, text="Zona:")
            label_zona.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            combo_zona = ttk.Combobox(ventana_parametros, values=["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
            combo_zona.set("Zona Norte")
            combo_zona.grid(row=0, column=1, padx=5, pady=5, sticky="we")

            label_estacion = tk.Label(ventana_parametros, text="Estación:")
            label_estacion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            combo_estacion = ttk.Combobox(ventana_parametros, values=["Invierno", "Otoño", "Primavera", "Verano"])
            combo_estacion.set("Invierno")
            combo_estacion.grid(row=1, column=1, padx=5, pady=5, sticky="we")

            label_num_archivos = tk.Label(ventana_parametros, text="Número de archivos a generar:")
            label_num_archivos.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            entry_num_archivos = tk.Entry(ventana_parametros)
            entry_num_archivos.grid(row=2, column=1, padx=5, pady=5, sticky="we")

            button_generar = tk.Button(ventana_parametros, text="Generar archivos", command=lambda: generar_archivos(ruta_archivo_ifc, combo_zona.get(), combo_estacion.get(), int(entry_num_archivos.get())))
            button_generar.grid(row=3, column=0, columnspan=2, pady=10)

            ventana_parametros.transient()
            ventana_parametros.grab_set()
            ventana_parametros.wait_window()
        else:
            messagebox.showerror("Error", "No se encontraron sensores en el archivo IFC.")
    else:
        messagebox.showerror("Error", "No se pudo abrir el archivo IFC.")

def crear_interfaz():
    try:
        global entry_ruta
        root = tk.Tk()
        root.title("Generador de archivos IFC")

        label_ruta = tk.Label(root, text="Ruta del archivo IFC:")
        label_ruta.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_ruta = tk.Entry(root, width=50)
        entry_ruta.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        button_seleccionar = tk.Button(root, text="Seleccionar archivo", command=lambda: entry_ruta.insert(tk.END, filedialog.askopenfilename()))
        button_seleccionar.grid(row=0, column=2, padx=5, pady=5)

        button_crear_archivos = tk.Button(root, text="Crear Archivos", command=crear_archivos)
        button_crear_archivos.grid(row=1, column=0, columnspan=3, pady=10)

        button_salir = tk.Button(root, text="Salir", command=root.quit)
        button_salir.grid(row=2, column=0, columnspan=3, pady=10)

        root.mainloop()
    except Exception as e:
        print("Error al crear la interfaz:", e)

if __name__ == "__main__":
    crear_interfaz()