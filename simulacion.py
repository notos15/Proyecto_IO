import random
import math


# -------------------------------
#  FUNCIONES AUXILIARES
# -------------------------------

def exp_time(rate):
    """Genera un tiempo exponencial con parámetro rate."""
    return random.expovariate(rate)


def siguiente_estado(actual, P):
    """Devuelve el siguiente estado operativo según la matriz P."""
    r = random.random()
    if r < P[actual][0]:
        return 0
    else:
        return 1


# -------------------------------
#  SIMULADOR PRINCIPAL
# -------------------------------

def simular(lam, mu, P, c1, c2, total_minutes=480):
    """
    Simulación del sistema Markov–modulado por 8 horas.
    Imprime en la terminal todas las métricas pedidas.
    """

    # -------------------------
    # VARIABLES DEL SISTEMA
    # -------------------------

    t = 0                           # tiempo actual
    estado = 0                      # comenzamos en estado 1 (índice 0)
    c = [c1, c2]                    # capacidad por estado
    servidores = c[estado]          # servidores disponibles actuales

    N = 0                           # clientes en sistema
    cola = []                       # tiempos de llegada en cola
    en_servicio = []                # tuplas (t_fin_servicio, t_llegada)

    # Próximos eventos
    t_llegada = exp_time(lam)
    t_cambio = exp_time(1)          # cada 1 minuto revisar transición

    # Variables para métricas
    area_N = 0
    area_cola = 0
    tiempo_vacio = 0
    tiempo_inestable = 0
    llegadas = []
    tiempos_W = []

    # -------------------------
    #  BUCLE PRINCIPAL
    # -------------------------

    while t < total_minutes:

        # Próxima salida (si hay clientes en servicio)
        if en_servicio:
            t_salida = min(ev[0] for ev in en_servicio)
        else:
            t_salida = float('inf')

        # Siguiente evento
        t_evento = min(t_llegada, t_salida, t_cambio)

        # Δt
        dt = t_evento - t

        # ---- 1) Acumular integrales de tiempo ----
        area_N += N * dt

        Lq = max(0, N - servidores)
        area_cola += Lq * dt

        if N == 0:
            tiempo_vacio += dt

        # Intensidad de tráfico actual
        rho = lam / (servidores * mu)
        if rho >= 1:
            tiempo_inestable += dt

        # Avanzamos tiempo
        t = t_evento

        # ------------------------------
        #  EVENTO: LLEGADA
        # ------------------------------
        if t == t_llegada:

            N += 1
            llegadas.append(t)

            # Si hay servidor libre → entra directo a servicio
            if len(en_servicio) < servidores:
                t_fin = t + exp_time(mu)
                en_servicio.append((t_fin, t))
            else:
                cola.append(t)

            t_llegada = t + exp_time(lam)

        # ------------------------------
        #  EVENTO: SALIDA
        # ------------------------------
        elif t == t_salida:

            # Encontrar cliente que sale
            for ev in en_servicio:
                if ev[0] == t_salida:
                    t_llegada_cli = ev[1]
                    en_servicio.remove(ev)
                    break

            N -= 1

            # Tiempo en sistema
            tiempos_W.append(t - t_llegada_cli)

            # Si había gente en cola → entra un nuevo cliente a servicio
            if cola:
                t_lleg = cola.pop(0)
                t_fin = t + exp_time(mu)
                en_servicio.append((t_fin, t_lleg))

        # ------------------------------
        #  EVENTO: CAMBIO DE ESTADO
        # ------------------------------
        else:  # t == t_cambio

            nuevo_estado = siguiente_estado(estado, P)
            estado = nuevo_estado
            servidores = c[estado]

            t_cambio = t + exp_time(1)

    # -------------------------
    #  MÉTRICAS FINALES
    # -------------------------

    T = total_minutes

    L_prom = area_N / T
    W_prom = sum(tiempos_W) / len(tiempos_W) if tiempos_W else 0
    P0 = tiempo_vacio / T
    proporcion_inestable = tiempo_inestable / T

    # -------------------------
    #  IMPRIMIR RESULTADOS
    # -------------------------

    print("\n----- RESULTADOS DE LA SIMULACIÓN -----")
    print(f"Tiempo simulado: {T} minutos")
    print(f"Número promedio de clientes L = {L_prom:.4f}")
    print(f"Tiempo promedio en sistema W = {W_prom:.4f}")
    print(f"Probabilidad de sistema vacío P0 = {P0:.4f}")
    print(f"Proporción de tiempo inestable = {proporcion_inestable:.4f}")

    # Valores puntuales finales
    print("\nÚltimos valores observados:")
    print(f"N(t) final = {N}")
    print(f"Lq(t) final = {max(0, N - servidores)}")
    print(f"Estado operativo final = {estado + 1}")

    print("---------------------------------------\n")

    # Retornar algunos valores si se quieren usar en GUI
    return {
        "L": L_prom,
        "W": W_prom,
        "P0": P0,
        "inestable": proporcion_inestable,
        "N_final": N,
        "estado_final": estado + 1
    }
