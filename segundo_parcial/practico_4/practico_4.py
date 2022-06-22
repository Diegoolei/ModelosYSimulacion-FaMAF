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


def generar_binomial(N, P):
    """
    Genera un valor de la variable aleatoria binomial usando el metodo de la 
    acumulada inversa
    Args:
        N: Cantidad de ensayos independientes
        P: Probabilidad de exito en el ensayo
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


def generar_binomial_ensayos(N, P):
    """
    Genera un valor de la variable aleatoria binomial usando el metodo de la 
    realizando N ensayos y contando cuantos de ellos fueron exitosos
    Args:
        N: Cantidad de ensayos independientes
        P: Probabilidad de exito en el ensayo
    """
    cantidad_exitos = 0
    for _ in range(N):
        U = random()
        if U < P:
            cantidad_exitos += 1
    return cantidad_exitos


def esperanza_binomial(ensayos, p, N, generador):
    """
    Estima la esperanza de la variable aleatoria binomial usando la ley fuerte
    de los grandes numeros
    Args:
        ensayos   : Parametro de la binomial
        p         : Probabilidad de exito en el ensayo
        N         : Numero de muestras para la estimacion
        generador : Generador de variables aleatorias binomiales
    """
    esperanza = 0
    for _ in range(N):
        esperanza += generador(ensayos, p)
    return esperanza / N


def estimar_p_x_binomial(ensayos, p, N, generador, X):
    """
    Estima la probabilidad de que la variable aleatoria binomial
    B(ensayos, p) tome el valor X
    Args:
        ensayos     : Parametro de la binomial (cantidad de ensayos independientes)
        p           : Probabilidad de exito del ensayo de la binomial
        N           : Cantidad de simulaciones a realizar
        generador   : Generador de variables aleatorias binomiales
        X           : Valor de la binomial de interes
    """
    p_x = 0
    for _ in range(N):
        B = generador(ensayos, p)
        if B == X:
            p_x += 1
    return p_x / N


def acumulada_poisson(Lambda, k):
    """
    Calcula la acumulada de la variable de poisson X de parametro Lambda
    Return:
        p(X <= k) 
    """
    p = exp(-Lambda)
    F = p
    for i in range(1, k + 1):
        p *= Lambda / i
        F += p
    return F


def poisson_TI(Lambda):
    """
    Genera una variable aleatoria de Poisson de parametro Lambda usando
    el metodo de la transformada inversa
    Args:
        Lambda: Parametro de la poisson a generar
    """
    U = random()
    i, p = 0, exp(-Lambda)
    F = p
    while U >= F:
        i += 1
        p *= Lambda / i
        F = F + p
    return i


def poisson_TI_optimizado(Lambda):
    """
    Genera una variable aleatoria de Poisson de parametro Lambda usando
    el metodo de la transformada inversa con una pequeña optimizacion
    Args:
        Lambda: Parametro de la poisson a generar
    """
    p = exp(-Lambda)
    F = p
    for j in range(1, int(Lambda) + 1):
        p *= Lambda / j
        F += p
    U = random()
    if U >= F:
        j = int(Lambda) + 1
        while U >= F:
            p *= Lambda / j
            F += p
            j += 1
        return j-1
    else:
        j = int(Lambda)
        while U < F:
            F -= p
            p *= j / Lambda
            j -= 1
        return j + 1


def geometrica_TI(p_exito):
    """
    Genera una variable aleatoria geometrica usando el metodo de la transformada
    inversa
    Args:
        p_exito: Parametro de la v.a. geometrica
    """
    p = p_exito
    F, i = p, 1
    U = random()
    while U > F:
        p *= 1 - p_exito
        F += p
        i += 1
    return i

def geometrica_SIM(p_exito):
    """
    Genera una variable aleatoria geometrica generando ensayos hasta que uno sea
    exitoso
    Args:
        p_exito: Parametro de la v.a. geometrica
    """
    i = 1
    while(True):
        U = random()
        if U < p_exito:
            return i
        i += 1


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
        # Desviacion estandar = raiz(varianza)
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
    print(
        f"simulaciones:valor, 100:{probabilidad_al_menos_15[0]}, 1000:{probabilidad_al_menos_15[1]}")

    print("\nProbabilidad a lo sumo 9:")
    print(
        f"simulaciones:valor, 100:{probabilidad_a_lo_sumo_9[0]}, 1000:{probabilidad_a_lo_sumo_9[1]}")


#!NOTE Auxiliares ejercicio 4
def simular_4_TI():
    """
    Genera un valor de la variable aleatoria del ejercicio 4 usando el metodo de
    la Transformada inversa
    """
    U = random()
    if (U < 0.35):
        return 3
    elif (U < 0.55):
        return 1
    elif (U < 0.75):
        return 4
    elif (U < 0.90):
        return 0
    else:
        return 2


def simular_4_AYR():
    """
    Genera un valor de la variable aleatoria del ejercicio 4 usando el metodo de 
    Aceptacion y rechazo
    """
    N, p = 4, 0.45
    p_x = [0.15, 0.20, 0.10, 0.35, 0.20]
    p_y = [0.09150625, 0.299475, 0.3675375, 0.200475, 0.04100625]
    c = 4.877305288827923  # Calculado previamente
    while(1):
        U = random()
        Y = generar_binomial(N, p)
        if (U < p_x[Y] / (p_y[Y] * c)):
            return Y


#!NOTE Ejercicio 4
def ej_4():
    N = 10**5
    # Tiempo del metodo de la transformada inversa
    tiempo_transformada_inv = time.time()
    for _ in range(N):
        simular_4_TI()
    tiempo_transformada_inv = np.round(
        (time.time() - tiempo_transformada_inv) * 1000, 2)     # en ms

    # Tiempo del metodo de aceptacion y rechazo
    tiempo_aceptacion_rechazo = time.time()
    for _ in range(N):
        simular_4_AYR()
    tiempo_aceptacion_rechazo = np.round(
        (time.time() - tiempo_aceptacion_rechazo) * 1000, 2)  # en ms

    print("""
    Tiempo requerido por el metodo de la transformada inversa: {} ms
    Tiempo requerido por el metodo de aceptacion y rechazo   : {} ms
    """.format(tiempo_transformada_inv, tiempo_aceptacion_rechazo))


#!NOTE Auxiliares ejercicio 5
def ejercicio_5_AYR():
    """
    Genera un valor de la variable aleatoria del ejercicio 5 usando el
    metodo de aceptacion y rechazo con la v.a. Y (Y ~ U [1, 10])
    """
    C = 1.4    # Calculado analiticamente
    p_y = 1/10   # Probabilidad de la uniforme Y
    p_x = [0.11, 0.14, 0.09, 0.08, 0.12, 0.10, 0.09, 0.07, 0.11, 0.09]
    while(1):
        U = random()
        Y = uniforme_d(1, 10)
        if (U < p_x[Y - 1] / (C * p_y)):
            return Y


def ejercicio_5_TI():
    """
    Genera un valor de la variable aleatoria del ejercicio 5 usando el
    metodo de la transformada inversa
    """
    p_x = [0.11, 0.14, 0.09, 0.08, 0.12, 0.10, 0.09, 0.07, 0.11, 0.09]
    U = random()
    F = p_x[0]
    i = 1
    while U > F:
        F += p_x[i]
        i += 1
    return i


def ejercicio_5_URNA(urna):
    """
    Genera un valor de la variable aleatoria del ejercicio 5 usando el
    metodo de la urna con K = 100
    """
    U = uniforme_d(0, 99)
    return urna[U]

#!NOTE Ejercicio 5


def ej_5():
    distribucion_urna = np.array(
        [0.11, 0.14, 0.09, 0.08, 0.12, 0.10, 0.09, 0.07, 0.11, 0.09]) * 100
    distribucion_urna = np.array(distribucion_urna, dtype=int)
    urna = []
    for i in range(10):
        for _ in range(distribucion_urna[i]):
            urna.append(i+1)

    # Tiempo del metodo de aceptacion y rechazo
    tiempo_5_AYR = time.time()
    for _ in range(10**4):
        ejercicio_5_AYR()
    tiempo_5_AYR = np.round((time.time() - tiempo_5_AYR)
                            * 10**3, 4)    # Tiempo en ms

    # Tiempo del metodo de la transformada inversa
    tiempo_5_TI = time.time()
    for _ in range(10**4):
        ejercicio_5_TI()
    tiempo_5_TI = np.round((time.time() - tiempo_5_TI)
                           * 10**3, 4)      # Tiempo en ms

    # Tiempo del metodo de la urna
    tiempo_5_URNA = time.time()
    for _ in range(10**4):
        ejercicio_5_URNA()
    tiempo_5_URNA = np.round(
        (time.time() - tiempo_5_URNA) * 10**3, 4)  # Tiempo en ms

    print("""
    Tiempo requerido por el metodo de la transformada inversa: {} ms
    Tiempo requerido por el metodo de aceptacion y rechazo   : {} ms
    Tiempo requerido por el metodo de la urna                : {} ms
    """.format(tiempo_5_TI, tiempo_5_AYR, tiempo_5_URNA))


#!NOTE Ejercicio 6
def ej_6():
    n, p = 10, 0.3

    # Tiempo de la transformada inversa
    time_6_TI = time.time()
    for _ in range(10**6):
        generar_binomial(n, p)
    time_6_TI = np.round((time.time() - time_6_TI) * 10**3, 4)  # Tiempo en ms

    # Tiempo de la binomial simulada
    time_6_SIM = time.time()
    for _ in range(10**6):
        generar_binomial_ensayos(n, p)
    time_6_SIM = np.round((time.time() - time_6_SIM)
                          * 10**3, 4)  # Tiempo en ms

    print("""
    Tiempo requerido por el metodo de la transformada inversa: {} ms
    Tiempo requerido por el metodo de simulacion             : {} ms
    """.format(time_6_TI, time_6_SIM))

    esperanza_TI = esperanza_binomial(ensayos=10, p=0.3, N=10**6,
                                      generador=generar_binomial)
    esperanza_SIM = esperanza_binomial(ensayos=10, p=0.3, N=10**6,
                                       generador=generar_binomial_ensayos)

    p_b_0_TI = estimar_p_x_binomial(ensayos=10, p=0.3, N=10**6,
                                    generador=generar_binomial, X=0)
    p_b_10_TI = estimar_p_x_binomial(ensayos=10, p=0.3, N=10**6,
                                     generador=generar_binomial, X=10)
    p_b_0_SIM = estimar_p_x_binomial(ensayos=10, p=0.3, N=10**6,
                                     generador=generar_binomial_ensayos, X=0)
    p_b_10_SIM = estimar_p_x_binomial(ensayos=10, p=0.3, N=10**6,
                                      generador=generar_binomial_ensayos, X=10)
    print("Esperanza obtenida usando transformada inversa:", esperanza_TI,
          "\nEsperanza obtenida usando simulacion:", esperanza_SIM,)

    print("""
    Probabilidad    Metodo T.I       Metodo SIM
    P(X = 0)      {}         {}
    P(X = 10)     {}            {}
    """.format(p_b_0_TI, p_b_0_SIM, p_b_10_TI, p_b_10_SIM))


#!NOTE Ejercicio 7
def ej_7():
    Lambda = 0.7
    iteraciones = 10**3

    # Tiempo de la poisson con Transformada inversa sin optimizar
    time_TI = time.time()
    p_y_TI = [0, 0, 0]
    for _ in range(iteraciones):
        Y = poisson_TI(Lambda)
        if (Y in [0, 1, 2]):
            p_y_TI[Y] = p_y_TI[Y] + 1

    resultado_TI = np.round(1 - sum(np.array(p_y_TI) / iteraciones), 3)
    time_TI = np.round((time.time() - time_TI) * 10**3, 4)

    # Tiempo de la poisson con Transformada inversa optimizada
    time_TI_o = time.time()
    p_y_TI_o = [0, 0, 0]
    for _ in range(iteraciones):
        Y = poisson_TI_optimizado(Lambda)
        if (Y in [0, 1, 2]):
            p_y_TI_o[Y] = p_y_TI_o[Y] + 1
    resultado_TI_o = np.round(1 - sum(np.array(p_y_TI_o) / iteraciones), 3)
    time_TI_o = np.round((time.time() - time_TI_o) * 10**3, 4)

    print("""
    Estimacion de P(Y > 2):
    Usando transformada inversa sin optimizar: {} en {} ms
    Usando transformada inversa optimizada   : {} en {} ms
    """.format(resultado_TI, time_TI, resultado_TI_o, time_TI_o))


#!NOTE Auxiliares ejercicio 8
def generar_8_TI(Lambda, k):
    """
    Genera la variable aleatoria descrita en el enunciado del ejercicio 8
    usando el metodo de la transformada inversa
    Args:
        Lambda: Parametro Lambda de la variable
        k     : Terminos antes de truncar la acumulada de poisson
    """
    p = exp(-Lambda) / acumulada_poisson(Lambda, k)
    F = p
    i = 0
    U = random()
    while U > F:
        i += 1
        p *= Lambda / i
        F += p
    return i

def generar_8_AYR(Lambda, k):
    """
    Genera la variable aleatoria descrita en el enunciado del ejercicio 8
    usando el metodo de aceptacion y rechazo por medio de la v.a. uniforme
    Y ~ U[0, k]
    Args:
        Lambda: Parametro Lambda de la variable
        k     : Terminos antes de truncar la acumulada de poisson
    """
    
    # Como la va del ejercicio 8 es una poisson dividida una constante
    # la maxima probabilidad se optiene en X = int(Lambda) por lo cual puedo 
    # calcular C del metodo de aceptacion y rechazo facilmente
    
    F_k    = acumulada_poisson(Lambda, k)
    masa_x = lambda x: exp(-Lambda) * Lambda ** int(x) / factorial(int(x)) / F_k 
    C      = masa_x(Lambda) / (1 / (k + 1))   # Probabilidad de la uniforme en Lambda
    
    while(True):
        U = random()
        Y = uniforme_d(0, k)
        if U < masa_x(Y) / (C / (k + 1)):
            return Y


#!NOTE Ejercicio 8
def ej_8():
    # Calculo el valor real de P(X > 2) = 1 - F(2)
    Lambda, k, repeticiones = 0.7, 10, 1000
    F_k = acumulada_poisson(Lambda, k)
    f_8 = lambda x: exp(-Lambda) * Lambda ** x / factorial(x) / F_k
    F_2_real = 1 - (f_8(0) + f_8(1) + f_8(2))


    # Calculo el valor estimado de P(X > 2) usando el metodo de la transformada inversa
    p_x = np.array([0, 0, 0])    # p(0), p(1), p(2)
    for _ in range(repeticiones):
        X = generar_8_TI(Lambda, k)
        if(X in [0, 1, 2]):
            p_x[X] += 1
    p_x = p_x / repeticiones
    F_2_TI = 1 - sum(p_x)

    # Calculo el valor estimado de P(X > 2) usando el metodo de aceptacion y rechazo
    p_x = np.array([0, 0, 0])
    for _ in range(repeticiones):
        X = generar_8_AYR(Lambda, k)
        if(X in [0, 1, 2]):
            p_x[X] += 1
    p_x = p_x / repeticiones
    F_2_AYR = 1 - sum(p_x)

    print("""
    Valor de P(X > 2) real                        {}
    Valor de P(X > 2) usando transformada inversa {}
    Valor de P(X > 2) usando aceptacion y rechazo {}
    """.format(F_2_real, F_2_TI, F_2_AYR))


#!NOTE Auxiliares ejercicio 9
def ejercicio_9():
    """
    Genera la variable aleatoria descrita en el ejercicio 9 usando el metodo
    de la transformada inversa
    """
    # Arreglos necesarios para hacer programacion dinamica y ahorrar tiempo de computo
    multiplo  = np.array([1/2, 2, 3])
    potencias = np.array([1/4, 1, 3])
    i = 1
    F = potencias[0] + potencias[1] / 2 / potencias[2]
    U = random()
    while U > F:
        i += 1
        potencias *= multiplo
        F += potencias[0] + potencias[1] / 2 / potencias[2]
    return i


#!NOTE Ejercicio 9
def ej_9():
    # Estimacion de la esperanza usando la ley fuerte de los grandes numeros
    esperanza_estimada = 0
    iteraciones = 10**3
    for _ in range(iteraciones):
        esperanza_estimada += ejercicio_9()
    esperanza_estimada = esperanza_estimada / iteraciones
    print("Esperanza estimada =", esperanza_estimada)


#!NOTE Ejercicio 10
def ej_10():
    # p = 0.8
    iteraciones = 10**5
    p = 0.8

    # Esperanza para el algoritmo de transformada inversa
    time_10_TI_0_8      = time.time()
    esperanza_10_TI_0_8 = 0
    for _ in range(iteraciones):
        esperanza_10_TI_0_8 += geometrica_TI(p)
    esperanza_10_TI_0_8 = esperanza_10_TI_0_8 / iteraciones
    time_10_TI_0_8      = np.round((time.time() - time_10_TI_0_8) * 10**3, 4)    # en ms

    # Esperanza para el algoritmo de simulacion
    time_10_SIM_0_8      = time.time()
    esperanza_10_SIM_0_8 = 0
    for _ in range(iteraciones):
        esperanza_10_SIM_0_8 += geometrica_SIM(p)
    esperanza_10_SIM_0_8 = esperanza_10_SIM_0_8 / iteraciones
    time_10_SIM_0_8      = np.round((time.time() - time_10_SIM_0_8) * 10**3, 4)    # en ms

    # p = 0.2
    p = 0.2

    # Esperanza para el algoritmo de transformada inversa
    time_10_TI_0_2      = time.time()
    esperanza_10_TI_0_2 = 0
    for _ in range(iteraciones):
        esperanza_10_TI_0_2 += geometrica_TI(p)
    esperanza_10_TI_0_2 = esperanza_10_TI_0_2 / iteraciones
    time_10_TI_0_2      = np.round((time.time() - time_10_TI_0_2) * 10**3, 4)    # en ms

    # Esperanza para el algoritmo de simulacion
    time_10_SIM_0_2      = time.time()
    esperanza_10_SIM_0_2 = 0
    for _ in range(iteraciones):
        esperanza_10_SIM_0_2 += geometrica_SIM(p)
    esperanza_10_SIM_0_2 = esperanza_10_SIM_0_2 / iteraciones
    time_10_SIM_0_2      = np.round((time.time() - time_10_SIM_0_2) * 10**3, 4)    # en ms

    print("""
        Algoritmo        P        Esperanza          Tiempo
        TI           0.2        {}         {} ms              
        SIM           0.2        {}         {} ms
        TI           0.8        {}         {} ms
        SIM           0.8        {}         {} ms
    """.format(esperanza_10_TI_0_2, time_10_TI_0_2, esperanza_10_SIM_0_2, time_10_SIM_0_2,
            esperanza_10_TI_0_8, time_10_TI_0_8, esperanza_10_SIM_0_8, time_10_SIM_0_8))
