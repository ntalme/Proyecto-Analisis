import ifcopenshell
import os
import random
import re
import shutil
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QLineEdit, QFileDialog, QMessageBox

class GestionArchivoIFC:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.archivo_ifc = self.abrir_archivo_ifc()
        self.lineas_sensores = self.encontrar_lineas_sensores()
        self.mostrar_lineas_sensores()

    # Función para abrir un archivo IFC
    def abrir_archivo_ifc(self):
        try:
            archivo_ifc = ifcopenshell.open(self.ruta_archivo)
            print("Archivo IFC abierto correctamente.")
            return archivo_ifc
        except Exception as e:
            print("Error al abrir el archivo IFC:", e)
            return None

    # Función para leer el archivo y retornar sus líneas
    def leer_archivo(self):
        with open(self.ruta_archivo, 'r') as file:
            return file.readlines()

    # Función para escribir líneas en un archivo
    def escribir_archivo(self, lineas, nueva_ruta):
        with open(nueva_ruta, 'w') as file:
            file.writelines(lineas)

    # Función para encontrar y guardar las líneas donde se encuentran los sensores de luz, humedad y temperatura
    def encontrar_lineas_sensores(self):
        lineas = self.leer_archivo()
        lineas_sensores = {"IFCTHERMODYNAMICTEMPERATUREMEASURE": None, "IFCILLUMINANCEMEASURE": None, "IFCPOSITIVERATIOMEASURE": None}
        
        patrones = {
            "IFCTHERMODYNAMICTEMPERATUREMEASURE": re.compile(r'\bIFCTHERMODYNAMICTEMPERATUREMEASURE\b\((\d+(\.\d*)?)\)'),
            "IFCILLUMINANCEMEASURE": re.compile(r'\bIFCILLUMINANCEMEASURE\b\((\d+(\.\d*)?)\)'),
            "IFCPOSITIVERATIOMEASURE": re.compile(r'\bIFCPOSITIVERATIOMEASURE\b\((\d+(\.\d*)?)\)')
        }

        for i, linea in enumerate(lineas):
            for sensor, patron in patrones.items():
                if patron.search(linea):
                    lineas_sensores[sensor] = i
        
        return lineas_sensores

    # Función para mostrar por pantalla las líneas donde se encuentran los sensores
    def mostrar_lineas_sensores(self):
        print("Líneas de los sensores:")
        for sensor, linea in self.lineas_sensores.items():
            print(f"{sensor}: Línea {linea + 1}")

    # Función para modificar el valor de un sensor en una línea específica del archivo
    def modificar_parametro_en_linea(self, lineas, parametro, nuevo_valor):
        sensor_linea = self.lineas_sensores[parametro]
        if sensor_linea is not None:
            patron = re.compile(rf'\b{parametro}\b\((\d+(\.\d*)?)\)')
            lineas[sensor_linea] = re.sub(patron, f'{parametro}({nuevo_valor})', lineas[sensor_linea])
        else:
            print(f"El parámetro {parametro} no está presente en el archivo IFC. No se realizaron cambios.")

    # Función para obtener el rango de temperatura según la zona y estación
    def obtener_rango_temperatura(self, zona, estacion):
        rangos = {
            "Zona Norte": {"Invierno": (2, 22), "Otoño": (3, 24), "Primavera": (4, 24), "Verano": (7, 24)},
            "Zona Central": {"Invierno": (3, 18), "Otoño": (5, 27), "Primavera": (5, 28), "Verano": (12, 31)},
            "Zona Sur": {"Invierno": (6, 14), "Otoño": (7, 22), "Primavera": (6, 20), "Verano": (11, 23)},
            "Zona Austral": {"Invierno": (3, 11), "Otoño": (3, 18), "Primavera": (4, 16), "Verano": (10, 18)}
        }
        return rangos.get(zona, {}).get(estacion, None)

    # Función para calcular el rango de luz solar según la zona y estación
    def calcular_luz_solar(self, zona, estacion):
        luz_solar_rangos = {
            "Zona Norte": {"Invierno": (4500, 6500), "Otoño": (4500, 6500), "Primavera": (5500, 7000), "Verano": (5500, 6500)},
            "Zona Central": {"Invierno": (2000, 4000), "Otoño": (2000, 5500), "Primavera": (4000, 7000), "Verano": (5500, 7000)},
            "Zona Sur": {"Invierno": (3000, 4000), "Otoño": (3000, 5000), "Primavera": (4000, 6500), "Verano": (5000, 6500)},
            "Zona Austral": {"Invierno": (1000, 2500), "Otoño": (1000, 2000), "Primavera": (2500, 3500), "Verano": (2000, 3500)}
        }
        return luz_solar_rangos.get(zona, {}).get(estacion, (0, 0))

    # Función para calcular la presión de vapor saturado a una temperatura dada
    def calcular_presion_vapor_saturado(self, temperatura):
        return 6.11 * 10**(7.5 * temperatura / (237.3 + temperatura))

    # Función para calcular la humedad relativa según la temperatura, temperatura de rocío y número de personas
    def calcular_humedad_relativa(self, temperatura, temperatura_rocio, numero_personas):
        es = self.calcular_presion_vapor_saturado(temperatura)
        e = self.calcular_presion_vapor_saturado(temperatura_rocio) + 0.3 * numero_personas
        return (e / es) * 100

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Generador de Simulaciones IFC')
        self.setGeometry(200, 200, 500, 300)

        # Creación de widgets para la interfaz gráfica
        self.label_ruta = QLabel('Ruta del archivo IFC:')
        self.entry_ruta = QLineEdit()
        self.button_seleccionar = QPushButton('Seleccionar')
        self.label_zona = QLabel('Zona:')
        self.combo_zona = QComboBox()
        self.combo_zona.addItems(["Zona Norte", "Zona Central", "Zona Sur", "Zona Austral"])
        self.label_estacion = QLabel('Estación:')
        self.combo_estacion = QComboBox()
        self.combo_estacion.addItems(["Invierno", "Otoño", "Primavera", "Verano"])
        self.label_personas = QLabel('Número de personas:')
        self.entry_personas = QLineEdit()
        self.label_num_archivos = QLabel('Número de archivos a generar:')
        self.entry_num_archivos = QLineEdit()
        self.button_generar = QPushButton('Generar archivos')

        # Configuración del layout de la ventana principal
        layout = QVBoxLayout()
        layout.addWidget(self.label_ruta)
        layout.addWidget(self.entry_ruta)
        layout.addWidget(self.button_seleccionar)
        layout.addWidget(self.label_zona)
        layout.addWidget(self.combo_zona)
        layout.addWidget(self.label_estacion)
        layout.addWidget(self.combo_estacion)
        layout.addWidget(self.label_personas)
        layout.addWidget(self.entry_personas)
        layout.addWidget(self.label_num_archivos)
        layout.addWidget(self.entry_num_archivos)
        layout.addWidget(self.button_generar)
        layout.addStretch(1)
        self.setLayout(layout)

        # Conexión de los botones a sus respectivas funciones
        self.button_seleccionar.clicked.connect(self.seleccionar_archivo)
        self.button_generar.clicked.connect(self.generar_archivos)

    # Función para seleccionar un archivo IFC mediante un cuadro de diálogo
    def seleccionar_archivo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo IFC', '', 'Archivos IFC (*.ifc)')
        if ruta_archivo:
            self.entry_ruta.setText(ruta_archivo)

    # Función para generar archivos IFC con valores aleatorios de sensores
    def generar_archivos(self):
        ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", "Simulaciones IFC")
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

        ruta_archivo_original = self.entry_ruta.text()
        zona = self.combo_zona.currentText()
        estacion = self.combo_estacion.currentText()
        numero_personas = int(self.entry_personas.text())
        num_archivos = int(self.entry_num_archivos.text())

        gestion_archivo = GestionArchivoIFC(ruta_archivo_original)

        if gestion_archivo.archivo_ifc:
            rango_temperatura = gestion_archivo.obtener_rango_temperatura(zona, estacion)
            luz_solar = gestion_archivo.calcular_luz_solar(zona, estacion)

            if not rango_temperatura:
                QMessageBox.warning(self, 'Error', 'No se encontraron rangos de temperatura para la zona y estación seleccionadas.')
                return

             # Tiempo inicial
            start_time = time.time()

            # Leer el archivo original una sola vez
            with open(ruta_archivo_original, 'r') as file:
                lineas_originales = file.readlines()

            for i in range(num_archivos):
                temperatura = random.uniform(rango_temperatura[0], rango_temperatura[1])
                humedad = gestion_archivo.calcular_humedad_relativa(random.uniform(rango_temperatura[0], rango_temperatura[1]), temperatura, numero_personas)
                luz = random.uniform(luz_solar[0], luz_solar[1])
                
                # Modificar solo las líneas relevantes en el archivo original
                lineas_modificadas = lineas_originales[:]
                gestion_archivo.modificar_parametro_en_linea(lineas_modificadas, "IFCTHERMODYNAMICTEMPERATUREMEASURE", temperatura)
                gestion_archivo.modificar_parametro_en_linea(lineas_modificadas, "IFCILLUMINANCEMEASURE", luz)
                gestion_archivo.modificar_parametro_en_linea(lineas_modificadas, "IFCPOSITIVERATIOMEASURE", humedad)

                # Escribir el archivo modificado
                nombre_archivo = f"Simulacion_IFC_T{temperatura:.2f}_L{luz:.2f}_H{humedad:.2f}.ifc"
                ruta_destino = os.path.join(ruta_carpeta, nombre_archivo)
                with open(ruta_destino, 'w') as file:
                    file.writelines(lineas_modificadas)
            elapsed_time = time.time() - start_time
            print(f'Tiempo: {elapsed_time}')
            QMessageBox.information(self, 'Archivos generados', f'Se han generado {num_archivos} archivos en la carpeta "Simulaciones IFC".')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

