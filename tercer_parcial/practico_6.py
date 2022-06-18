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
        media = media_previa + (X - media_previa) / i
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


#!NOTE Ejercicio 1
def ej_1():
    pass


#!NOTE Ejercicio 2
def ej_2():
    pass


#!NOTE Ejercicio 3
def ej_3():
    pass


#!NOTE Ejercicio 4
def ej_4():
    pass


#!NOTE Ejercicio 5
def ej_5():
    pass


#!NOTE Ejercicio 6
def ej_6():
    pass


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
