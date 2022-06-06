from math import log
from random import random


def ejercicio_1_a(s, N, lambda0, lambda1):
    cajas_deposito = s
    cajas_tecnico = 0
    tiempos_rotura = []
    # Genero N variables aleatorias
    for _ in range(N):
        aux = -log(random())/lambda0
        tiempos_rotura.append(aux)
    tiempos_rotura.sort()

    tiempo = tiempos_rotura[0]

    # Itera sobre cuando se rompe una maquina
    while cajas_deposito != 0:

        
        # Se rompe una caja
        cajas_tecnico += 1

        # Itera sobre maquinas arregladas por el tecnico hasta que se rompa otra
        while cajas_tecnico >= 0 and tiempo < tiempos_rotura[0] and cajas_deposito >= 0:
            tiempo = tiempos_rotura[0] - log(random())/lambda1
            cajas_tecnico -= 1
            cajas_deposito += 1

        
        # Se repone la caja rota con una del deposito
        cajas_deposito -= 1
        tiempos_rotura[0] = tiempo - log(random())/lambda0 # Posiblemente vaya al final de la lista 
        tiempos_rotura.sort()
    return tiempo


def ejercicio_2_a(s, N, lambda0, lambda1):
    cajas_deposito = s
    cajas_tecnico = [0, 0]
    tiempos_rotura = []
    # Genero N variables aleatorias
    for _ in range(N):
        a = -log(random())/lambda0
        tiempos_rotura.append(a)
    tiempos_rotura.sort()

    tiempo = tiempos_rotura[0]

    # Itera sobre cuando se rompe una maquina
    a = 0
    while cajas_deposito != 0:
        
        # Se rompe una caja
        cajas_tecnico[a] += 1
        
        # Se repone la caja rota con una del deposito
        cajas_deposito -= 1
        tiempos_rotura[0] = tiempo -log(random())/lambda0
        tiempos_rotura.sort()

        # Itera sobre maquinas arregladas por cajas_tecnico hasta que se rompa otra
        tiempoa, tiempob = tiempo,tiempo
        
        while cajas_tecnico[0] and tiempoa < tiempos_rotura[0] and cajas_deposito != 0:
            tiempoa = tiempos_rotura[0] - log(random())/lambda1
            cajas_tecnico[0] -= 1
            cajas_deposito += 1

        while cajas_tecnico[1] and tiempob < tiempos_rotura[0] and cajas_deposito != 0:
            tiempob = tiempos_rotura[0] - log(random())/lambda1
            cajas_tecnico[1] -= 1
            cajas_deposito += 1

        tiempo = max(tiempoa,tiempob)

        if  cajas_tecnico[1] < cajas_tecnico[0]:
            a = a % 2
        else:
            a = a % 2 - 1

    return tiempo


def ejercicio_1_b(N):
    a = 0
    for _ in range(N):
       a += ejercicio_1_a(3, 7, 1, 8)
    return a/N


def ejercicio_2_b(N):
    a = 0
    for _ in range(N):
       a += ejercicio_2_a(3, 7, 1, 8)
    return a/N

print(ejercicio_1_b(1)) # 1.22
print(ejercicio_2_b(10000))
