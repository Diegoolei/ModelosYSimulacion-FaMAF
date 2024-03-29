import re
from urllib.request import DataHandler
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
    U = []
    for i in range(np.max(datos) + 1):
        U.append(np.count_nonzero(datos == i))
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
    muestra = np.array(muestra)
    muestra.sort()
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
    H0: Los datos provienen de una distribución binomial de parametros X ~ bin(n=8, p)
    donde p no se conoce
    """
    datos = np.array([6, 7, 3, 4, 7, 3, 7, 2, 6, 3, 7, 8, 2, 1, 3, 5, 8, 7])
    n = 8

    #! En las binomiales, E[X] = n.p como conozco el n, si estimo la esperanza
    #! puedo estimar el p: E[X]/n = p     =>     media_X/n = p_estimada
    esperanza = estimar_esperanza(datos)
    probabilidad_estimada = esperanza/n

    datos.sort()
    frecuencias = np.array(calcular_frecuencias(datos))
    k = len(frecuencias)

    # * FORMA A DE HACER EL EJERCICIO (ESTIMACIÓN)
    #! Calculo las probabilidades que efectivamente corresponden a una binomial
    #! Usando la probabilidad estimada
    probabilidades = np.array(
        list(map(lambda x: masa_binomial(x, n, probabilidad_estimada) * len(datos), list(range(0, k)))))

    T = calcular_T(frecuencias, probabilidades)
    p_valor = p_valor_pearson(T, grados_libertad=k - 1 - 1)

    # -------------------------------------------- #
    # * FORMA B DE HACER EL EJERCICIO (SIMULACION)

    p_valor_sim = 0
    for _ in range(N_sim):
        # Muestra generada a partir de la distribucion con el parametro estimado
        # en la muestra original
        muestra_sim = generar_muestra(
            lambda: generar_binomial(n, probabilidad_estimada), len(datos))

        # Re-estimamos el parametro p pero ahora con esta muestra
        #! media_X/n = p_estimada
        p_sim_est = estimar_esperanza(muestra_sim)/n

        # Calculamos la frecuencia observada en la muestra
        frec_simulada = np.zeros(9)
        for dato in muestra_sim:
            frec_simulada[dato] += 1

        # Calculamos la probabilidad de masa teorica de cada valor posible con el parametro
        # estimado con la muestra de la simulacion
        p_sim = np.array(
            list(map(lambda x: masa_binomial(x, n, p_sim_est)*len(datos), list(range(0, k)))))

        # Calculamos el valor del estadistico de la simulacion
        T_sim = calcular_T(frec_simulada, p_sim)

        #! Comparo con la forma A
        if T_sim > T:
            p_valor_sim += 1

    p_valor_sim = p_valor_sim / N_sim

    #! Print Ejercicio 5

    datos = [[T, p_valor, p_valor_sim]]
    headers = ["Estadistico T", "p-valor por Pearson", "p-valor simulado"]

    print(tabulate(datos, headers, tablefmt="pretty"))


#!NOTE Ejericicio 6
def ej_6():
    """
    Datos Discretos;
    H0: las áreas de la rueda para los distintos premios, numerados del 1 al 10,
    son respectivamente: 31%, 22%, 12%, 10%, 8%, 6%, 4%, 4%, 2% y 1% 
    Tenemos 637 eventos, por lo cual podemos utilizar el Teorema Central del Limite
    Pruebas de Hipótesis para la Proporción poblacional:
    Z = (p_estimado - p_i)/sqrt((p_i - q_i) / n)
    """

    probabilidades = [0.31, 0.22, 0.12, 0.10,
                      0.08, 0.06, 0.04, 0.04, 0.02, 0.01]
    datos = [188, 138, 87, 65, 48, 32, 30, 34, 13, 2]
    k = 10

    #! d) Utilizando una chi cuadrado
    # Estadistico de la muestra original
    T = calcular_T(datos, probabilidades)
    # Tamaño de la muestra original
    n = sum(datos)

    # Estimamos el p-valor
    # Usando la prueba de Pearson
    p_valor = p_valor_pearson(T, grados_libertad=k - 1)

    #! e) Utilizando una simulación
    Nsim = 10**4
    p_valor_sim = estimar_p_valor_pearson(T, Nsim, probabilidades, k, n)

    data = [[p_valor, p_valor_sim, T]]
    headers = ["p-valor Pearson", "p-valor Simulacion", "Estadistico"]

    print(tabulate(data, headers, tablefmt="pretty"))


#! Auxiliar ejercicio 7
def acumulada_exponencial_7(x):
    """
    Acumulada de la distribucion dada en la hipotesis nula (e(1))
    """
    if x < 0:
        return 0
    else:
        Lambda = 1
        return 1 - exp(-Lambda * x)


#!NOTE Ejercicio 7
def ej_7():
    """
    Generar los valores correspondientes a 10 variables aleatorias exponenciales independientes,
    cada una con media 1. Luego, en base al estadístico de prueba de Kolmogorov-Smirnov, aproxime el
    p−valor de la prueba de que los datos realmente provienen de una distribución exponencial con media 1
    """
    exponenciales = generar_muestra(lambda: generar_exp(1), 10)
    D = calcular_D(exponenciales, acumulada_exponencial_7)
    print(D)

    p_valor = estimar_p_valor_k(D, N_sim, 10)

    data = [[D, p_valor]]
    headers = ["D", "p-valor k"]

    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Ejercicio 8
def ej_8():
    pass


#!NOTE Ejercicio 9
def ej_9():
    pass


#!NOTE Ejercicio 10
def ej_10():
    pass


#!NOTE FUNCIONES GENERALES (PROBLEMAS DE DOS MUESTRAS)
def calcular_R(datos_1, datos_2):
    """
    Calcula el valor del estadistico dado en el test de suma de rangos
    Args:
        datos_1:   Primera muestra
        datos_2:   Segunda muestra
    """
    n = len(datos_1)
    m = len(datos_2)
    R = 0

    datos = np.array(datos_1 + datos_2)   # Lista auxiliar
    orden = np.argsort(datos)             # Indices ordenados

    for i in range(n + m):
        if orden[i] < n:
            R += i + 1
    return R


def rangos(n, m, r):
    """
    Formula recursiva para calcular Pn,m(r) = Ph0(R <= r)
    """
    if n == 1 and m == 0:
        if r < 1:
            p = 0
        else:
            p = 1
    elif n == 0 and m == 1:
        if r < 0:
            p = 0
        else:
            p = 1
    else:
        if n == 0:
            p = rangos(0, m-1, r)
        elif m == 0:
            p = rangos(n-1, 0, r-n)
        else:  # n>0, m>0
            p = (n*rangos(n-1, m, r-n-m)+m*rangos(n, m-1, r))/(n+m)
    return p


def p_valor_recursivo(n, m, r):
    """
    Calcula el p_valor usando la formula recursiva Pn,m(r) = Ph0(R <= r)
    Args:
        n:    Cantidad de elementos en la muestra 1
        m:    Cantidad de elementos en la muestra 2
        r:    Rango de la muestra original
    """
    p_valor = 2 * min(rangos(n, m, r), 1 - rangos(n, m, r-1))
    return p_valor


def cdf_z(x):
    """
    Acumulada de la normal estandar
    """
    return erf(x/sqrt(2))/2 + 0.5


def p_valor_normal(n, m, r):
    """
    Calcula el p_valor usando la distribucion normal estandar
    Args:
        n:    Cantidad de elementos en la muestra 1
        m:    Cantidad de elementos en la muestra 2
        r:    Rango de la muestra original
    """
    r_star = (r - n*(n+m+1)/2) / sqrt(n*m*(n+m+1)/12)   # r* de la teoria
    p_valor = 2 * min(cdf_z(r_star), 1 - cdf_z(r_star))
    return p_valor


def estimar_p_valor_r(r, Nsim, n, m):
    """
    Estima el p-valor por medio de simulaciones
    Args:
        r   :   Estadistico R de la muestra original 
        Nsim:   Cantidad de simulaciones a realizar
        n   :   Tamaño de la primera muestra
        m   :   Tamaño de la segunda muestra
    """
    mayor_a_r = 0
    menor_a_r = 0
    aux = list(range(1, n+m+1))   # Arreglo para generar estadisticos
    for _ in range(Nsim):
        aux = permutar(aux)
        r_sim = sum(aux[:n])
        if r_sim >= r:
            mayor_a_r += 1
        if r_sim <= r:
            menor_a_r += 1

    p_valor = 2 * min(mayor_a_r, menor_a_r) / Nsim
    return p_valor


#!NOTE Ejericio 11
def ej_11():
    datos_1 = [65.2, 67.1, 69.4, 78.4, 74.0, 80.3]
    datos_2 = [59.4, 72.1, 68.0, 66.2, 58.5]

    R = calcular_R(datos_1, datos_2)

    #! A) calcular el p-valor exacto (se hace con recursividad)
    p_valor_rec = p_valor_recursivo(len(datos_1), len(datos_2), R)

    #! B) calcular elp−valor aproximado en base a una aproximación normal
    p_valor_nor = p_valor_normal(len(datos_1), len(datos_2), R)

    #! C) Calcular el p−valor aproximado en base a una simulación
    p_valor_sim = estimar_p_valor_r(R, N_sim, len(datos_1), len(datos_2))

    #! Print Ejercicio 11
    data_11 = [[p_valor_rec, p_valor_nor, p_valor_sim]]
    headers_11 = ["p-valor exacto", "p-valor (normal)", "p-valor (simulacion)"]
    print(tabulate(data_11, headers=headers_11, tablefmt="pretty"))


#!NOTE Ejericio 12
def ej_12():
    datos1 = [19, 31, 39, 45, 47, 66, 75]
    datos2 = [28, 36, 44, 49, 52, 72, 72]

    R = calcular_R(datos1, datos2)

    #! A) calcular el p-valor exacto (se hace con recursividad)
    p_valor_rec = p_valor_recursivo(len(datos1), len(datos2), R)

    #! B) calcular el p−valor aproximado en base a una aproximación normal
    p_valor_nor = p_valor_normal(len(datos1), len(datos2), R)

    #! C) calcular el p−valor aproximado en base a una simulacion
    p_valor_sim = estimar_p_valor_r(R, N_sim, len(datos1), len(datos2))

    #! Print Ejercicio 12
    data = [[p_valor_rec, p_valor_nor, p_valor_sim]]
    headers = ["p-valor exacto", "p-valor (normal)", "p-valor (simulacion)"]
    print(tabulate(data, headers, tablefmt="pretty"))


#!NOTE Ejericio 13
def ej_13():
    datos_1 = [39, 40, 38.9, 35, 32, 33, 22.8, 36]    # Primera muestra

    datos_2 = [36.5, 33.1, 35.2, 30, 29, 26, 35.1]  # totobot

    R = calcular_R(datos_1, datos_2)

    #! A) calcular el p-valor exacto (se hace con recursividad)
    p_valor_rec = p_valor_recursivo(len(datos_1), len(datos_2), R)

    #! B) calcular elp−valor aproximado en base a una aproximación normal
    p_valor_nor = p_valor_normal(len(datos_1), len(datos_2), R)

    #! C) Calcular el p−valor aproximado en base a una simulación
    p_valor_sim = estimar_p_valor_r(R, N_sim, len(datos_1), len(datos_2))

    data = [["p-valor (recursivo)", p_valor_rec, p_valor_rec < 0.05],
            ["p-Valor (normal)", p_valor_nor, p_valor_nor < 0.05],
            ["p-valor (simulado)", p_valor_sim, p_valor_sim < 0.05]]

    headers = ["Caso", "Estimacion", "¿Rechazar H0 al 5% de rechazo?"]

    print(tabulate(data, headers=headers, tablefmt="pretty"))

#!NOTE Ejericio 14


def ej_14():
    datos_1 = [141, 132, 154, 142, 143, 150, 134, 140]
    datos_2 = [133, 138, 136, 125, 135, 130, 127, 131, 116, 128]

    R = calcular_R(datos_1, datos_2)

    #! A) calcular el p-valor exacto (se hace con recursividad)
    p_valor_rec = p_valor_recursivo(len(datos_1), len(datos_2), R)

    #! B) calcular elp−valor aproximado en base a una aproximación normal
    p_valor_nor = p_valor_normal(len(datos_1), len(datos_2), R)

    #! C) Calcular el p−valor aproximado en base a una simulación
    p_valor_sim = estimar_p_valor_r(R, N_sim, len(datos_1), len(datos_2))

    data = [["p-valor (recursivo)", p_valor_rec, p_valor_rec < 0.05],
            ["p-Valor (normal)", p_valor_nor, p_valor_nor < 0.05],
            ["p-valor (simulado)", p_valor_sim, p_valor_sim < 0.05]]

    headers = ["Caso", "Estimacion", "¿Rechazar H0 al 5% de rechazo?"]

    print(tabulate(data, headers=headers, tablefmt="pretty"))
