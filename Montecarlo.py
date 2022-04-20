from random import random
# from math import exp

##estimacion de la integral de g con Nsim simulaciones
def montecarlo(g, Nsim):
    Integral = 0
    for _ in range(Nsim):
        Integral += g(random())
    return Integral/Nsim


print(montecarlo(1000))

print(montecarlo(10000))

print(montecarlo(100000))

print(montecarlo(1000000))
