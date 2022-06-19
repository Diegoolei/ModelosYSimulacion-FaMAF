from random import random
from tabulate import tabulate
from time import time
from math import log, e, sqrt, exp, sin, pi


N_sim = 10000


#!NOTE Funciones Generales
def estimar_esperanza(N, generador):
    """
    Estima la esperanza usando la ley fuerte de los grandes numeros
    Args:
        N:            Cantidad total de valores a promediar
        generador:    Generador de la variable aleatoria de interes
    """
    esperanza = 0
    for _ in range(N):
        esperanza += generador()
    return esperanza / N


def media_muestral(datos):
    """
    Calcula la media muestral de los datos dados
    """
    n = len(datos)
    media = sum(datos) / n
    return media


def var_muestral(datos):
    """
    Calcula la varianza muestral de los datos dados
    """
    n = len(datos)
    media = media_muestral(datos)
    varianza = sum(list(map(lambda x: (x - media)**2, datos)))
    varianza = varianza / (n - 1)
    return varianza


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


def media_muestral_d(d, generador, n=100):
    """
    Estima el valor esperado de la variable aleatoria simulada por generador
    usando el estimador insesgado media muestral.
    Args:
        n:       : Tamaño minimo de la muestra
        d        : Cota para la desviacion aceptable del estimador
        generador: Generador de la variable aleatoria 
    Return:
        media    : Estimacion del valor esperado
        scuad    : Varianza muestral obtenida
        i        : Tamaño de la muestra final
    """
    media = generador()
    scuad = 0
    i = 1
    while i <= n or sqrt(scuad/i) > d:
        i += 1
        X = generador()
        media_previa = media

        # Forma recursiva del estimador de la media muestral
        media = media_previa + (X - media_previa) / i
        # Forma recursiva del estimador de la varianza muestral
        scuad = scuad * (1 - 1/(i-1)) + i*(media - media_previa) ** 2
    return media, scuad, i


def estimar_proporcion_d(d, generador, n=100):
    """
    Estima la proporción de exito de una bernoulli, con un desvio 
    de estimador acotado
    Args:
        n:       : Tamaño minimo de la muestra
        d        : Cota para la desviacion aceptable del estimador
        generador: Generador de una bernoulli 
    Return:
        p        : Estimacion de la proporcion
        var_m    : Varianza muestral obtenida
        i        : Tamaño de la muestra final
    """
    p = 0
    i = 0
    while i <= n or sqrt(p * (1 - p) / i) > d:
        i += 1
        X = generador()
        p = p + (X - p) / i
    var_m = p * (1 - p)
    return p, var_m, i


def normal_ross(mu=0, sigma=1):
    """
    Genera una variable normal estandar (por defecto) usando el algoritmo descrito 
    en el libro de Sheldon Ross, el cual esta basado en el metodo de aceptacion y 
    rechazo
    Args:
        mu   : Esperanza de la variable normal
        sigma: Desvio estandar de la variable normal 
    """
    while True:
        Y1 = -log(random())  # Exponencial de parametro 1
        Y2 = -log(random())  # Exponencial de parametro 1
        if Y2 >= (Y1 - 1) ** 2 / 2:
            # En este punto Y1 es una variable aleatoria con distribucion |Z|
            # La siguiente comparacion es el metodo para generar Z con composicion
            # a partir del generador de |Z|
            if random() < 0.5:
                return Y1 * sigma + mu
            else:
                return -Y1 * sigma + mu


#!NOTE Ejercicio 1
def ej_1():
    """
    Resumen del ejercicio: Generar una muestra de datos normales a partir 
    del algorítmo dado en el libro ross para generar eventos normales y 
    un generador de muestras.
    a) Ver cuantos eventos tiene la muestra cumpliendo sigma / sqrt(n) < 0.1
    b) Calcular la media muestral
    c) Calcular la varianza muestral
    """
    # Tamaño esperado de la muestra
    # sigma / 0.1 < sqrt(n) <=> (sigma*10)**2 < n pero sabemos que
    # el desvio de una normal estandar es 1 por lo tanto n = 101
    tamaño_muestra_esperado = 101

    # Simulamos las condiciones pedidas en el enunciado
    n = 30
    d = 0.1

    simulacion_1 = media_muestral_d(d, normal_ross, n)

    #! Print ejercicio 1
    tamaño_muestra_obtenido = simulacion_1[2]
    media_muestral_1 = round(simulacion_1[0], 4)
    varianza_muestral_1 = round(simulacion_1[1], 4)

    datos = [[tamaño_muestra_esperado, tamaño_muestra_obtenido,
              media_muestral_1, varianza_muestral_1]]

    headers = ["Tamaño esperado", "Tamaño obtenido", "Media muestral",
               "Varianza muestral"]

    print(tabulate(datos, headers, tablefmt="pretty"))


