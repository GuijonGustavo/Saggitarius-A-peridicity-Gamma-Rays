def transformar_fechas(archivo_entrada, archivo_salida):
    """
    Transforma un archivo de fechas en un formato tabular con la estructura deseada.
    
    Args:
        archivo_entrada (str): Nombre del archivo de entrada con las fechas.
        archivo_salida (str): Nombre del archivo de salida con el formato transformado.
    """
    with open(archivo_entrada, 'r') as entrada:
        fechas = [linea.strip() for linea in entrada if linea.strip()]

    with open(archivo_salida, 'w') as salida:
        for i in range(0, len(fechas), 4):
            bloque = fechas[i:i+4]
            # Agregar un `&` al final de cada línea excepto la última del bloque
            for fecha in bloque[:-1]:
                salida.write(f"{fecha} &\n")
            # La última fecha del bloque seguido de `\\ \midrule`
            salida.write(f"{bloque[-1]} \\\\ \\midrule\n")

# Ejecución
archivo_entrada = "fechas_utc_sort_muestra2.txt"
archivo_salida = "fechas_transformadas.txt"
transformar_fechas(archivo_entrada, archivo_salida)

