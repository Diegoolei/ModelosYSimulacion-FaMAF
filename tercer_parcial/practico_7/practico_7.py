import numpy as np
from scipy.stats import chi2
from random import random, gauss, gammavariate
from tabulate import tabulate
from math import exp, comb, log, sqrt, erf

N_sim = 10000

#!NOTE Funciones Generales
def generar_muestra(generador, n):
    """
    Genera una muestra de tamaño n de una variable aleatoria
    Args:
        generador:    Generador de la variable aleatoria
        n        :    Tamaño de la muestra
    """
    datos = []
    for _ in range(n):
        datos.append(generador())
    return datos


def generar_binomial(N, P):
    """
    Genera un valor de la variable aleatoria binomial usando el metodo de la 
    transformada inversa
    Args:
        N: Cantidad de ensayos independientes
        P: Probabilidad de exito de ensayo
    """
    prob = (1 - P) ** N
    c = P / (1 - P)
    F = prob
    i = 0
    U = random()
    while U >= F:
        prob *= c * (N-i) / (i+1)
        F += prob
        i += 1
    return i


def generar_exp(Lambda):
    """
    Genera una variable aleatoria exponencial usando el metodo de la transformada
    inversa
    Args:
        Lambda: Parametro de la variable aleatoria exponencial
    """
    U = random()
    return -log(U) / Lambda


def uniforme_d(n, m):
    """
    Genera numeros aleatorios entre n y m (inclusive) 
    """
    U = int(random() * (m - n + 1))  # 0 <= U < (m-n+1) Equivale a 0 <= U <= (m-n)
    U = U + n                        # Equivale a n <= U <= m
    return U


def permutar(a):
    """
    Permuta el arreglo a
    args: 
        a: Arreglo a permutar
    return:
        a_p: Arreglo permutado
    """
    N = len(a)
    a_p = a.copy()
    for i in range(N):
        U = uniforme_d(i, N-1)             # Numero aleatorio entre [i, N-1]
        a_p[U], a_p[i] = a_p[i], a_p[U]    # Permutamos un elemento del arreglo
    return a_p


#! Funciones Generales (Tests para datos discretos)
def calcular_T(N, p):
    """
    Calcula el estadistico T dado en el test chi-cuadrado de 
    Pearson.
    ¡Ambas entradas deben estar ordenadas de menor a mayor respecto
    al valor de variable aleatoria al que hacen referencia!
    Args:
        N:    Frecuencia observada de la muestra
        p:    Probabilidad de los valores posibles de la variable aleatoria
    """
    n = sum(N)    # Tamaño de la muestra
    T = sum((N - n*p)**2 / (n*p))
    return T


def p_valor_pearson(t, grados_libertad):
    """
    Calcula el p-valor usando los resultados teoricos que dictan:
    Ph0(T >= t) = P(X_k-1 >= t)
    Args:
        t              :    Resultado del estadistico en la muestra
        grados_libertad:    Grados de libertad de la variable chi-cuadrada
    """
    acumulada_chi = chi2.cdf(t, grados_libertad)
    # Calcula P(chi_(3-1) <= T) entonces hacemos 1 - para invertirlo
    p_valor = 1 - acumulada_chi
    return p_valor


def generar_frecuencia_observada(n, p_masa, k):
    """
    Genera la frecuencia observada usando una variable aleatoria binomial
    Args:
        n     :   Tamaño de la muestra
        p_masa:   Probabilidad masa de los valores posibles de la distribucion 
                  de la hipotesis nula
        k     :   Cantidad total de valores posibles de la variable con distribucion
                  dada en la hipotesis nula
    """
    N = np.zeros(k)
    N[0] = generar_binomial(n, p_masa[0])
    for i in range(1, k-1):
        N[i] = generar_binomial(
            n - sum(N[:i]), p_masa[i] / (1 - sum(p_masa[:i])))
    N[k-1] = n - sum(N[:k-1])
    return np.array(N)