#!NOTE Ejercicio 2
#! Estimacion de las integrales por Monte Carlo
def generar_i():
    """
    Devuelve un valor aleatorio de la funcion g determinada por el metodo de
    Monte Carlo para el inciso i
    """
    U = random()
    return exp(U) / sqrt(2*U)


def generar_ii():
    """
    Devuelve un valor aleatorio de la funcion g determinada por el metodo de
    Monte Carlo para el inciso ii
    """
    U = random()
    return 1/U**2 * (1/U - 1)**2 * exp(-(1/U - 1)**2)


def ej_2():
    # Estimacion de las integrales por Monte Carlo
    d = 0.01
    estimacion_i = media_muestral_d(d, generar_i)
    estimacion_ii = media_muestral_d(d, generar_ii)

    datos_2 = [["i", estimacion_i[0], estimacion_i[2]],
               ["ii", estimacion_ii[0]*2, estimacion_ii[2]]
               ]
    headers_2 = ["Inciso", "Estimacion", "Datos generados"]

    print(tabulate(datos_2, headers=headers_2, tablefmt="pretty"))


#!NOTE Ejercicio 3
#! Estimacion de las integrales por Monte Carlo
def integral_i():
    """
    Una funcion que sirve para estimar la integral del inciso i usando el
    metodo de Monte Carlo
    """
    U = random()
    return sin((U+1)*pi) / (U+1)


def integral_ii():
    """
    Una funcion que sirve para estimar la integral del inciso ii usando el
    metodo de Monte Carlo
    """
    U = random()
    return 1/U**2 * (3 / (3 + (1/U - 1)**4))


def ej_3():
    # Parametros para estimar las integrales con un intervalo de confianza del 95%
    # con el SEMIANCHO no mayor a 0.001 del intervalo
    z_alpha_2 = 1.96
    d = 0.001 / z_alpha_2

    # Estimamos las integrales simulando hasta satisfacer las condiciones dadas en
    # el enunciado (un intervalo no mayor al 0.001 con una confianza del 95%)
    b_3_i = media_muestral_d(d, integral_i)
    b_3_ii = media_muestral_d(d, integral_ii)

    # Generamos las muestras de los distintos tamaños pedidos en la tabla
    numero_sim = [1000, 5000, 7000]
    sim_3_i = list(map(lambda n: generar_muestra(integral_i, n), numero_sim))
    sim_3_ii = list(map(lambda n: generar_muestra(integral_ii, n), numero_sim))

    # Calculamos los estimadores puntuales en las muestras obtenidas
    sim_3_i = list(map(lambda datos: [media_muestral(datos),
                                      var_muestral(datos), len(datos)],
                       sim_3_i))

    sim_3_ii = list(map(lambda datos: [media_muestral(datos),
                                       var_muestral(datos), len(datos)],
                        sim_3_ii))

    # Agregamos las simulaciones anteriores a las listas correspondientes
    sim_3_i.append(b_3_i)
    sim_3_ii.append(b_3_ii)

    # Funcion para calcular el intervalo obtenido en las simulaciones
    # a partir de los resultados en la simulacion
    def intervalo(media, var, n): return [round(media - sqrt(var/n) * z_alpha_2, 4),
                                          round(media + sqrt(var/n) * z_alpha_2, 4)]

    # Formateo de datos
    datos_3_i = list(map(lambda x: [x[2], intervalo(
        x[0], x[1], x[2]), round(x[0], 4)], sim_3_i))
    datos_3_ii = list(map(lambda x: [x[2], intervalo(
        x[0], x[1], x[2]), round(x[0], 4)], sim_3_ii))
    headers_3 = ["N° de simulaciones", "Intervalo", "Valor estimado"]

    print("\nInciso i")
    print(tabulate(datos_3_i, headers=headers_3, tablefmt="pretty"))
    print("\nInciso ii")
    print(tabulate(datos_3_ii, headers=headers_3, tablefmt="pretty"))


#!NOTE Ejercicio 4
#! Estimación de n y e
def generar_N():
    """
    Genera la variable aleatoria N del ejercicio 4
    """
    n = 0
    suma = 0
    while suma < 1:
        n += 1
        suma += random()
    return n


