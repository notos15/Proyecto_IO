import random
from collections import deque

def simular(lam_hora, mu_hora, P, c1, c2, total_minutes):
    """
    Simula el sistema de colas M/M/c con cambios markovianos en servidores
    VERSIÓN CORREGIDA - Tasas en horas convertidas correctamente a minutos
    
    Parámetros:
    lam_hora: tasa de llegada (clientes/hora)
    mu_hora: tasa de servicio por servidor (clientes/hora)
    P: matriz de transición de Markov [[p11, p12], [p21, p22]]
    c1: servidores en estado 1 (ambos activos)
    c2: servidores en estado 2 (solo uno activo)
    total_minutes: tiempo total de simulación en minutos
    
    Retorna: Lista de registros con métricas del sistema cada 5 minutos
    """
    
    # ========== CONVERSIÓN CORRECTA DE UNIDADES ==========
    lam_min = lam_hora / 60.0    # clientes/minuto
    mu_min = mu_hora / 60.0      # clientes/minuto por servidor
    
    # Capacidades teóricas
    capacidad_estado1_hora = c1 * mu_hora
    capacidad_estado2_hora = c2 * mu_hora
    capacidad_promedio_hora = (2/3) * capacidad_estado1_hora + (1/3) * capacidad_estado2_hora
    
    print(f"=== INICIANDO SIMULACIÓN CORREGIDA ===")
    print(f"λ = {lam_hora}/hora = {lam_min:.4f}/minuto")
    print(f"μ = {mu_hora}/hora por servidor = {mu_min:.4f}/minuto por servidor")
    print(f"Estado 1: {c1} servidores, capacidad = {capacidad_estado1_hora}/hora")
    print(f"Estado 2: {c2} servidores, capacidad = {capacidad_estado2_hora}/hora")
    print(f"Capacidad promedio: {capacidad_promedio_hora:.2f}/hora")
    print(f"Matriz P: {P}")
    print(f"Tiempo total: {total_minutes} minutos")
    print(f"Condición estabilidad: {lam_hora} < {capacidad_promedio_hora:.2f} = {lam_hora < capacidad_promedio_hora}")
    print("=" * 60)
    
    # ========== INICIALIZACIÓN ==========
    tiempo = 0.0
    estado = 1  # Estado inicial: ambos servidores activos
    servidores_disponibles = c1
    
    # Cola de clientes: cada elemento es (tiempo_llegada, id_cliente)
    cola = deque()
    proximo_id_cliente = 0
    
    # Lista de eventos: (tipo, tiempo, datos_adicionales)
    eventos = []
    
    # ========== ESTADÍSTICAS ACUMULADAS ==========
    area_N = 0.0      # Integral de N(t) para calcular L promedio
    area_Lq = 0.0     # Integral de Lq(t) 
    tiempo_vacio = 0.0 # Tiempo total con sistema vacío
    tiempo_estado1 = 0.0  # Tiempo en estado 1
    
    # Para cálculo de W (tiempo en sistema)
    tiempos_llegada = {}  # Mapea id_cliente -> tiempo_de_llegada
    tiempos_sistema_acumulado = 0.0
    clientes_completados = 0
    
    # ========== CONFIGURACIÓN INICIAL DE EVENTOS ==========
    # Primera llegada - CORREGIDO: usar lam_min
    tiempo_proxima_llegada = random.expovariate(lam_min)
    eventos.append(('llegada', tiempo_proxima_llegada, None))
    
    # Primer cambio de estado (cada 5 minutos)
    tiempo_proximo_cambio = 5.0
    eventos.append(('cambio_estado', tiempo_proximo_cambio, None))
    
    # Primer registro de métricas (cada 5 minutos)
    tiempo_proximo_registro = 5.0
    eventos.append(('registro', tiempo_proximo_registro, None))
    
    # ========== ESTADO DE SERVIDORES ==========
    servidores_ocupados = 0
    # Lista de servidores, cada uno con su estado
    servidores = [{
        'ocupado': False, 
        'tiempo_fin_servicio': float('inf'), 
        'cliente_actual': None
    } for _ in range(max(c1, c2))]
    
    # ========== VARIABLES TEMPORALES ==========
    ultimo_tiempo = 0.0    # Para calcular delta_t entre eventos
    N_actual = 0           # Clientes en sistema (instantáneo)
    Lq_actual = 0          # Clientes en cola (instantáneo)
    
    registros = []  # Aquí se guardarán los resultados
    
    # ========== BUCLE PRINCIPAL DE SIMULACIÓN ==========
    while tiempo <= total_minutes and eventos:
        # Ordenar eventos por tiempo (el más próximo primero)
        eventos.sort(key=lambda x: x[1])
        tipo_evento, tiempo_evento, datos = eventos.pop(0)
        
        # Calcular tiempo transcurrido desde último evento
        delta_t = tiempo_evento - tiempo
        
        # ========== ACTUALIZAR ESTADÍSTICAS ACUMULADAS ==========
        area_N += N_actual * delta_t
        area_Lq += Lq_actual * delta_t
        if N_actual == 0:
            tiempo_vacio += delta_t
        if estado == 1:
            tiempo_estado1 += delta_t
        
        # Avanzar el tiempo de simulación
        tiempo = tiempo_evento
        ultimo_tiempo = tiempo
        
        # ========== PROCESAR CADA TIPO DE EVENTO ==========
        
        if tipo_evento == 'llegada':
            # ========== EVENTO: LLEGADA DE CLIENTE ==========
            cliente_id = proximo_id_cliente
            proximo_id_cliente += 1
            
            # Registrar tiempo de llegada para calcular W después
            tiempos_llegada[cliente_id] = tiempo
            
            # Agregar cliente a la cola
            cola.append((tiempo, cliente_id))
            
            # Programar próxima llegada (distribución exponencial) - CORREGIDO: usar lam_min
            tiempo_proxima_llegada = tiempo + random.expovariate(lam_min)
            eventos.append(('llegada', tiempo_proxima_llegada, None))
            
        elif tipo_evento == 'salida':
            # ========== EVENTO: FIN DE SERVICIO ==========
            servidor_id, cliente_id = datos
            
            # Liberar servidor
            servidores[servidor_id]['ocupado'] = False
            servidores[servidor_id]['tiempo_fin_servicio'] = float('inf')
            servidores[servidor_id]['cliente_actual'] = None
            servidores_ocupados -= 1
            
            # Calcular tiempo total en sistema para este cliente
            if cliente_id in tiempos_llegada:
                tiempo_llegada = tiempos_llegada.pop(cliente_id)
                tiempo_sistema = tiempo - tiempo_llegada
                tiempos_sistema_acumulado += tiempo_sistema
                clientes_completados += 1
            
        elif tipo_evento == 'cambio_estado':
            # ========== EVENTO: CAMBIO DE ESTADO MARKOVIANO ==========
            if estado == 1:
                # Transición desde estado 1 (ambos servidores)
                if random.random() < P[0][1]:  # Probabilidad de ir a estado 2
                    estado = 2
                    servidores_disponibles = c2
                else:
                    # Permanecer en estado 1
                    estado = 1
                    servidores_disponibles = c1
            else:
                # Transición desde estado 2 (un servidor)
                if random.random() < P[1][0]:  # Probabilidad de ir a estado 1
                    estado = 1
                    servidores_disponibles = c1
                else:
                    # Permanecer en estado 2
                    estado = 2
                    servidores_disponibles = c2
            
            # Programar próximo cambio de estado (cada 5 minutos)
            tiempo_proximo_cambio = tiempo + 5.0
            eventos.append(('cambio_estado', tiempo_proximo_cambio, None))
        
        elif tipo_evento == 'registro':
            # ========== EVENTO: REGISTRO DE MÉTRICAS (cada 5 minutos) ==========
            
            # Calcular métricas promedio acumuladas
            P0_promedio = tiempo_vacio / tiempo if tiempo > 0 else 0
            L_promedio = area_N / tiempo if tiempo > 0 else 0
            W_promedio = tiempos_sistema_acumulado / clientes_completados if clientes_completados > 0 else 0
            
            # Tiempo en estado "inestable" (primeros 60 minutos)
            tiempo_inestable = min(tiempo, 60.0)
            
            # Guardar registro en el formato solicitado
            registro = {
                "t": tiempo,
                "N": N_actual,           # Instantáneo: clientes en sistema
                "Lq": Lq_actual,         # Instantáneo: clientes en cola
                "estado": estado,        # Estado actual (1 o 2)
                "W": W_promedio,         # Promedio: tiempo en sistema
                "L": L_promedio,         # Promedio: clientes en sistema
                "P0": P0_promedio,       # Promedio: probabilidad sistema vacío
                "T_inestable": tiempo_inestable
            }
            registros.append(registro)
            
            # Imprimir registro en consola
            print(f"t={tiempo:3.0f}min | N(t)={N_actual:2.0f} | Lq(t)={Lq_actual:2.0f} | "
                  f"Estado={estado} | W={W_promedio:6.2f}min | L={L_promedio:5.2f} | "
                  f"P0={P0_promedio:4.2f} | T_inst={tiempo_inestable:4.1f}min")
            
            # Programar próximo registro (cada 5 minutos)
            if tiempo + 5 <= total_minutes:
                tiempo_proximo_registro = tiempo + 5
                eventos.append(('registro', tiempo_proximo_registro, None))
        
        # ========== ASIGNAR CLIENTES A SERVIDORES DISPONIBLES ==========
        # Esto se ejecuta después de CADA evento
        while cola and servidores_ocupados < servidores_disponibles:
            # Buscar un servidor libre
            servidor_libre = None
            for i in range(len(servidores)):
                if not servidores[i]['ocupado'] and i < servidores_disponibles:
                    servidor_libre = i
                    break
            
            if servidor_libre is not None:
                # Sacar al primer cliente de la cola
                tiempo_llegada_cliente, cliente_id = cola.popleft()
                
                # Calcular tiempo de servicio (distribución exponencial) - CORREGIDO: usar mu_min
                tiempo_servicio = random.expovariate(mu_min)
                tiempo_fin_servicio = tiempo + tiempo_servicio
                
                # Asignar cliente al servidor
                servidores[servidor_libre]['ocupado'] = True
                servidores[servidor_libre]['tiempo_fin_servicio'] = tiempo_fin_servicio
                servidores[servidor_libre]['cliente_actual'] = cliente_id
                servidores_ocupados += 1
                
                # Programar evento de salida
                eventos.append(('salida', tiempo_fin_servicio, (servidor_libre, cliente_id)))
        
        # ========== ACTUALIZAR MÉTRICAS INSTANTÁNEAS ==========
        N_actual = len(cola) + servidores_ocupados
        Lq_actual = len(cola)
    
    # ========== REGISTRO FINAL ==========
    # Asegurar que tenemos registro al tiempo final exacto
    if registros and registros[-1]["t"] < total_minutes:
        tiempo = total_minutes
        delta_t_final = tiempo - ultimo_tiempo
        
        # Actualizar estadísticas finales
        area_N += N_actual * delta_t_final
        area_Lq += Lq_actual * delta_t_final
        if N_actual == 0:
            tiempo_vacio += delta_t_final
        
        # Calcular métricas finales
        P0_promedio = tiempo_vacio / tiempo if tiempo > 0 else 0
        L_promedio = area_N / tiempo if tiempo > 0 else 0
        W_promedio = tiempos_sistema_acumulado / clientes_completados if clientes_completados > 0 else 0
        tiempo_inestable = min(tiempo, 60.0)
        
        registro_final = {
            "t": tiempo,
            "N": N_actual,
            "Lq": Lq_actual,
            "estado": estado,
            "W": W_promedio,
            "L": L_promedio,
            "P0": P0_promedio,
            "T_inestable": tiempo_inestable
        }
        registros.append(registro_final)
        
        # Imprimir registro final
        print(f"t={tiempo:3.0f}min | N(t)={N_actual:2.0f} | Lq(t)={Lq_actual:2.0f} | "
              f"Estado={estado} | W={W_promedio:6.2f}min | L={L_promedio:5.2f} | "
              f"P0={P0_promedio:4.2f} | T_inst={tiempo_inestable:4.1f}min")
    
    # ========== RESUMEN FINAL ==========
    proporcion_estado1 = tiempo_estado1 / tiempo if tiempo > 0 else 0
    
    print("\n" + "=" * 60)
    print("=== RESUMEN FINAL DE LA SIMULACIÓN CORREGIDA ===")
    print(f"Tiempo total simulado: {tiempo:.1f} minutos")
    print(f"Clientes atendidos: {clientes_completados}")
    print(f"L final (promedio): {L_promedio:.2f} clientes")
    print(f"W final (promedio): {W_promedio:.2f} minutos ({W_promedio/60:.2f} horas)")
    print(f"P0 final: {P0_promedio:.3f}")
    print(f"Proporción estado 1: {proporcion_estado1:.3f} (teórico: 0.667)")
    print(f"Proporción estado 2: {1-proporcion_estado1:.3f} (teórico: 0.333)")
    print(f"Clientes en cola al final: {Lq_actual}")
    print(f"Clientes en sistema al final: {N_actual}")
    print(f"Verificación Little: L = {L_promedio:.2f}, λW = {lam_min * 60 * W_promedio/60:.2f}")
    print("=" * 60)
    
    return registros

# ========== EJECUCIÓN DE PRUEBA ==========
if __name__ == "__main__":
    # Parámetros del problema - EN HORAS como debe ser
    lambda_hora = 5  # clientes/hora
    mu_hora = 4      # clientes/hora por servidor
    
    P = [[0.8, 0.2], [0.4, 0.6]]
    c1 = 2  # servidores en estado 1
    c2 = 1  # servidores en estado 2
    tiempo_total = 480  # minutos (8 horas)
    
    # Ejecutar simulación CORREGIDA
    resultados = simular(lambda_hora, mu_hora, P, c1, c2, tiempo_total)