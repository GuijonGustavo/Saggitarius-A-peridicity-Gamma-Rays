#!/usr/bin/env python

import pandas as pd
import numpy as np
from scipy.signal import lombscargle
from multiprocessing import Pool, cpu_count

# Definir la función para calcular el periodograma usando Lomb-Scargle
def calcular_periodograma(archivo):
    resultado = {'archivo': archivo, 'mensaje': None, 'periodo_maximo': np.nan}

    # Leer los datos del archivo actual
    try:
        data = pd.read_csv(archivo, header=None, sep=r'\s+')  # Usar una cadena cruda
    except Exception as e:
        resultado['mensaje'] = f"Error al leer el archivo: {e}"
        return resultado

    # Transformar las fechas restando el valor mínimo para iniciar desde cero
    data.iloc[:, 0] -= data.iloc[:, 0].min()

    # Convertir las fechas de días fraccionarios a minutos
    data.iloc[:, 0] *= 24 * 60

    # Multiplicar la columna de flujo por 10^8
    data.iloc[:, 1] *= 10**8

    # Eliminar filas con NaNs
    data = data.dropna()

    # Verificar si los datos son insuficientes o constantes
    if len(data) == 0 or data.iloc[:, 1].var() == 0:
        resultado['mensaje'] = "Datos insuficientes o constantes, no se puede calcular el periodograma."
        return resultado

    # Calcular el periodograma de Lomb-Scargle
    try:
        # Obtener los valores de tiempo y flujo
        time = data.iloc[:, 0].values
        flux = data.iloc[:, 1].values

        # Definir los períodos de interés (en minutos)
        frequency = np.linspace(0.001, 0.1, 700)  # Ajusta este rango según tus necesidades
        angular_frequency = 2 * np.pi * frequency
        
        # Calcular el periodograma
        power = lombscargle(time, flux, angular_frequency)

        # Encontrar el índice del máximo valor del periodograma
        max_index = np.argmax(power)

        # El índice corresponde directamente al período en minutos
        resultado['periodo_maximo'] = 1 / frequency[max_index]

    except Exception as e:
        resultado['mensaje'] = str(e)

    return resultado

# Leer la lista de archivos
with open("lista.txt", "r") as file:
    lista_archivos = [line.strip() for line in file.readlines()]

# Paralelizar el cálculo para cada archivo en la lista
num_cores = cpu_count() - 1  # Deja 1 núcleo libre
with Pool(processes=num_cores) as pool:
    resultados = pool.map(calcular_periodograma, lista_archivos)

# Guardar los resultados en un archivo de dos columnas
output_file = "resultados_periodogramas_1_700_lombscargle.txt"
output_data = pd.DataFrame({
    'archivo': [res['archivo'] for res in resultados],
    'periodicidad_maxima_minutos': [res['periodo_maximo'] if res['mensaje'] is None else "NA" for res in resultados]
})

output_data.to_csv(output_file, sep='\t', index=False, header=['Archivo', 'Periodicidad_Maxima_Minutos'])

