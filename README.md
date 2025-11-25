# Proyecto_IO

Aplicación GUI en Python que simula un sistema de colas M/M/c con cambios markovianos entre dos estados. La interfaz permite ingresar la matriz de transición, las tasas y parámetros del sistema, ejecutar los cálculos teóricos y la simulación, y visualizar un gráfico con la distribución del tiempo en cada estado.

Archivos principales
- `main.py` : Interfaz gráfica (tkinter) y orquestador.
- `calculos.py` : Cálculos teóricos (π estacionaria, métricas L/W, intensidades).
- `simulacion.py` : Simulador de eventos discretos que genera registros por intervalo.
- `graficos.py` : Generación del gráfico con matplotlib integrado en Tkinter.

Requisitos
- Python 3.12+ (el proyecto fue probado con Python 3.12).
- Paquetes del sistema:

  - `python3-numpy` (o `numpy` en tu entorno)
  - `python3-matplotlib` (para `matplotlib` y backend TkAgg)
  - `python3-tk` (soporte de Tkinter)


Ejecutar la aplicación

- Ejecutar con el Python del sistema:

```bash
python3 main.py
```
Interfaz
En la pestaña de Cálculos se encuentran valores predefinidos para la tasa de llegada, tasa de servicio, matriz p, los estados y el tiempo de ejecucion. Estos se pueden modificar para finalmente calcular los valores de rho, L y W que apareceran en pantalla.
La pestaña de Simulación genera escenarios con parámetros configurables y puede ejecutar múltiples réplicas del modelo, mostrando métricas en tiempo real como longitud de cola, estado del sistema y tiempos de permanencia.
La pestaña de Gráficos muestra visualizaciones interactivas de los resultados, incluyendo evolución temporal de las colas, distribución del tiempo en cada estado markoviano y comparación entre valores teóricos y simulados.
# Proyecto_IO