def estimador_e(n):
    """
    Genera valores aleatorios del estimador de e (media muestral)
    Args:
        n: Tamaño de la muestra
    """
    muestra      = generar_muestra(generar_N, n)
    estimacion_e = media_muestral(muestra)
    return estimacion_e


def ej_4():
    # Inciso b
    # Calculo la varianza muestral del estimador e
    n = 1000
    muestra_estimador  = generar_muestra(lambda: estimador_e(n), n)
    varianza_estimador = var_muestral(muestra_estimador) 

    # Inciso c
    # Estimamos e por intervalos de confianza al 95% con un ancho de 0.1
    z_alpha_2 = 1.96
    d = 0.1 / (2 * z_alpha_2)
    estimacion_e = media_muestral_d(d, generar_N)[0]


    datos_4   = [[e, estimacion_e, varianza_estimador]]
    headers_4 = ["Valor real e","Estimacion de e", "Varianza estimador"]
    print(tabulate(datos_4, headers=headers_4, tablefmt="pretty"))


#!NOTE Ejercicio 5
#! Generadores
def generar_M():
    """
    Genera la variable aleatoria M dada en el ejercicio 5
    """
    numero_actual = random()
    n = 2
    while True:
        numero_proximo = random()
        if numero_actual < numero_proximo:
            numero_actual = numero_proximo
            n+=1
        else:
            return n
        

def estimador_e(n):
    """
    Genera valores aleatorios del estimador de e (media muestral)
    Args:
        n: Tamaño de la muestra
    """
    muestra      = generar_muestra(generar_M, n)
    estimacion_e = media_muestral(muestra)
    return estimacion_e


def ej_5():
    # Estimamos el valor de e con 1000 simulaciones
    n = 1000

    # Inciso c
    muestra_m    = generar_muestra(generar_M, n)
    estimacion_e = media_muestral(muestra_m)

    # Inciso d 
    # Varianza del estimador de e (media muestral de M)
    muestra_estimador      = generar_muestra(lambda: estimador_e(n), n)
    var_muestral_estimador = var_muestral(muestra_estimador) 

    # Estimacion de e con intervalos de confianza del 95% y largo del 0.01
    z_alpha_2 = 1.96
    L = 0.01
    d = L / (2 * z_alpha_2)
    estimacion_e_confianza = media_muestral_d(d, generar_M)[0]

    data_5    = [[estimacion_e, var_muestral_estimador, estimacion_e_confianza]]
    headers_5 = ["Valor por estimador", "Varianza del estimador", 
                "Estimacion por intervalo"]

    print(tabulate(data_5, headers=headers_5, tablefmt="pretty"))


#!NOTE Ejercicio 6
#! Generador
def cae_en_circulo():
    """
    Genera la variable aleatoria bernoulli que modela el hecho de que un punto
    aleatorio del cuadrado [-1,1]x[-1,1] caiga en el circulo unitario
    """
    X = random()*2 - 1    # U(-1, 1)  
    Y = random()*2 - 1    # U(-1, 1)
    return int(X**2 + Y**2 <= 1)


def ej_6():
    # Estimamos pi por intervalo de confianza al 95% con una cota de 0.1
    L = 0.1
    z_alpha_2 = 1.96         # Valor de la normal para la confianza al 95%
    d = L / (8 * z_alpha_2)  # Por justificacion analitica

    simular_pi = estimar_proporcion_d(d, cae_en_circulo) 

    estimacion_pi  = simular_pi[0] * 4  # Porque la media muestral de cae_en_circulo estima pi/4
    tamaño_muestra = simular_pi[2]

    data_6    = [[pi, estimacion_pi, tamaño_muestra]]
    headers_6 = ["Valor de pi", "Estimacion de pi", "Tamaño final de la muestra"]

    print(tabulate(data_6, headers=headers_6, tablefmt="pretty"))


#!NOTE Funciones para BOOTSTRAP
def generar_empirica(datos):
    """
    Genera la variable aleatoria con distribucion empirica para los
    datos dados
    """
    n = len(datos)
    U = int(random() * n)
    return datos[U]


def generar_muestra_bootstrap_jose(datos):
    """
    Genera una muestra bootstrap a partir de la distribucion empirica
    de los datos dados
    """
    n = len(datos)        # Tamaño de la muestra bootstrap apropiado
    muestra = generar_muestra(lambda: generar_empirica(datos), n)
    return muestra


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
    return X


def esperanza_empirica(datos):
    """
    Calcula la esperanza empirica de los datos dados
    """
    esperanza = sum(datos) / len(datos)
    return esperanza


