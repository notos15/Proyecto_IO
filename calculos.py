import numpy as np
import math
# Pregunta a
def calcular_pi(P):
    """
    Calcula la distribución estacionaria π de una cadena de 2 estados
    usando el sistema clásico de 3 ecuaciones:
        π1 = π1*p11 + π2*p21
        π2 = π1*p12 + π2*p22
        π1 + π2 = 1
    """
    p11, p12 = P[0]
    p21, p22 = P[1]

    # Construir el sistema A * π = b
    # Ecuaciones:
    # π1 - π1*p11 - π2*p21 = 0
    # π2 - π1*p12 - π2*p22 = 0
    # π1 + π2 = 1
    A = np.array([
        [1 - p11,   -p21     ],
        [ -p12,     1 - p22  ],
        [1,          1       ]
    ], dtype=float)
    b = np.array([0, 0, 1], dtype=float)
    # Resolver el sistema lineal
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


