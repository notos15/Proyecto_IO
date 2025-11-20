import random

def estado_operativo(P, estado_actual):
    p = random.random()  # número entre 0 y 1

    if estado_actual == 1:
        # Estado 1 → P11, P12
        return 1 if p <= P[0][0] else 2
    else:
        # Estado 2 → P21, P22
        return 1 if p <= P[1][0] else 2


def simular(lam, mu, P, c1, c2, total_minutes):

    # Estado inicial
    estado = 1
    N = 0
    tiempo_inestable = 0
    tiempo = 0

    # Contadores para promedios
    total_L = 0
    total_observaciones = 0
    veces_vacio = 0

    registros = []

    while tiempo <= total_minutes:

        # ------ Elegir estado operativo ------
        estado = estado_operativo(P, estado)

        # Servidores activos según estado
        servidores = c1 if estado == 1 else c2

        # ------ Llegadas ------
        # Aproximación Poisson usando 100 subdivisiones
        llegadas = sum(1 for _ in range(100) if random.random() < lam/100)
        N += llegadas

        # ------ Servicios ------
        capacidad_servicio = mu * servidores
        atendidos = min(N, int(capacidad_servicio))
        N -= atendidos

        # ------ Métricas ------
        Lq = max(0, N - servidores)

        total_L += N
        total_observaciones += 1

        if N == 0:
            veces_vacio += 1

        if N > servidores:
            tiempo_inestable += 1

        W_prom = (total_L / lam) if lam > 0 else 0
        P0 = veces_vacio / total_observaciones

        # Guardar registro cada 5 minutos
        if tiempo % 5 == 0:
            registros.append({
                "t": tiempo,
                "N": N,
                "Lq": Lq,
                "estado": estado,
                "W": W_prom,
                "L": total_L / total_observaciones,
                "P0": P0,
                "T_inestable": tiempo_inestable
            })

        tiempo += 1

    return registros
