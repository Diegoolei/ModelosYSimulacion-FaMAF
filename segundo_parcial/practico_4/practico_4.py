from random import random
from math import exp, factorial, comb, sqrt
import time
import numpy as np

N_sim = 10000

#!NOTE Funciones generales


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
    for i in range(N):
        U = uniforme_d(i, N-1)     # Numero aleatorio entre [i, N-1]
        a[U], a[i] = a[i], a[U]    # Permutamos un elemento del arreglo
    return a


def estimar_esperanza(generador, N_muestras):
    suma = 0
    for _ in range(N_muestras):
        suma += generador()
    esperanza = suma/N_muestras
    return esperanza


def estimar_varianza(generador, N_muestras):
    """
    Estima el Varianza de una variable aleatoria el estimador de la varianza Sn
    Args:
        M: Cantidad de valores a promediar (tamaño de la muestra)
    """
    MU = estimar_esperanza(generador, N_muestras)
    varianza = 0
    for _ in range(N_muestras):
        varianza += (generador() - MU) ** 2

    varianza = varianza / (N_muestras - 1)
    return varianza


#!NOTE Auxiliares ejercicio 1
def simulacion_1_i(r, iteraciones):
    """
    probabilidad de que  las primeras r cartas sean coincidencias
    Args:
        r:            Numero entero entre 1 y 100
        iteraciones:  Cantidad total de iteraciones de la simulacion
    Return:
        resultado:    Resultado de la simulacion para los parametros dados
    """
    N = 100    # Cantidad de cartas
    cartas_ordenadas = list(range(1, N + 1))
    exitos = 0    # Veces en que el experimento concluyo satisfactoriamente
    for _ in range(iteraciones):
        baraja = permutar(cartas_ordenadas)
        cumple_criterio = True
        for i in range(r):
            if baraja[i] != i + 1:
                cumple_criterio = False
                break
        if cumple_criterio:
            exitos += 1
    resultado = exitos / iteraciones
    return resultado


def simulacion_1_ii(r, iteraciones):
    """
    probabilidad de que haya exactamente r coincidencias
    y estén en las primeras r cartas
    Args:
        r:            Numero entero entre 0 y 100
        iteraciones:  Cantidad total de iteraciones de la simulacion
    Return:
        resultado:    Resultado de la simulacion para los parametros dados
    """
    N = 100       # Cantidad de cartas
    cartas_ordenadas = list(range(1, N + 1))
    exitos = 0    # Veces en que el experimento concluyo satisfactoriamente
    for _ in range(iteraciones):
        baraja = permutar(cartas_ordenadas)
        aciertos = 0
        for i in range(N):
            if baraja[i] == i + 1:
                aciertos += 1
        if aciertos == r:
            exitos += 1

    resultado = exitos / iteraciones
    return resultado


def generar_VA_coincidencias(N):
    """
    Genera la variable aleatoria que cuenta las coincidencias en una baraja
    de N cartas
    Args:
        N: Cantidad total de cartas de la baraja
    """
    baraja = permutar(list(range(1, N+1)))
    coincidencias = 0
    for i in range(N):
        if baraja[i] == i + 1:
            coincidencias += 1
    return coincidencias


def esperanza_1(M, N):
    """
    Estima el valor medio de la variable aleatoria del ejercicio 1 usando la 
    ley fuerte de los grandes numeros
    Args:
        M: Valores a promediar
        N: Tamaño de la baraja
    """
    promedio = 0
    for _ in range(M):
        promedio += generar_VA_coincidencias(N)
    promedio = promedio / M
    return promedio


def varianza_1(M, N):
    """
    Estima la varianza de la variable aleatoria del ejercicio 1 usando un 
    estimador de la varianza
    Args:
        M: Valores a promediar
        N: Tamaño de la baraja
    """
    MU = esperanza_1(10**4, N)
    varianza_estimada = 0
    for _ in range(M):
        varianza_estimada += (generar_VA_coincidencias(N) - MU) ** 2

    return varianza_estimada / (M-1)


#!NOTE Ejercicio 1
def ej_1():
    esperanza_estimada = np.round(esperanza_1(10**4, 100), 2)
    varianza_estimada = np.round(varianza_1(10**4, 100), 2)
    r = 10

    print("------------EJERCICIO 1-------------")
    print("Esperanza estimada =", esperanza_estimada,
          "\nVarianza estimada =", varianza_estimada)

    # Probabilidad de que las primeras r cartas esten ordenadas
    print("\nProbabilidad de que las primeras 10 cartas esten ordenadas")
    for i in range(2, 6):
        print(
            f"Con {10**i} iteraciones la probabilidad es {simulacion_1_i(r, 10**i)}")

    # Probabilidad de obtener exactamente r aciertos
    print("\nProbabilidad de que la baraja tenga exactamente 10 aciertos")
    for i in range(2, 6):
        print(
            "Con {10**i} iteraciones la probabilidad es {simulacion_1_ii(r, 10**i)}")