def varianza_empirica(datos):
    """
    Calcula la varianza empirica de los datos dados
    """
    mu = esperanza_empirica(
        datos)  # Suponemos que no conocemos el valor esperado real
    varianza_empirica = sum(list(map(lambda x: (x-mu)**2, datos))) / len(datos)
    return varianza_empirica


def var_muestral_mu(datos, mu):
    """
    Calcula la varianza muestral sin estimar la esperanza de los datos
    Args:
        mu: Valor esperado de los datos
    """
    var = sum(list(map(lambda x: (x-mu)**2, datos))) / len(datos)
    return var


#!NOTE Ejercicio 7
def ej_7():
    pass


#!NOTE Ejercicio 8
def ej_8():
    pass


#!NOTE Ejercicio 9
def ej_9():
    #! C)
    data = [3.0592, 2.3304, 2.8548, 1.2546, 2.1628,
            4.9828, 5.4259, 0.9078, 4.5811, 3.2749]
    a = 2.5
    #! A)
    data_len = len(data)
    contador = 0
    for _ in range(N_sim):
        data_gen = generar_muestra_bootstrap(data)
        media_muestral_empirica = esperanza_empirica(data_gen)
        media = esperanza_empirica(data)
        varianza_muestral = varianza_empirica(data_gen)
        T = (media_muestral_empirica - media) / \
            sqrt((varianza_muestral/data_len))
        if T > a:
            contador += 1
    probabilidad = round(contador/N_sim, 5)

    #! B) Todavía no pide usar bootstrap
    # te da la normal (distribucion conocida)
    media_muestral_normal = media_muestral(data)
    var_muestral_normal = var_muestral(data)

    #! Print ejercicio 9
    datos = [[media_muestral_normal, var_muestral_normal, probabilidad]]
    headers = ["media_muestral_normal",
               "var_muestral_normal", "P(T<2.5) estimada"]

    print(tabulate(datos, headers, tablefmt="pretty"))


#!NOTE Ejercicio 10
def ej_10():
    """
    Valor esperado Empírico: Igual a la esperanza muestral (con los datos 
    dados), no tiene sentido tratar de generar la empírica ya que es 
    uniformemente distribuída

    Bootrstrap: Tengo un conjunto de datos cuya distribucion es desconocida,
    uso la distribucion empirica para generar muestras

    Media Muestral usando Bootstrap: Genero una muestra mediante Bootstrap
    y calculo su media
    """
    data = [7.5, 12.3, 8.8, 7.9, 9.3, 10.4, 10.9, 9.6, 9.1, 11.2]

    #! A) Valor esperado Empirico
    E_empirica = esperanza_empirica(data)

    #! B) Aproximación Bootstrap del ECM (Error Cuadrático Medio)
    # ECM = Esperanza((media - media_simulada)**2)
    aux = 0
    for _ in range(N_sim):
        aux += (E_empirica - media_muestral(generar_muestra_bootstrap(data)))**2

    ECM = aux/N_sim

    #! C) P(8 <= Xmedia <= 10)
    contador = 0
    for _ in range(N_sim):
        if 8 <= media_muestral(generar_muestra_bootstrap(data)) <= 10:
            contador += 1
    probabilidad = contador/N_sim

    #! Print ejercicio 10
    datos = [[E_empirica, ECM, probabilidad]]
    headers = ["Esperanza empirica", "ECM estimado", "P(8<=X̄<=10) estimada"]

    print(tabulate(datos, headers, tablefmt="pretty"))


#!NOTE Ejercicio 11
def ej_11():
    """
    Genera una variable aleatoria con probabilidad de exito
    igual a p(|s² - σ²| > 0.02)
    """
    data = [144.98, 145.04, 145.02, 145.04, 145.03, 145.03, 145.04,
            144.97, 145.05, 145.03, 145.02, 145, 145.02]

    contador = 0
    for _ in range(N_sim):
        var_muestral = varianza_empirica(generar_muestra_bootstrap(data))
        var_empirica = varianza_empirica(data)
        guarda = abs(var_empirica - var_muestral) > 0.02
        if guarda:
            contador += 1

    probabilidad = contador/N_sim

    #! Print ejercicio 11
    datos = [[esperanza_empirica(data), var_empirica, probabilidad]]
    headers = ["Esperanza empirica", "Varianza empirica",
               "P(|s² - σ²| > 0.02) estimado"]

    print(tabulate(datos, headers, tablefmt="pretty"))


#!NOTE Ejercicio 12
def ej_12():
    pass
