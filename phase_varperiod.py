#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool, cpu_count

# Crear carpeta principal para las imágenes y archivos .dat
carpeta_principal = "variacion_periodicidad"
os.makedirs(carpeta_principal, exist_ok=True)

# Rango de periodicidades
periodicidades = range(10, 721)  # de 30 a 200 minutos

# Función para procesar la serie de tiempo (sin columna de error)
def procesar_serie(archivo):
    try:
        data = pd.read_csv(archivo, header=None, sep=r'\s+', names=["MJD", "Flux", "Error"])
        data['MJD'] -= data['MJD'].min()
        data['MJD'] *= 24 * 60
        data = data.dropna()
        media_flux = np.mean(data['Flux'])
        sigma_flux = np.std(data['Flux'])
        data = data[(data['Flux'] > media_flux - 3 * sigma_flux) & (data['Flux'] < media_flux + 3 * sigma_flux)]
        data['Flux'] = (data['Flux'] - data['Flux'].min()) / (data['Flux'].max() - data['Flux'].min())
        return data
    except Exception as e:
        print(f"Error al procesar el archivo {archivo}: {e}")
        return None

# Función para calcular las fases y flujos de cada archivo
def calcular_phasefold(data, periodicidad):
    phase = (data['MJD'] % periodicidad) / periodicidad
    return phase, data['Flux'].values

# Función para ajustar la fase centrada en 0 con rango -período/2 a +período/2
def ajustar_fase_centrada_en_0(phase, periodicidad):
    return (phase - 0.5) * periodicidad

# Función para graficar el phase folding de múltiples archivos en una sola gráfica y guardar los datos en .dat
def graficar_y_guardar_datos(periodicidad, phase_foldings):
    # Crear gráfica
    plt.figure(figsize=(10, 6))
    fases_total = []
    flujos_total = []

    for phase, folded_flux in phase_foldings:
        phase_centrada = ajustar_fase_centrada_en_0(phase, periodicidad)
        plt.scatter(phase_centrada, folded_flux, s=1, alpha=0.5)
        
        # Almacenar datos en listas
        fases_total.extend(phase_centrada)
        flujos_total.extend(folded_flux)

    # Configuración de la gráfica
    plt.xlabel("Fase (minutos)")
    plt.ylabel("Flujo normalizado")
    plt.title(f"Phase Folding para Periodicidad = {periodicidad} minutos")
    plt.axvline(0, color='red', linestyle='--')
    plt.xlim(-periodicidad / 2, periodicidad / 2)
    plt.tight_layout()
    
    # Guardar imagen
    plt.savefig(os.path.join(carpeta_principal, f"phasefolding_periodicidad_{periodicidad}.png"))
    plt.close()

    # Guardar datos en archivo .dat
    archivo_dat = os.path.join(carpeta_principal, f"phasefolding_periodicidad_{periodicidad}.dat")
    datos_df = pd.DataFrame({"Fase": fases_total, "Flujo_normalizado": flujos_total})
    datos_df.to_csv(archivo_dat, sep='\t', index=False, header=True)

# Leer la lista de archivos desde 'lista.txt'
lista_archivos = 'filtrado_periodicidades_95.42_robper.txt'
with open(lista_archivos, 'r') as f:
    archivos = [line.strip() for line in f.readlines()]

# Procesar todos los archivos
def procesar_archivo(archivo):
    return procesar_serie(archivo)

# Usar todos los núcleos para procesar archivos en paralelo
with Pool(cpu_count()) as pool:
    datos_procesados = pool.map(procesar_archivo, archivos)

# Filtrar archivos que no se procesaron correctamente
datos_procesados = [data for data in datos_procesados if data is not None]

# Loop para cada periodicidad y graficar cada set de datos en una gráfica y archivo .dat
for periodicidad in periodicidades:
    # Calcular el phase folding para cada archivo con la periodicidad actual
    phase_foldings = [calcular_phasefold(data, periodicidad) for data in datos_procesados]
    
    # Graficar y guardar phase foldings en una gráfica y archivo .dat para la periodicidad actual
    graficar_y_guardar_datos(periodicidad, phase_foldings)

print("Phasefolding completado. Gráficos e archivos .dat guardados en 'variacion_periodicidad'.")

