#!/usr/bin/env Rscript

# Cargar las librerías necesarias
library(RobPer)
library(parallel)

# Definir el número de núcleos para usar (ajustable según la CPU)
num_cores <- detectCores() - 1  # Deja 1 núcleo libre

# Leer la lista de archivos
lista_archivos <- readLines("lista.txt")

# Función para transformar y calcular el periodograma
calcular_periodograma <- function(archivo) {
  resultado <- list(archivo = archivo, mensaje = NULL, periodo_maximo = NA)
  
  # Leer los datos del archivo actual
  data <- tryCatch(read.table(archivo, header = FALSE), error = function(e) return(NULL))
  if (is.null(data)) {
    resultado$mensaje <- "Error al leer el archivo."
    return(resultado)
  }
  
  # Transformar las fechas restando el valor mínimo para iniciar desde cero
  data[, 1] <- data[, 1] - min(data[, 1])
  
  # Convertir las fechas de días fraccionarios a minutos (multiplicando por 24*60)
  data[, 1] <- data[, 1] * 24 * 60
  
  # Multiplicar la columna de flujo (segunda columna) por 10^8 para evitar valores muy pequeños
  data[, 2] <- data[, 2] * 10^8
  
  # Eliminar filas con NAs
  data <- na.omit(data)
  
  # Verificar si los datos no son constantes o insuficientes
  if (nrow(data) == 0 || var(data[, 2]) == 0) {
    resultado$mensaje <- "Datos insuficientes o constantes, no se puede calcular el periodograma."
    return(resultado)
  }
  
  # Intentar calcular el periodograma
  tryCatch({
    rp <- RobPer(data, model = "sine", regression = "tau", weighting =FALSE, var1 = FALSE, periods = 1:700)
    
    # Encontrar el índice del máximo valor del periodograma
    max_index <- which.max(rp)
    
    # El índice corresponde directamente al período en minutos
    resultado$periodo_maximo <- max_index
    
  }, error = function(e) {
    resultado$mensaje <- e$message
  })
  
  return(resultado)
}

# Paralelizar el cálculo para cada archivo en la lista
resultados <- mclapply(lista_archivos, calcular_periodograma, mc.cores = num_cores)

# Guardar los resultados en un archivo de dos columnas
output_file <- "resultados_periodogramas_1_700periodos_modelsine.txt"
write.table(
  data.frame(
    archivo = sapply(resultados, function(x) x$archivo),
    periodicidad_max = sapply(resultados, function(x) ifelse(is.na(x$periodo_maximo), "NA", x$periodo_maximo))
  ),
  file = output_file,
  col.names = c("Archivo", "Periodicidad_Maxima_Minutos"),
  row.names = FALSE,
  sep = "\t",
  quote = FALSE
)

