awk '{ 
    # Imprimir la fecha y hora con el formato requerido
    printf "%s & ", $0
    # Cada 4 líneas, agregar \\ \midrule
    if (NR % 4 == 0) {
        print "\\ \\midrule"
    } else {
        print ""
    }
}' fechas_utc_sort_muestra2.txt