def estimar_p_valor_pearson(t, Nsim, p, k, n):
    """
    Estima el p_valor por medio de una simulacion P(T >= t)
    Args:
        t   :   Valor del estadistico en la muestra original
        Nsim:   Cantidad de simulaciones a realizar
        p   :   Probabilidad masa de los valores posibles de la distribucion 
                de la hipotesis nula
        k   :   Cantidad total de valores posibles de la variable con distribucion
                dada en la hipotesis nula
        n   :   Tamaño de la muestra original
    """
    p_valor = 0
    for _ in range(Nsim):
        # Frecuencia observada en la simulacion
        N_sim = generar_frecuencia_observada(n, p, k)
        # Estadistico de la simulacion
        t_sim = calcular_T(N_sim, p)
        if t_sim >= t:
            p_valor += 1
    return p_valor / Nsim


def estimar_p_valor_k(d, Nsim, n):
    """
    Estima el p-valor por medio de simulacion P(D >= d)
    args:
        d   :    Valor del estadistico en la muestra original
        Nsim:    Cantidad de simulaciones a realizar
        n   :    Tamaño de la muestra original
    """
    p_valor = 0
    for _ in range(Nsim):
        muestra_sim = generar_muestra(random, n)    # Muestra de uniformes
        muestra_sim.sort()
        d_sim = calcular_D(muestra_sim, acumulada_uniforme)
        if d_sim >= d:
            p_valor += 1
    return p_valor / Nsim


#!NOTE Ejercicio 1
def ej_1():
    #! A)
    # Datos de la muestra
    # Mapeamos a cada flor con un valor discreto asi podemos modelarla con una variable
    # aleatoria
    # Flor Blanca ----> 0
    # Flor Rosa   ----> 1
    # Flor Roja   ----> 2 
    # Masa de nuestra distribucion de la hipotesis nula.
    probabilidades = [1/4, 1/2, 1/4]
    muestras = [141, 291, 132] # Frecuencia observada.
    n = sum(muestras) # Tamaño de la muestra
    T = calcular_T(muestras, probabilidades) # Valor del estadisctico en la muestra

    # Cantidad de valores posibles de la muestra (dado por H0)
    k = 3
    print(muestras)
    # Aproximo el p-valor
    # Usando la prueba de pearson
    p_valor_1 = p_valor_pearson(T, grados_libertad = k - 1)

    #! B)
    # Usando una simulacion
    p_valor_est_1 = estimar_p_valor_pearson(T, N_sim, probabilidades, k, n)

    #! Print ejercicio 1
    data = [[p_valor_1, p_valor_est_1]]
    headers = ["P-valor Pearson", "P-valor simulacion"]
    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Ejercicio 2
def ej_2():
    #! A)
    probabilidad = 1/6
    muestras = [158, 172, 164, 181, 160, 165]
    T = calcular_T(muestras, probabilidad)
    p_valor = p_valor_pearson(T, len(muestras) - 1)

    #! B)
    p_valor_estimado = estimar_p_valor_pearson(T, N_sim, probabilidad, len(muestras), sum(muestras))

    #! Print ejercicio 2
    data = [[p_valor, p_valor_estimado]]
    headers = ["P-valor Pearson", "P-valor simulacion"]
    print(tabulate(data, headers, tablefmt="pretty"))



#! Funciones Generales (Tests para datos Continuos)
def calcular_D(muestra, acumulada_h):
    """
    Calcula el estadistico dado en el test de Kolmogorov-Smirnov
    Args:
        muestra    :    Muestra original de datos
        acumulada_h:    Acumulada de la distribucion de la hipotesis nula
    """
    n = len(muestra)
    m_copy = list.copy(muestra)
    m_copy.sort()
    m_copy = np.array(m_copy)

    # Vectores_auxiliares
    F = np.array(list(map(acumulada_h, m_copy)))
    j = np.array(list(range(1, n+1))) / n
    j_1 = j - 1/n

    m1 = max(j - F)
    m2 = max(F - j_1)
    D = max(m1, m2)
    return D


def acumulada_uniforme(x):
    """
    Acumulada de la distribucion uniforme (U(0, 1))
    """
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1
