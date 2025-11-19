import numpy as np
import math
# Pregunta a
def calcular_pi(P):
    """
    Calcula la distribución estacionaria π para una matriz de transición P.
    P debe ser una matriz cuadrada (lista de listas o np.array).
    Retorna un vector numpy con las probabilidades estacionarias.
    """
    P = np.array(P, dtype=float)
    n = P.shape[0]

    # Ecuación: πP = π  →  (Pᵗ - I)ᵗ π = 0  →  (Pᵗ - I)π = 0
    # Añadimos la restricción sum(π)=1 para resolver el sistema lineal
    A = np.transpose(P) - np.eye(n)
    A = np.vstack([A, np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1  # condición de normalización

    # Resolver el sistema
    pi = np.linalg.lstsq(A, b, rcond=None)[0]
    return pi
#-----------------------------------------------------------------------------------

# Pregunta b
# Calcular P
def calcular_intensidades(lam, mu, c):
    """
    Calcula las intensidades de tráfico por estado:
    p0 = λ / (c0 * μ)
    """
    p0 = lam / (c * mu)
    
    return p0

# Calcular L
def calcular_clientes(lam,mu,p,c):
    a=lam/mu
    # Suma Σ (a^n / n!) desde n = 0 hasta c-1
    suma = sum((a**n) / math.factorial(n) for n in range(c))
    
    # Término adicional: a^c / (c! * (1 - rho1))
    termino = (a**c) / (math.factorial(c) * (1 - p))
    
    # Inversa
    P0 = 1 / (suma + termino)

    # Calcular Lq
    Lq = ((a**c) * p) / (math.factorial(c) * ((1 - p)**2))
    Lq *= P0

    return (Lq+a)


# Calcular W

#-----------------------------------------------------------------------------------
#pregunta 3