#!/bin/bash

# Archivos de entrada y salida
entrada="fechas_utc_sort.txt"
salida="tabla_fechas.tex"

# Número de columnas para la tabla
columnas=4

# Comienza a escribir el archivo de salida
echo "\\begin{longtable}{c c c c}" > "$salida"

echo "\\toprule" >> "$salida"
echo "UTC Date & UTC Date & UTC Date & UTC Date \\\\ \\midrule" >> "$salida"
echo "\\endfirsthead" >> "$salida"
echo "\\multicolumn{$columnas}{c}{{\\bfseries Continuación de la página anterior}} \\\\ \\toprule" >> "$salida"
echo "UTC Date & UTC Date & UTC Date & UTC Date \\\\ \\midrule" >> "$salida"

echo "\\endhead" >> "$salida"
echo "\\bottomrule" >> "$salida"

# Procesar el archivo de entrada y agregar las fechas a la tabla
awk -v cols="$columnas" '{
    printf "%s %s", $2, $3
    if (NR % cols == 0) {
        print " \\\\ \\midrule"
    } else {
        print " & "
    }
}' "$entrada" >> "$salida"

# Cerrar la tabla y el documento
echo "\\end{longtable}" >> "$salida"
echo "\\caption{Tabla de Fechas en UTC}" >> "$salida"
# echo "\\end{document}" >> "$salida"

