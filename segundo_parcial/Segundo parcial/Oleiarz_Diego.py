from random import random, uniform
from math import log


def ejercicio1():
    return 0

###### EJERCICIO 2 #######


def transf_inversa_ej2():
    U = random()
    if U < 1/3:
        return log(3*U)
    else:
        return log((1-U)*(3/2))/(-2)  # Revisar inversa


def ejercicio2(N):
    suma = 0
    for _ in range(N):
        if transf_inversa_ej2() <= 1:
            suma += 1
    return suma/N


print(f"El resultado ejercicio 2 es: {ejercicio2(10000)}")


def AyR_ej3():
    while True:
        X = uniform(-1, 1)
        U = random()
        if U < (1 - X**2):
            return X


def ejercicio3(N):
    suma = 0
    for _ in range(N):
        if AyR_ej3() <= 0:
            suma += 1
    return suma/N


print(f"El resultado ejercicio 3 es: {ejercicio3(10000)}")


def a(n):
    U = random()
    if U < ((2**(n-1)) + 2)/(3**n):
        return 0
    else:
        return 1


def exp_ej4():
    i = 0
    if random() > 1/3:
        while random() > 1/3:
            i += 1
        return i
    else:
        while random() <= 1/3:
            i += 1
        return i


def ejercicio4(Nsim, n):
    suma = 0
    for _ in range(Nsim):
        if exp_ej4() == n:
            suma += 1
    return suma/Nsim


print(f"El resultado ejercicio 4 es: {ejercicio4(10000,4)}")
