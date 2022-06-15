from math import log, inf
from random import random
from statistics import pstdev

def reparacion_1(maquinas, repuestos, lambda_m, lambda_r):
    tiempo = 0
    a_reparar = 0
    tiempo_reparacion = inf
    # Genero N variables aleatorias con los tiempos de vida de las máquinas
    tiempos_de_vida = [(-log(random())/(1/lambda_m)) for _ in range(maquinas)]
    tiempos_de_vida.sort()

    while True:
        # Caso 1:
        if tiempos_de_vida[0] < tiempo_reparacion:
            tiempo = tiempos_de_vida[0]
            a_reparar += 1
            if a_reparar == repuestos + 1:
                return tiempo # pues como hay repuestos + 1 maquinas descompuestas, no hay repuestos 
            if a_reparar < repuestos + 1:
                x = -log(random())/(1/lambda_m) # tiempo de vida de la maquina
                tiempos_de_vida[0] = tiempo + x
                tiempos_de_vida.sort()
            if a_reparar == 1:
                x = -log(random())/(1/lambda_r) # tiempo de reparacion
                tiempo_reparacion = tiempo + x # tiempo donde concluye la reparación
        
        # Caso 2:
        if tiempo_reparacion < tiempos_de_vida[0]:
            tiempo = tiempo_reparacion
            a_reparar -= 1
            if a_reparar > 0:
                x = -log(random())/(1/lambda_r) # tiempo de reparacion
                tiempo_reparacion = tiempo + x # tiempo donde concluye la reparación
            if a_reparar == 0:
                tiempo_reparacion = inf


def reparacion_2(maquinas, repuestos, lambda_m, lambda_r):
    tiempo = 0
    a_reparar = 0
    tiempo_reparacion = [inf, inf]
    tiempos_de_vida = [(-log(random())/(1/lambda_m)) for _ in range(maquinas)]
    tiempos_de_vida.sort()

    while True:
        # Caso 1:
        if tiempos_de_vida[0] < tiempo_reparacion[0]:
            tiempo = tiempos_de_vida[0]
            a_reparar += 1
            if a_reparar == repuestos + 1:
                return tiempo
            if a_reparar < repuestos + 1:
                x = -log(random())/(1/lambda_m)
                tiempos_de_vida[0] = tiempo + x
                tiempos_de_vida.sort()
            if a_reparar == 1:
                x = -log(random())/(1/lambda_r)
                tiempo_reparacion[0] = tiempo + x
            if a_reparar == 2:
                x = -log(random())/(1/lambda_r)
                tiempo_reparacion[1] = tiempo + x
            tiempo_reparacion.sort()

        # Caso 2:
        if tiempo_reparacion[0] < tiempos_de_vida[0]:
            tiempo = tiempo_reparacion[0]
            a_reparar -= 1
            if a_reparar > 1:
                # caso donde se acaba de ocupar uno
                x = -log(random())/(1/lambda_r)
                tiempo_reparacion[0] = tiempo + x
            else:
                # caso donde se libera uno
                tiempo_reparacion[0] = inf
            tiempo_reparacion.sort()
              
def estimar_esperanza(n, f):
    suma = 0
    for _ in range(n):
        suma += f(7,3,1,1/8)
    return (suma/n)

def estimar_desvio(n, f):
    simulaciones = [f(7,3,1,1/8) for _ in range(n)]
    return pstdev(simulaciones)

print(f"Un operador ➡️ Tiempo medio de falla: {estimar_esperanza(10000, reparacion_1)}, Desviación estándar: {estimar_desvio(10000, reparacion_1)}")
print(f"Dos operadores ➡️ Tiempo medio de falla: {estimar_esperanza(10000, reparacion_2)}, Desviación estándar: {estimar_desvio(10000, reparacion_2)}")