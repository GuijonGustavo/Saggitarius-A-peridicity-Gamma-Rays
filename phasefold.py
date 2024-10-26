#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

# Definir la periodicidad de interés (en minutos)
periodicidad = 95.42  # en minutos

# Función para procesar la serie de tiempo (sin columna de error)
def procesar_serie(archivo):
    try:
        # Leer los datos del archivo
        data = pd.read_csv(archivo, header=None, sep=r'\s+', names=["MJD", "Flux", "Error"])

        # Transformar las fechas restando el valor mínimo para iniciar desde cero
        data['MJD'] -= data['MJD'].min()

        # Convertir las fechas de días fraccionarios a minutos
        data['MJD'] *= 24 * 60

        # Eliminar filas con NaNs
        data = data.dropna()

        # Eliminar outliers usando la regla de 3 sigma
        media_flux = np.mean(data['Flux'])
        sigma_flux = np.std(data['Flux'])
        data = data[(data['Flux'] > media_flux - 3 * sigma_flux) & (data['Flux'] < media_flux + 3 * sigma_flux)]

        # Normalizar los valores de flujo (rango 0-1)
        data['Flux'] = (data['Flux'] - data['Flux'].min()) / (data['Flux'].max() - data['Flux'].min())

        return data

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

# Función para calcular las fases de una porción de la serie de tiempo
def calcular_phasefold(data_chunk, periodicidad):
    phase = (data_chunk['MJD'] % periodicidad) / periodicidad
    return phase, data_chunk['Flux'].values

# Función para realizar el phasefolding en paralelo
def realizar_phasefolding_parallel(data, periodicidad, n_procesos=4):
    # Dividir los datos en "n_procesos" fragmentos para el procesamiento en paralelo
    data_chunks = np.array_split(data, n_procesos)

    # Crear un Pool de procesos
    with Pool(processes=n_procesos) as pool:
        resultados = pool.starmap(calcular_phasefold, [(chunk, periodicidad) for chunk in data_chunks])

    # Combinar resultados de todos los procesos
    fases = np.concatenate([resultado[0] for resultado in resultados])
    flujos_folded = np.concatenate([resultado[1] for resultado in resultados])

    # Ordenar los resultados por fase
    phase_sorted = np.argsort(fases)
    return fases[phase_sorted], flujos_folded[phase_sorted]

# Función para ajustar el eje de fase centrado en 0 con rango de -50 a 50 minutos
def ajustar_fase_centrada_en_0(phase):
    # Transformar el rango de fase de [0, 1] a [-0.5, 0.5]
    phase_centrada = phase - 0.5
    # Multiplicar por la periodicidad para obtener la fase en minutos (de -periodo/2 a +periodo/2)
    phase_centrada *= periodicidad
    return phase_centrada

# Función para graficar el phasefolding con línea promedio binned
def graficar_phasefolding_con_binned(phase, folded_flux, archivo):
    # Ajustar la fase centrada en 0
    phase_centrada = ajustar_fase_centrada_en_0(phase)

    # Graficar los puntos del phase folding
    plt.figure(figsize=(8, 6))
    plt.scatter(phase_centrada, folded_flux, s=1, color='b', label='Datos folded')

    # Crear un binning de los datos para obtener una línea que muestre la tendencia
    bins = np.linspace(-periodicidad / 2, periodicidad / 2, 50)  # Dividir la fase en 50 bins
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    bin_means = np.array([folded_flux[(phase_centrada >= bins[i]) & (phase_centrada < bins[i+1])].mean() for i in range(len(bins)-1)])

    # Graficar la línea promedio binned
    plt.plot(bin_centers, bin_means, color='r', label='Curva promedio binned', lw=2)

    plt.xlabel("Fase (minutos)")
    plt.ylabel("Flujo normalizado")
    plt.title(f"Phasefolding - {archivo}")
    plt.legend()
    plt.savefig(f"phasefolding_{archivo}_con_binned.png")
    plt.close()

# Ruta del archivo de la serie de tiempo
archivo = "sagA_450489601.dat"

# Procesar la serie de tiempo (sin usar la columna de error)
data = procesar_serie(archivo)

if data is not None:
    # Realizar el phasefolding en paralelo
    phase, folded_flux = realizar_phasefolding_parallel(data, periodicidad, n_procesos=4)

    # Guardar la fase y flujo en un archivo
    output_file = f"phasefolding_{archivo}.txt"
    pd.DataFrame({
        'fase': phase,
        'flujo': folded_flux
    }).to_csv(output_file, sep='\t', index=False, header=['Fase', 'Flujo'])

    # Graficar el phasefolding con la curva promedio binned
    graficar_phasefolding_con_binned(phase, folded_flux, archivo)
    print(f"Phasefolding completado y guardado en {output_file}. Gráfico guardado como phasefolding_{archivo}_con_binned.png")
else:
    print("No se pudo realizar el phasefolding debido a un error en los datos.")

