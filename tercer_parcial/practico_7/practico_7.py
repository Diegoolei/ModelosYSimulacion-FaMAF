import re
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


def estimar_esperanza(datos):
    return sum(datos)/len(datos)


def calcular_frecuencias(datos):
    """
    la lista tiene que estar ordenada
    """
    print(datos)
    U = []
    count = 1
    for i in range():
        if datos[i-1] == datos[i]:
            count += 1
        else:
            U.append(count)
            count = 1
    U.append(count)
    print(U)
    return U


#!NOTE Funciones Generales (Tests para datos discretos)
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


def p_valor_pearson(T, grados_libertad):
    """
    Calcula el p-valor usando los resultados teoricos que dictan:
    Ph0(T >= t) = P(X_k-1 >= t)
    Args:
        t              :    Resultado del estadistico en la muestra
        grados_libertad:    Grados de libertad de la variable chi-cuadrada
    """
    acumulada_chi = chi2.cdf(T, grados_libertad)
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


def estimar_p_valor_pearson(T, Nsim, p, k, n):
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
        Nsim = generar_frecuencia_observada(n, p, k)
        # Estadistico de la simulacion
        t_sim = calcular_T(Nsim, p)
        if t_sim >= T:
            p_valor += 1
    return p_valor / Nsim


def masa_binomial(x, n, p):
    """
    Funcion de probabilidad de masa de la distribucion binomial X ~ b(n, p)
    """
    if x < 0:
        return 0
    else:
        return comb(n, x) * (p**x) * (1-p)**(n-x)


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
    probabilidades = np.array([1/4, 1/2, 1/4])
    muestras = np.array([141, 291, 132])  # Frecuencia observada.
    n = sum(muestras)  # Tamaño de la muestra
    # Valor del estadisctico en la muestra
    T = calcular_T(muestras, probabilidades)

    # Cantidad de valores posibles de la muestra (dado por H0)
    k = 3
    # Aproximo el p-valor
    # Usando la prueba de pearson
    p_valor_1 = p_valor_pearson(T, grados_libertad=k - 1)

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
    probabilidad = np.array([1/6]*6)
    muestras = np.array([158, 172, 164, 181, 160, 165])
    T = calcular_T(muestras, probabilidad)
    p_valor = p_valor_pearson(T, len(muestras) - 1)

    #! B)
    p_valor_estimado = estimar_p_valor_pearson(
        T, N_sim, probabilidad, len(muestras), sum(muestras))

    #! Print ejercicio 2
    data = [[p_valor, p_valor_estimado]]
    headers = ["P-valor Pearson", "P-valor simulacion"]
    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Funciones Generales (Tests para datos Continuos)
def calcular_D(muestra, acumulada_h):
    """
    Calcula el estadistico dado en el test de Kolmogorov-Smirnov
    Args:
        muestra    :    Muestra original de datos
        acumulada_h:    Acumulada de la distribucion de la hipotesis nula
    """

    n = len(muestra)
    # Vectores_auxiliares
    F = np.array(list(map(acumulada_h, muestra)))
    j = np.array(list(range(1, n+1))) / n
    j_1 = np.array(list(range(n))) / n

    #  max      {(j/n) - F(muestra[j])}
    # 1<=j<=n
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


def acumulada_exp(x, lam=1/50):
    """
    Acumulada de la distribucion exponencial (exp(l))
    """
    if x < 0:
        return 0
    else:
        return 1 - exp(-x*lam)


def estimar_p_valor_k(d, Nsim, n):
    """
    Test de Kolmogorov-smirnov
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
        # D generado con los datos simulados
        d_sim = calcular_D(muestra_sim, acumulada_uniforme)
        if d_sim >= d:
            p_valor += 1
    return p_valor / Nsim


#!NOTE Ejercicio 3
def ej_3():
    """
    H0: Los  siguientes  10  números  son aleatorios:
    """
    datos = [0.12, 0.18, 0.06, 0.33, 0.72, 0.83, 0.36, 0.27, 0.77, 0.74]
    # Los datos tienen que estar ordenados
    datos.sort()
    # D generado con los datos a comparar
    d = calcular_D(datos, acumulada_uniforme)  # Valor del estadistico

    # Estimamos el p-valor usando simulaciones
    p_valor = estimar_p_valor_k(d, N_sim, len(datos))

    #! Print Ejercicio 3
    data = [[p_valor, d]]
    headers = ["p-valor estimado", "Estadistico"]

    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Ejercicio 4
def ej_4():
    """
    Los siguientes 13 valores provienende una distribución exponencial con media 50
    exp(1/50)
    calcular el p-valor para una continua
    """
    datos = [86, 133, 75, 22, 11, 144, 78, 122, 8, 146, 33, 41, 99]
    datos.sort()

    D = calcular_D(datos, acumulada_exp)
    #!!!! Si el p-valor es muy chico (comparar con el nivel de rechazo), hay evidencia
    #!!!! Suficiente para rechazar la hipótesis nula (H0), caso contrario no hay evidencia
    #!!!! suficiente
    p_valor = estimar_p_valor_k(D, N_sim, len(datos))

    #! Print Ejercicio 4
    data = [[p_valor, D]]
    headers = ["p-valor estimado", "Estadistico"]

    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Ejercicio 5
def ej_5():
    """
    Distribución binomial con parámetros(n=8, p), donde p no se conoce
    """
    datos = np.array([6, 7, 3, 4, 7, 3, 7, 2, 6, 3, 7, 8, 2, 1, 3, 5, 8, 7])
    datos.sort()
    frecuencias = np.array([0, 1, 2, 4, 1, 1, 2, 5, 2])
    k = 9
    n = 8
    
    #! En las binomiales la esperanza es n.p, como conozco el n si calculo 
    #! la esperanza, puedo calcular el p
    esperanza = estimar_esperanza(datos)
    p_estimado = esperanza/n

    probabilidades = np.array(list(map(lambda x: masa_binomial(x, n, p_estimado), list(range(0, 9)))))

    T = calcular_T(frecuencias, probabilidades)
    p_valor = p_valor_pearson(T, grados_libertad = k - 2)  

    p_valor_sim = 0
    for _ in range(N_sim):
        # Muestra generada a partir de la distribucion con el parametro estimado
        # en la muestra original
        muestra_sim = generar_muestra(lambda: generar_binomial(8, p_estimado), n)
        
        # Re-estimamos el parametro p pero ahora con esta muestra
        p_sim_est = sum(muestra_sim) / len(muestra_sim) / 8
        
        # Calculamos la frecuencia observada en la muestra
        Nsim = np.zeros(9)
        for dato in muestra_sim:
            Nsim[dato] += 1
            
        # Calculamos la probabilidad de masa teorica de cada valor posible con el parametro
        # estimado con la muestra de la simulacion
        p_sim = np.array(list(map(lambda x: masa_binomial(x, n, p_sim_est), list(range(0, 9)))))
        # Calculamos el valor del estadistico de la simulacion
        t_sim = calcular_T(Nsim, p_sim)

        if t_sim > T:
            p_valor_sim += 1
            
    p_valor_sim = p_valor_sim / N_sim

    datos   = [[T, p_valor, p_valor_sim]]
    headers = ["Estadistico T", "p-valor por Pearson", "p-valor simulado"]

    print(tabulate(datos, headers, tablefmt="pretty"))
