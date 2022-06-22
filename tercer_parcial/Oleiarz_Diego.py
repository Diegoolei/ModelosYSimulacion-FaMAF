from scipy.stats import chi2
from random import random
import numpy as np
from tabulate import tabulate
from math import comb
N_sim = 10000


#!NOTE Funciones auxiliares ejercicio 1
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


def distribucion_f(x):
    if x**2 < 0:
        return 0
    elif x**2 < 1:
        return x**2
    else:
        return 1


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


#!NOTE Ejercicio 1
def Ejercicio_1():
    """
    la muestra proviene de una variable aleatoria
    X con densidad f(x) = 2x en (0,1).
    """
    #! Estimar mediante 10000 simulaciones el p-valor usando muestras de uniformes.
    datos = [0.590, 0.312, 0.665, 0.926, 0.577, 0.505,
             0.615, 0.360, 0.899, 0.779, 0.293, 0.962]

    D = calcular_D(datos, distribucion_f)

    p_valor = estimar_p_valor_k(D, N_sim, len(datos))

    print("---------EJERCICIO 1------------")
    print(f"Estadistico {D}")
    print(f"P-valor {p_valor}")
    print(f"Rechazo hipotesis nula al alfa = 0.1?: {p_valor < 0.1}")


#!NOTE Funciones auxiliares ejercicio 2
def estimar_esperanza(datos):
    return sum(datos)/len(datos)


def masa_binomial(x, n, p):
    """
    Funcion de probabilidad de masa de la distribucion binomial X ~ b(n, p)
    """
    if x < 0:
        return 0
    else:
        return comb(n, x) * (p**x) * (1-p)**(n-x)


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


#!NOTE Ejercicio 2
def Ejercicio_2():
    """
    H0: Los datos provienen de una distribución binomial de parametros X ~ bin(n=8, p)
    donde p no se conoce
    """
    frecuencias = np.array([35, 31, 10, 4, 0])
    n = 80
    n_bin = 8
    #! En las binomiales, E[X] = n.p como conozco el n, si estimo la esperanza
    #! puedo estimar el p: E[X]/n = p     =>     media_X/n = p_estimada
    esperanza = (0*35+1*31+2*10+3*4+4*0)/n
    probabilidad_estimada = esperanza/n_bin
    k = len(frecuencias)

    #! Calculo las probabilidades que efectivamente corresponden a una binomial
    #! Usando la probabilidad estimada
    probabilidades = np.array(
        list(map(lambda x: masa_binomial(x, n_bin, probabilidad_estimada), list(range(0, k)))))
    print(probabilidades)
    T = calcular_T(frecuencias, probabilidades)
    p_valor = p_valor_pearson(T, grados_libertad=k - 1 - 1)

    # -------------------------------------------- #

    p_valor_sim = 0
    for _ in range(N_sim):
        # Muestra generada a partir de la distribucion con el parametro estimado
        # en la muestra original
        muestra_sim = generar_muestra(
            lambda: generar_binomial(8, probabilidad_estimada), n)
        # Re-estimamos el parametro p pero ahora con esta muestra
        p_sim_est = sum(muestra_sim) / len(muestra_sim) / 8
        k_sim = max(muestra_sim)+1
        # Calculamos la frecuencia observada en la muestra
        frec_sim = np.zeros(k_sim)
        for dato in muestra_sim:
            frec_sim[dato] += 1

        # Calculamos la probabilidad de masa teorica de cada valor posible con el parametro
        # estimado con la muestra de la simulacion
        p_sim = np.array(
            list(map(lambda x: masa_binomial(x, 8, p_sim_est), list(range(k_sim)))))
        # Calculamos el valor del estadistico de la simulacion
        t_sim = calcular_T(frec_sim, p_sim)

        if t_sim > T:
            p_valor_sim += 1

        p_valor_sim = p_valor_sim / N_sim

    p_valor_sim = p_valor_sim / N_sim
    print()
    print("---------EJERCICIO 2------------")
    print(f"Probabilidad estim: {probabilidad_estimada}")
    print(f"P-valor por chi2: {p_valor}")
    print(f"P-valor simulado: {p_valor_sim}")
    print(f"Rechazo hipotesis nula al alfa = 0.1? chi2: {p_valor < 0.025}")
    print(f"Rechazo hipotesis nula al alfa = 0.1?: {p_valor_sim < 0.025}")


#!NOTE Funciones auxiliares ejercicio 3
def generar_empirica(datos):
    """
    Genera la variable aleatoria con distribucion empirica para los
    datos dados
    """
    n = len(datos)
    U = int(random() * n)
    return datos[U]


def generar_muestra_bootstrap(data):
    """
    Genera una muestra bootstrap a partir de la distribucion empirica
    de los datos dados
    """
    X = []
    a = len(data)
    for _ in range(a):
        U = int(a * random())
        X.append(data[U])
    X.sort()
    return X


def esperanza_empirica_truncada(datos):
    """
    Calcula la esperanza empirica de los datos dados
    """
    esperanza = sum(datos[1:9]) / len(datos[1:9])
    return esperanza


def media_muestral(datos):
    """
    Calcula la media muestral de los datos dados
    """
    n = len(datos)
    media = sum(datos) / n
    return media


def varianza_empirica(datos):
    """
    Calcula la varianza empirica con la media truncada
    """
    datos_truncados = datos[1:9]
    mu = esperanza_empirica_truncada(datos_truncados)
    varianza_empirica = sum(list(map(lambda x: (x-mu)**2, datos))) / len(datos)
    return varianza_empirica


#!NOTE Ejercicio 3
def Ejercicio_3():
    datos = np.array([2, 4, 6, 7, 11, 21, 81, 90, 105, 121])

    simulaciones = 1000
    varianza_muestral = 0
    datos_generados = []
    for _ in range(simulaciones):
        datos_generados.append(esperanza_empirica_truncada(
            generar_muestra_bootstrap(datos)))

    media_bootstrap = media_muestral(datos_generados)

    for i in datos_generados:
        varianza_muestral += (i - media_bootstrap)**2

    print()
    print("---------EJERCICIO 3------------")
    print(f"Varianza: {varianza_muestral/simulaciones}")


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


#!NOTE Ejercicio 4
def Ejercicio_4():
    datos_1 = [0.778, 0.980, 0.967, 0.843, 0.916,
               0.905, 0.948, 0.971, 0.744, 0.641, 0.978, 0.901]
    datos_2 = [0.762, 0.002, 0.445, 0.722, 0.229, 0.945, 0.902, 0.031]

    R = calcular_R(datos_1, datos_2)

    #! B) calcular el p-valor exacto (se hace con recursividad)
    p_valor_rec = p_valor_recursivo(len(datos_1), len(datos_2), R)
    # Creo que esta bien como lo plantee
    #! C) Calcular el p−valor aproximado en base a una simulación
    p_valor_sim = estimar_p_valor_r(R, N_sim, len(datos_1), len(datos_2))

    data = [["p-valor (recursivo)", p_valor_rec, p_valor_rec < 0.05],
            ["Estadistico R", R],
            ["p-valor (simulado)", p_valor_sim, p_valor_sim < 0.05]]

    headers = ["Caso", "Estimacion", "¿Rechazar H0 al 5% de rechazo?"]
    print()
    print("----------EJERCICIO 4-----------")
    print(tabulate(data, headers=headers, tablefmt="pretty"))


Ejercicio_1()
Ejercicio_2()
Ejercicio_3()
Ejercicio_4()
