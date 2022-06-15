import un_operario_Oleiarz_Diego as UOP
import dos_operarios_Oleiarz_Diego as DOP

from statistics import pstdev

def estimar_esperanza(n, f):
    suma = 0
    for _ in range(n):
        suma += f(7, 1, 1/8, 3)
    return (suma/n)


def estimar_desvio(n, f):
    simulaciones = [f(7, 1, 1/8, 3) for _ in range(n)]
    return pstdev(simulaciones)

print(estimar_esperanza(10000, UOP.un_operario(7 ,1, 1/8, 3)))
print(estimar_esperanza(10000, DOP.dos_operarios(7, 1, 1/8, 3)))