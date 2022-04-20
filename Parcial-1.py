from random import random
from math import exp


print("Ejercicio 2c")

def ejercicio2(Nsim):
    result = 0
    for _ in range(Nsim):
        comp = max(random(),random())
        if (comp > 0.6):
            result = result + 1
    return result/Nsim

print(ejercicio2(10000))


print("Ejercicio 4b, integral A")


##estimacion de la integral de g con Nsim simulaciones ´
def ejercicio4a(Nsim):
    Integral = 0
    for _ in range(Nsim):
        Integral += 1 - exp(-(random() + random()))
    return Integral/Nsim


print(ejercicio4a(1000))

print(ejercicio4a(10000))

print(ejercicio4a(100000))

print(ejercicio4a(1000000))


print("----------------------------")


print("Ejercicio 4b, integral B")

##estimacion de la integral de g con Nsim simulaciones ´
def ejercicio4b(Nsim):
    Integral = 0
    for _ in range(Nsim):
        rand = random()
        Integral += (((1/rand)-1)**2 * exp(-((1/rand)-1)**2) ) / rand**2
    return Integral/Nsim


print(ejercicio4b(1000))

print(ejercicio4b(10000))

print(ejercicio4b(100000))

print(ejercicio4b(1000000))
