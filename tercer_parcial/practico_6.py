from random import random
from tabulate import tabulate
from time import time
from math import log, e, sqrt, exp, sin, pi

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


def generar_muestra_bootstrap(datos):
    """
    Genera una muestra bootstrap a partir de la distribucion empirica
    de los datos dados
    """
    n = len(datos)        # Tamaño de la muestra bootstrap apropiado
    muestra = generar_muestra(lambda: generar_empirica(datos), n)
    return muestra


def esperanza_empirica(datos):
    """
    Calcula la esperanza empirica de los datos dados
    """
    esperanza = sum(datos) / len(datos)
    return esperanza


def varianza_empirica(datos):
    """
    Calcula la varianza empirica de los datos datos
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


#!NOTE Ejercicio 10

def ej_10():
    """
    Valor esperado Empírico: Igual a la esperanza muestral (con los datos 
    dados), no tiene sentido tratar de generar la empírica ya que es 
    uniformemente distribuída

    """
    data = [7.5, 12.3, 8.8, 7.9, 9.3, 10.4, 10.9, 9.6, 9.1, 11, 2]
    #! A) Valor esperado Empirico
    E_empirica = esperanza_empirica(data)

    #! B) Aproximación Bootstrap del ECM
    ECM = 0
    for _ in 10000:
        ECM += (E_empirica - generar_muestra_bootstrap(data))**2

    ECM = ECM/10000