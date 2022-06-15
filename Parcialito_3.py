from random import random
from math import sqrt

datos = [0.932, 0.202, 2.627, 3.297, 0.548, 1.828, 2.217, 2.235, 1.041, 3.096]

########### Funciones auxiliares ##############


def generar_muestra(generador, n):
    datos = []
    for _ in range(n):
        datos.append(generador())
    return datos


def media_muestral(datos):
    return sum(datos) / len(datos)


def var_muestral(datos):
    varianza = sum(list(map(lambda x: (x - media_muestral(datos))**2, datos)))
    varianza = varianza / (len(datos) - 1)
    return varianza


def generar_empirica():
    return datos[int(random() * len(datos))]


def generar_muestra_bootstrap():
    return generar_muestra(lambda: generar_empirica(), len(datos))


def replicacion_bootstrap(datos):
    replicacion = (media_muestral(generar_muestra_bootstrap()) -
                   media_muestral(datos)) ** 2
    return replicacion


##################### Ejercicios ###########################


def ejercicio_1(N):
    media = media_muestral(datos)
    varianza = var_muestral(datos)
    conteo = 0
    for _ in range(N):
        muestra = generar_muestra_bootstrap()
        if (abs(media_muestral(muestra) - media)) >= 0.5*sqrt(varianza):
            conteo += 1
    return conteo/N


print(f"La probabilidad de que la media muestral diste de la media en al menos la mitad del desvío: {ejercicio_1(1000)}")


def ejercicio_2(N):
    sumatoria = 0
    for _ in range(N):
        sumatoria += replicacion_bootstrap(datos)
    return round(sumatoria/N, 4)


print(f"Error Cuadrático Medio: {ejercicio_2(1000)}")
