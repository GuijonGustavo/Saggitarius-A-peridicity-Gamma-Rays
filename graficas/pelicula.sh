#!/bin/bash

# Verificar si FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null
then
    echo "FFmpeg no está instalado. Instálalo e intenta nuevamente."
    exit 1
fi

# Crear un archivo temporal con una lista de archivos y la duración
lista_ffmpeg="lista_ffmpeg.txt"
rm -f "$lista_ffmpeg"

# Leer cada archivo de lista.txt y agregarlo al archivo temporal para FFmpeg
while IFS= read -r archivo; do
    # Verificar si el archivo de imagen existe
    if [ -f "$archivo" ]; then
        # Agregar al archivo temporal el formato para FFmpeg
        echo "file '$archivo'" >> "$lista_ffmpeg"
        echo "duration 0.5" >> "$lista_ffmpeg"
    else
        echo "Archivo $archivo no encontrado, omitiendo."
    fi
done < lista.txt

# Añadir la última imagen sin duración (para que FFmpeg la procese correctamente)
ultima_imagen=$(tail -n 1 lista.txt)
echo "file '$ultima_imagen'" >> "$lista_ffmpeg"

# Generar el video en formato MP4
output_video="pelicula.mp4"
ffmpeg -f concat -safe 0 -i "$lista_ffmpeg" -vsync vfr -pix_fmt yuv420p "$output_video"

# Limpiar el archivo temporal
rm -f "$lista_ffmpeg"

echo "Película generada: $output_video"

