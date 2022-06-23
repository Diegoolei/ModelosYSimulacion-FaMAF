from random import random
from math import sqrt, log, exp


#!NOTE Funciones auxiliares Ejercicio 1
def TinversaX():
    U = random()
    if U < 0.5:
        return 0
    elif U < 0.75:
        return 1
    elif U < 0.9375:
        return 3
    else:
        return 2


def estimar_esperanza(N):
    suma = 0
    for _ in range(N):
        suma += TinversaX()
    return suma/N


#!NOTE Ejercicio 1
def ejercicio1():
    """
    #! A)
    Distribucion de probabilidad: 
    P(X = 0) = 1/2 = 0.5;  
    P(X = 1) = 32/128 = 0.25; 
    P(X = 2) = 8/128 = 0.0625
    P(X = 3)= 1 - P(X=0) - P(X=1) - P(X=2) = 1 - 1/2- 32/128 - 8/128 = 0.1875

    Valor Esperado de X:
    Sumatoria(x*p(x)) = 0*0.5 + 1*0.25 + 2*0.0625 + 3*0.1875 = 0.9375
    Ojo que la f(x) seria:
    f(x) = {0.5 si x=0
            0.25 si x=1
            0.0625 si x=2
            0.1875 si x=3
    Metodo de la TI: # gracias valen <3
    Se ordenan las probabilidades de mayor a menor, para mas eficiencia. 
    Se genera una v.a. uniforme en (0,1), y segun a qué intervalo pertenezca,
    se devuelve el valor de X generado.
    """
    print("-----Ejercicio 1------")
    print(f"E[X] = {estimar_esperanza(1000)}")


#!NOTE Funciones auxiliares Ejercicio 2
def variableX():
    U = random()
    if U < 2/9:
        return 3/2*U
    elif U < 5/9:
        return sqrt(U - 1/9)
    else:
        return 3/4*(U + 1/3)


def calculo_probabilidad_2(Nsim):
    conteo = 0
    for _ in range(Nsim):
        if 0.2 < variableX() <= 0.5:
            conteo += 1
    return conteo/Nsim

#!NOTE Ejercicio 2


def ejercicio2():
    print()
    print("-----Ejercicio 2------")
    print(
        f"La probabilidad de que X sea entre 0.2 y 0.5 es {calculo_probabilidad_2(10000)}")


#!NOTE Funciones auxiliares Ejercicio 3
def generar_exp(Lambda):
    """
    Genera una variable aleatoria exponencial usando el metodo de la transformada
    inversa
    Args:
        Lambda: Parametro de la variable aleatoria exponencial
    """
    U = random()
    return -log(U) / Lambda


def rechazoX():
    while True:
        Y = generar_exp(1)
        c = 2.1654
        U = random()
        if U < (4*(Y**2))/(exp(Y)*c):
            return Y


def calculo_probabilidad_3(Nsim):
    conteo = 0
    for _ in range(Nsim):
        if rechazoX() > 1:
            conteo += 1
    return conteo/Nsim


#!NOTE Ejercicio 3
def ejercicio3():
    print()
    print("-----Ejercicio 3------")
    print(
        f"La probabilidad de que X sea mayor a 1 es {calculo_probabilidad_3(1000)}")


#!NOTE Auxiliares Ejercicio 4
def tirar_moneda(p):
    U = random()
    if U <= p:
        return 1
    else:
        return 0


def experimentoX(p):
    primera_tirada = tirar_moneda(p)
    n = 1
    while primera_tirada != tirar_moneda(p):
        n += 1
    return n


def calculo_probabilidad_4_a(N_sim):
    #!NOTE Ejercicio 4 a)
    p = 0.25
    n = 0
    for _ in range(N_sim):
        if experimentoX(p) == 4:
            n += 1
    return n/N_sim


def composicionX(p):
    primera_tirada = tirar_moneda(p)
    n = 1
    while primera_tirada != tirar_moneda(p):
        n += 1
    return n


def calculo_probabilidad_4_b(N_sim):
    #!NOTE Ejercicio 4 b)
    p = 0.25
    n = 0
    for _ in range(N_sim):
        if composicionX(p) == 4:
            n += 1
    return n/N_sim

#!NOTE EJERCICIO 4


def ejercicio4():
    """
    Método de composición: 
    X1 = la moneda sale cara con prob p
    X2 = la moneda sale cruz con prob 1-p
    P (X = j) = αpj + (1 − α)qj
    P (X = j) = 1/2 (p (1-p)^j-1 + (1-p)p^j-1)
    qj = p^(j-1)/2
    pj = (1-p)^(j-1)/2
    P(X1 = xj) = pj
    P(X2 = xj) = qj
    X = {X1 con prob p
         X2 con prob 1-p
    U = random()
    if U < p:
        generar X1
        return X1
    else:
        generar X2
        return X2   
    """

    print()
    print("------Ejercicio 4 ------")
    print(
        f"la probabilidad de que X sea 4 es: {calculo_probabilidad_4_a(10000)}")
    print(
        f"la probabilidad de que X sea 4 con composicion es: {calculo_probabilidad_4_b(10000)}")


ejercicio1()
ejercicio2()
ejercicio3()
ejercicio4()
