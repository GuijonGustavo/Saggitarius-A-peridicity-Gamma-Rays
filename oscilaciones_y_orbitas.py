import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configuración de parámetros
periodos = [48, 32, 96]  # En minutos
frecuencias = [1/p for p in periodos]  # Frecuencia inversa del periodo
tiempo_total = 500  # Minutos
fps = 1000  # Cuadros por segundo
interval = 1000 / fps  # Intervalo entre cuadros en milisegundos

# Definir el tiempo y las señales de oscilación
t = np.linspace(0, tiempo_total, int(fps * tiempo_total / 60))
oscilaciones = [np.sin(2 * np.pi * f * t) for f in frecuencias]

# Coordenadas para órbitas circulares
radio = 1.0  # Radio de la órbita
angulo_inclinacion = np.radians(80)  # Inclinación en 80 grados

# Inicializar figuras
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(24, 15))  # Cambiamos figsize para hacer más ancho el gráfico superior
ax1.set_xlim(0, tiempo_total)
ax1.set_ylim(-1.5, 1.5)
ax2.set_aspect('equal')
ax2.set_xlim(-1.2, 1.2)
ax2.set_ylim(-1.2 * np.cos(angulo_inclinacion), 1.2 * np.cos(angulo_inclinacion))
ax3.set_aspect('equal')
ax3.set_xlim(-1.2, 1.2)
ax3.set_ylim(-1.2, 1.2)

# Configuración para la gráfica de oscilaciones (arriba)
lineas_osc = [ax1.plot([], [], label=f'Periodo {p} min')[0] for p in periodos]
ax1.set_title("Oscilaciones")
ax1.set_xlabel("Tiempo (minutos)")
ax1.set_ylabel("Amplitud")
ax1.legend()  # Mostrar leyenda en la gráfica de oscilaciones

# Configuración para la gráfica de órbitas inclinadas (segundo gráfico)
puntos_orbitas_inclinadas = [ax2.plot([], [], 'o', markersize=8, label=f'Periodo {p} min')[0] for p in periodos]
angulo_base = np.linspace(0, 2 * np.pi, 100)
x_circulo_inclinado = radio * np.cos(angulo_base)
y_circulo_inclinado = radio * np.sin(angulo_base) * np.cos(angulo_inclinacion)  # Aplicando la inclinación

# Dibujar la órbita circular inclinada
ax2.plot(x_circulo_inclinado, y_circulo_inclinado, 'k--', alpha=0.5)
yticks = np.linspace(-1, 1, 5) * np.cos(angulo_inclinacion)
ax2.set_yticks(yticks)
ax2.set_yticklabels([f"{ytick:.2f}" for ytick in yticks])
ax2.set_title("Órbitas inclinadas")
ax2.set_xlabel("X")
ax2.set_ylabel("Y (inclinación de 80°)")
ax2.legend()  # Mostrar leyenda en la gráfica de órbitas inclinadas

# Configuración para la gráfica de órbitas vista desde arriba (tercer gráfico)
puntos_orbitas_arriba = [ax3.plot([], [], 'o', markersize=8, label=f'Periodo {p} min')[0] for p in periodos]
x_circulo_arriba = radio * np.cos(angulo_base)
y_circulo_arriba = radio * np.sin(angulo_base)

# Dibujar la órbita circular sin inclinación
ax3.plot(x_circulo_arriba, y_circulo_arriba, 'k--', alpha=0.5)
ax3.set_title("Vista superior (círculo)")
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.legend()  # Mostrar leyenda en la vista superior

# Función de actualización para la animación
def update(frame):
    # Actualizar gráficos de oscilaciones
    for osc, linea in zip(oscilaciones, lineas_osc):
        linea.set_data(t[:frame], osc[:frame])

    # Actualizar posiciones en la órbita inclinada
    for i, punto in enumerate(puntos_orbitas_inclinadas):
        # Ángulo en la órbita para cada objeto, basado en su periodo
        theta = 2 * np.pi * (t[frame] / periodos[i])
        x = radio * np.cos(theta)
        y = radio * np.sin(theta)

        # Proyección inclinada
        x_inclinado = x
        y_inclinado = y * np.cos(angulo_inclinacion)
        punto.set_data(x_inclinado, y_inclinado)

    # Actualizar posiciones en la vista desde arriba (circular)
    for i, punto in enumerate(puntos_orbitas_arriba):
        # Ángulo en la órbita para cada objeto, basado en su periodo
        theta = 2 * np.pi * (t[frame] / periodos[i])
        x = radio * np.cos(theta)
        y = radio * np.sin(theta)
        punto.set_data(x, y)

    return lineas_osc + puntos_orbitas_inclinadas + puntos_orbitas_arriba

# Crear y guardar la animación
anim = FuncAnimation(fig, update, frames=len(t), interval=interval, blit=True)
anim.save('oscilaciones_y_orbitas.mp4', writer='ffmpeg', fps=fps)

plt.show()