#!NOTE Auxiliares ejercicio 2
def sim_2(M, N):
    """
    Aproxima la Sumatoria k=1 a N de exp(k/N) usando M valores
    """
    #! A) algoritmo para estimar la cantidad deseada
    # start = time.time()
    suma = 0
    for _ in range(M):
        U = uniforme_d(1, N)
        suma += exp(U/N)
    suma = suma*(N/M)  # ! Aproximo de 1 a N usando solo 100 valores
    # stop = time.time() # Tiempo de ejecución
    return suma


def suma_primerosM(M, N):
    """
    Sumatoria k=1 a N de exp(k/N) para los primeros M valores
    """
    #start = time.time()
    suma = 0
    for i in range(1, M + 1):
        suma += exp(i/N)
    #stop = time.time()
    return suma


#!NOTE Ejercicio 2
def ej_2():
    """
    Sumatoria k=1 a N de exp(k/N)
    """
    #! B) Obtenga la aproximación sorteando 100 números aleatorios
    r = 100
    aproximacion = sim_2(r, N_sim)

    #! C) Obtenga la suma de los 100 primeros numeros
    exacta = suma_primerosM(N_sim, N_sim)

    print("------------EJERCICIO 2-------------")
    print(f"Valor estimado: {round(aproximacion, 4)}")
    print(f"Valor real:     {round(exacta, 4)}")


#!NOTE Auxiliares ejercicio 3
def sim_3():
    """
    Genero dos valores aleatorios entre 1 y 6 inclusive, si el
    valor no se había visto lo guardo un arreglo. Todos los ya 
    vistos estarán en ese arreglo. Aumento el contador y repito
    hasta tener 11 elementos distintos en el arreglo y devuelvo
    el contador.
    """
    resultados_vistos = []
    resultados_distintos = 0
    N = 0
    while resultados_distintos != 11:
        dado_1, dado_2 = uniforme_d(1, 6), uniforme_d(1, 6)
        resultado = dado_1 + dado_2
        if (not resultado in resultados_vistos):
            resultados_vistos.append(resultado)
            resultados_distintos += 1
        N += 1
    return N


def probabilidad_al_menos_X(X, iteraciones):
    """
    Estima la probabilidad de que la variable aleatoria N sea mayor o igual a X
    Args:
        X:            Valor minimo de N
        iteraciones : Cantidad de iteraciones del algoritmo
    """
    estimacion = 0
    for _ in range(iteraciones):
        if (sim_3() >= X):
            estimacion += 1
    return estimacion / iteraciones


#!NOTE Ejercicio 3
def ej_3():
    """
    Simulación tirada de dados
    """
    #! B)
    esperanza = []
    varianza = []
    probabilidad_al_menos_15 = []
    probabilidad_a_lo_sumo_9 = []
    for i in range(1, 3):
        #! i)
        esperanza.append(estimar_esperanza(sim_3, 100**i))
        varianza.append(sqrt(estimar_varianza(sim_3, 100**i)))
        
        
    for i in range(1, 3):
        #! ii)
    
        probabilidad_al_menos_15.append(probabilidad_al_menos_X(15, 100**i))
        probabilidad_a_lo_sumo_9.append(1 - probabilidad_al_menos_X(9, 100**i))

    print("\nEsperanza estimada:")
    print(
        f"simulaciones:valor, 100:{esperanza[0]}, 1000:{esperanza[1]} ")

    print("\ndesviacion estandar estimada:")
    print(
        f"simulaciones:valor, 100:{varianza[0]}, 1000:{varianza[1]} ")

    print("\nProbabilidad al menos 15:")
    print(f"simulaciones:valor, 100:{probabilidad_al_menos_15[0]}, 1000:{probabilidad_al_menos_15[1]}")

    print("\nProbabilidad a lo sumo 9:")
    print(f"simulaciones:valor, 100:{probabilidad_a_lo_sumo_9[0]}, 1000:{probabilidad_a_lo_sumo_9[1]}")

# ej_1()
# ej_2()
# ej_3()