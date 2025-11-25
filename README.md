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

## Interfaz de usuario

La aplicación se divide en un panel izquierdo (controles) y un panel derecho (pestañas de resultados).

### Panel izquierdo - Controles
- **Matriz P**: matriz de transición 2×2 para la cadena de Markov (valores por defecto: 0.8, 0.2, 0.4, 0.6).
- **λ (tasa de llegada)**: clientes que llegan por minuto (por defecto: 5).
- **μ (tasa de servicio)**: clientes atendidos por servidor por minuto (por defecto: 4).
- **Estado 1 (c₁)**: número de servidores disponibles en el estado 1 (por defecto: 2).
- **Estado 2 (c₂)**: número de servidores disponibles en el estado 2 (por defecto: 1).
- **Tiempo de simulación**: duración total en minutos (por defecto: 480).
- **Botón "Calcular"**: inicia los cálculos teóricos y la simulación.

### Panel derecho - Pestañas

#### Pestaña "Cálculos"
Muestra los resultados de los cálculos teóricos del sistema:
- **π (distribución estacionaria)**: probabilidades de estar en cada estado a largo plazo.
- **ρ ponderado (intensidad de tráfico)**: promedio ponderado por estado.
- **L ponderado (número medio de clientes)**: cantidad promedio de clientes en el sistema.
- **W ponderado (tiempo medio en sistema)**: tiempo promedio que un cliente pasa en el sistema.

#### Pestaña "Simulación"
Tabla interactiva con registros de la simulación cada 5 minutos:
- **t**: tiempo (en minutos).
- **N(t)**: número de clientes en el sistema en el instante t.
- **Lq(t)**: número de clientes en espera (cola) en el instante t.
- **Estado**: estado operativo actual (1 o 2) según la cadena de Markov.
- **W**: tiempo medio en sistema (acumulado hasta ese momento).
- **L**: número medio de clientes (acumulado hasta ese momento).
- **P0**: probabilidad de que el sistema esté vacío (acumulada).
- **T inestable**: tiempo en el cual el sistema se estabiliza alrededor del promedio teórico π.

#### Pestaña "Gráfico"
Gráfico de barras que muestra la distribución del tiempo en cada estado:
- Compara los porcentajes observados en la simulación con los valores teóricos (66.7% Estado 1, 33.3% Estado 2).
- Incluye información del tiempo total simulado y número de muestras.

## Notas técnicas

- La simulación usa eventos discretos (llegadas, salidas, cambios de estado, registros).
- Los cambios de estado markoviano ocurren cada 5 minutos.
- Se detecta automáticamente el tiempo de estabilización comparando la proporción observada de Estado 1 con el valor teórico (2/3 con tolerancia ±5%).
- Los tiempos de servicio son exponenciales (model M/M/c).

## Contacto

Para dudas o mejoras, consulta el repositorio en GitHub: https://github.com/notos15/Proyecto_IO.git

