from random import random, uniform
from math import log


#!NOTE FUNCIONES GENERALES
def uniforme_d(n, m):
    """
    Genera numeros aleatorios entre n y m (inclusive) 
    """
    U = int(random() * (m - n + 1))  # 0 <= U < (m-n+1) Equivale a 0 <= U <= (m-n)
    U = U + n                        # Equivale a n <= U <= m
    return U


def geometrica_SIM(p_exito):
    """
    Genera una variable aleatoria geometrica generando ensayos hasta que uno sea
    exitoso
    Args:
        p_exito: Parametro de la v.a. geometrica
    """
    i = 1
    while(True):
        U = random()
        if U < p_exito:
            return i
        i += 1


#!NOTE EJERCICIO 1
def ej_1():
    """
    #!NOTE Distribucion de probabilidad
    Distribución de probabilidad: P(X=0)=0.32   P(X=1)=0.21  P(X=2)=0.33  P(X=3)=0.14

    #!NOTE Descripción método de urna
    El método de la urna consiste en dada una variable aleatoria X, que toma un número
    finito de valores, considerar un valor k perteneciente a los naturales tal que k 
    por una probabilidad pj igual a P(X = j) sea entero para todo j, 1 <= j <= n.
    Teniendo un arreglo A de k posiciones, almacenando cada valor i en k por pi posiciones
    del arreglo. El algoritmo selecciona una posición al azar del arreglo y devuelve 
    el valor en dicha posición. 
    """

    #!NOTE Método de la Urna
    A = [1, 2, 3, 4]
    U = int(random() * len(A))
    return A[U]


#!NOTE Transformada inversa EJERCICIO 2
def transf_inversa_ej2():
    """
    Para hacer la transformada inversa, primero calculo la Funcion de probabilidad acumulada (F(x))
    para todos los intervalos
    Luego hago la inversa para cada intervalo (U = F(x) y despejo x)
    Finalmente valuo la acumulada en el punto que comunica los intervalos y allí es donde separo el if 
    """
    #!Transformada inversa
    U = random()
    if U < 1/3:
        return log(3*U)
    else:
        return log((1-U)*(3/2))/(-2)


#!NOTE EJERCICIO 2
def ej_2(N):
    """
    Escribir un codigo en Python que genere valores de X utilizando el metodo de la transformada inversa.
    Utilizar este codigo para estimar P(X ≤ 1) con 10000 simulaciones. Imprimir este valor.
    """
    suma = 0
    for _ in range(N):
        if transf_inversa_ej2() <= 1:
            suma += 1
    return suma/N


#!NOTE Aceptación y Rechazo EJERCICIO 3
def AyR_ej3():
    """
    Tengo que maximizar h(x) tal que h(x)=f(x)/g(x) <= c para eso:
    1) Veo con que funcion g(x) rechazar segun que intervalo tenga f(x)
      - si el intervalo tiene la forma a <= x <= b uso una uniforme U(a,b) = 1/(b-a)
      - si tiene la forma de 0<x uso una exponencial
      - -inf<x<inf uso normal
    2) despejo h(x)
    3) maximizo c (valuo en los extremos, derivo h(x) e igualo a 0 y despejo x)
    4) valuo h(x) donde maximiza c (valor encontrado en 3)
    5) reemplazo en h(x) c por su valor maximo y simplifico
    6) h(x) será la guarda con la que comparo en el if con x generado segun g(x)
    """
    while True:
        X = uniform(-1, 1)
        U = random()
        if U < (1 - X**2):
            return X


#!NOTE EJERCICIO 3
def ej_3(N):
    """
    Escribir un codigo en Python que genere valores de X usando el metodo descripto en (a).
    Utilizar este codigo para estimar P(X > 0). Imprimir este valor.
    """
    suma = 0
    for _ in range(N):
        if AyR_ej3() <= 0:
            suma += 1
    return suma/N


#!NOTE Auxiliares Ejercicio 4
def tirar_moneda(p):
    U = random()
    if U < p:
        return 1
    else:
        return 0


def experimento():
    n = 1
    anterior = tirar_moneda()
    while anterior == tirar_moneda():
        n += 1
    return n


def calc_probabilidad(N_sim):
    n = 0
    for _ in range(N_sim):
        if experimento() == 4:
            n += 1
    return n/N_sim


#!NOTE EJERCICIO 4
def ej_4():
    """
    Tengo que maximizar h(x) tal que h(x)=f(x)/g(x) <= c para eso:
    1) Veo con que funcion g(x) rechazar segun que intervalo tenga f(x)
      - si el intervalo tiene la forma a <= x <= b uso una uniforme U(a,b) = 1/(b-a)
      - si tiene la forma de 0<x uso una exponencial
      - -inf<x<inf uso normal
    2) despejo h(x)
    3) maximizo c (valuo en los extremos, derivo h(x) e igualo a 0 y despejo x)
    4) valuo h(x) donde maximiza c (valor encontrado en 3)
    5) reemplazo en h(x) c por su valor maximo y simplifico
    6) h(x) será la guarda con la que comparo en el if con x generado segun g(x)
    """
    while True:
        X = geometrica_SIM(1/3)
        U = random()
        if U < (1/2 - 1/2**(X-1)):
            return X


print(f"El resultado ejercicio 1 es: {ej_1()}")
print(f"El resultado ejercicio 2 es: {ej_2(10000)}")
print(f"El resultado ejercicio 3 es: {ej_3(10000)}")
print(f"El resultado ejercicio 4 es: {ej_4(10000,4)}")
