import random
from collections import deque

def simular(lam, mu, P, c1, c2, total_minutes):
    """
    Simula el sistema de colas M/M/c con cambios markovianos.
    lam : tasa de llegada por minuto
    mu  : tasa de servicio por minuto por servidor
    """

    # ===== INICIALIZACIÓN =====
    tiempo = 0.0
    estado = 1
    servidores_disponibles = c1

    cola = deque()
    proximo_id = 0

    eventos = []

    # Estadísticas acumuladas
    area_N = 0.0
    area_Lq = 0.0
    tiempo_vacio = 0.0
    tiempo_estado1 = 0.0

    # Para W
    tiempos_llegada = {}
    suma_W = 0.0
    clientes_completados = 0

    # Para T_inestable CORREGIDO
    tiempo_estabilizacion = None
    epsilon = 0.05  # 5% de tolerancia

    # Eventos iniciales
    eventos.append(("llegada", random.expovariate(lam), None))
    eventos.append(("cambio_estado", 5.0, None))
    eventos.append(("registro", 5.0, None))

    # Estado de servidores
    servidores = [{
        "ocupado": False,
        "fin": float("inf"),
        "cliente": None
    } for _ in range(max(c1, c2))]

    servidores_ocupados = 0

    # Variables instantáneas
    N_actual = 0
    Lq_actual = 0

    registros = []
    ultimo_tiempo = 0.0

    # ===== BUCLE PRINCIPAL =====
    while tiempo <= total_minutes and eventos:

        eventos.sort(key=lambda x: x[1])
        tipo, t_evento, datos = eventos.pop(0)

        dt = t_evento - tiempo

        # Acumulación
        area_N += N_actual * dt
        area_Lq += Lq_actual * dt
        if N_actual == 0:
            tiempo_vacio += dt
        if estado == 1:
            tiempo_estado1 += dt

        tiempo = t_evento
        ultimo_tiempo = tiempo

        # ===== VERIFICAR ESTABILIZACIÓN (NUEVO) =====
        if tiempo_estabilizacion is None and tiempo > 30:  # Esperar al menos 30 min
            proporcion_estado1_actual = tiempo_estado1 / tiempo
            if abs(proporcion_estado1_actual - 2/3) < epsilon:
                tiempo_estabilizacion = tiempo

        # ===== PROCESAR EVENTOS =====
        if tipo == "llegada":

            cliente_id = proximo_id
            proximo_id += 1
            tiempos_llegada[cliente_id] = tiempo
            cola.append(cliente_id)

            # siguiente llegada
            eventos.append(("llegada", tiempo + random.expovariate(lam), None))

        elif tipo == "salida":
            servidor_id, cliente_id = datos

            servidores[servidor_id]["ocupado"] = False
            servidores[servidor_id]["fin"] = float("inf")
            servidores[servidor_id]["cliente"] = None
            servidores_ocupados -= 1

            # tiempo en sistema
            t_llegada = tiempos_llegada.pop(cliente_id)
            suma_W += (tiempo - t_llegada)
            clientes_completados += 1

        elif tipo == "cambio_estado":

            # Transición markoviana
            if estado == 1:
                estado = 1 if random.random() < P[0][0] else 2
            else:
                estado = 1 if random.random() < P[1][0] else 2

            servidores_disponibles = c1 if estado == 1 else c2
            eventos.append(("cambio_estado", tiempo + 5.0, None))

        elif tipo == "registro":

            L_prom = area_N / tiempo if tiempo > 0 else 0
            W_prom = suma_W / clientes_completados if clientes_completados > 0 else 0
            P0_prom = tiempo_vacio / tiempo if tiempo > 0 else 0
            
            # T_inestable CORREGIDO
            if tiempo_estabilizacion is not None:
                T_inst = tiempo_estabilizacion
            else:
                T_inst = tiempo  # Si no se ha estabilizado, es el tiempo actual

            registros.append({
                "t": tiempo,
                "N": N_actual,
                "Lq": Lq_actual,
                "estado": estado,
                "W": W_prom,
                "L": L_prom,
                "P0": P0_prom,
                "T_inestable": T_inst
            })

            if tiempo + 5 <= total_minutes:
                eventos.append(("registro", tiempo + 5.0, None))

        # ===== ASIGNAR SERVICIO DESPUÉS DE CADA EVENTO =====
        while cola and servidores_ocupados < servidores_disponibles:
            # Buscar un servidor libre
            for i in range(len(servidores)):
                if not servidores[i]["ocupado"] and i < servidores_disponibles:

                    cliente = cola.popleft()
                    tiempo_serv = random.expovariate(mu)
                    fin_serv = tiempo + tiempo_serv

                    servidores[i]["ocupado"] = True
                    servidores[i]["cliente"] = cliente
                    servidores[i]["fin"] = fin_serv
                    servidores_ocupados += 1

                    eventos.append(("salida", fin_serv, (i, cliente)))
                    break

        # ===== ACTUALIZAR MÉTRICAS INSTANTÁNEAS =====
        N_actual = servidores_ocupados + len(cola)
        Lq_actual = len(cola)

    # ===== REGISTRO FINAL EXACTO EN t = total_minutes =====
    if registros and registros[-1]["t"] < total_minutes:

        dt = total_minutes - ultimo_tiempo

        area_N += N_actual * dt
        area_Lq += Lq_actual * dt
        if N_actual == 0:
            tiempo_vacio += dt

        L_prom = area_N / total_minutes
        W_prom = suma_W / clientes_completados if clientes_completados > 0 else 0
        P0_prom = tiempo_vacio / total_minutes
        
        # T_inestable CORREGIDO (final)
        if tiempo_estabilizacion is not None:
            T_inst = tiempo_estabilizacion
        else:
            T_inst = total_minutes  # Si nunca se estabilizó, es el tiempo total

        registros.append({
            "t": total_minutes,
            "N": N_actual,
            "Lq": Lq_actual,
            "estado": estado,
            "W": W_prom,
            "L": L_prom,
            "P0": P0_prom,
            "T_inestable": T_inst
        })

    return registros