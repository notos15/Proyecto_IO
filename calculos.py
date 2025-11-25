import numpy as np
import math

# Pregunta a
def calcular_pi(P):
    """
    Calcula la distribución estacionaria π para una matriz de transición P.
    """
    P = np.array(P, dtype=float)
    n = P.shape[0]

    A = np.transpose(P) - np.eye(n)
    A = np.vstack([A, np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1

    pi = np.linalg.lstsq(A, b, rcond=None)[0]
    return pi

# Pregunta b
def calcular_rho(lam, mu, c):
    """Calcula ρ = λ / (c * μ) para un estado"""
    return lam / (c * mu)

def calcular_L_MMc(lam, mu, c):
    """Calcula L para M/M/c (solo para estados estables)"""
    rho = calcular_rho(lam, mu, c)
    
    if rho >= 1:
        # Para estados inestables, usar aproximación basada en capacidad promedio
        return float('inf')
    
    a = lam / mu
    
    # Calcular P0
    suma = sum(a**n / math.factorial(n) for n in range(c))
    termino = (a**c) / (math.factorial(c) * (1 - rho))
    P0 = 1 / (suma + termino)
    
    # Calcular Lq
    Lq = (a**c * rho * P0) / (math.factorial(c) * (1 - rho)**2)
    
    # L = Lq + λ/μ
    return Lq + a

def calcular_metricas_ponderadas(lam, mu, pi, c1, c2):
    """
    Calcula ρ, L y W ponderados usando aproximación por capacidad efectiva
    """
    # Capacidad efectiva del sistema
    capacidad_efectiva = (c1 * pi[0] + c2 * pi[1]) * mu
    
    # Verificar estabilidad global
    if lam >= capacidad_efectiva:
        return float('inf'), float('inf'), float('inf')
    
    # Aproximación: tratar como M/M/1 con tasa de servicio efectiva
    rho_efectivo = lam / capacidad_efectiva
    
    # Fórmulas para M/M/1
    L_efectivo = rho_efectivo / (1 - rho_efectivo)
    W_efectivo = L_efectivo / lam
    
    # ρ ponderado (promedio simple)
    rho1 = calcular_rho(lam, mu, c1)
    rho2 = calcular_rho(lam, mu, c2)
    rho_pond = pi[0] * rho1 + pi[1] * rho2
    
    return rho_pond, L_efectivo, W_efectivo