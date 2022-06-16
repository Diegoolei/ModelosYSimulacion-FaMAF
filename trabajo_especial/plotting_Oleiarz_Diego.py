import un_operario_Oleiarz_Diego as UOP
import dos_operarios_Oleiarz_Diego as DOP
import matplotlib.pyplot as plot

from statistics import pstdev


def media(n, f):
    suma = 0
    for _ in range(n):
        suma += f(7, 3, 1, 1/8)
    return (suma/n)


def desviacion(n, f):
    dev = []
    for _ in range(n):
        x = f(7, 3, 1, 1/8)
        dev.append(x)
    return pstdev(dev)

##print(media(10000, UOP.un_operario))
##print(media(10000, DOP.dos_operarios))

#print(desviacion(10000, UOP.un_operario))
#print(desviacion(10000, DOP.dos_operarios))


def histograma_conjunto(n):
    un_op_tres_rep = [UOP.un_operario(7, 3, 1, 1/8) for _ in range(n)]
    un_op_cuatro_rep = [UOP.un_operario(7, 4, 1, 1/8) for _ in range(n)]
    dos_op_tres_rep = [DOP.dos_operarios(7, 3, 1, 1/8) for _ in range(n)]
    dos_op_cuatro_rep = [DOP.dos_operarios(7, 4, 1, 1/8) for _ in range(n)]

    intervalos = range(0, 40)

    plot.hist([un_op_tres_rep, un_op_cuatro_rep, dos_op_tres_rep, dos_op_cuatro_rep], bins=intervalos, label=[
              f'1 operario, 3 repuestos', f'1 operario, 4 repuestos', f'2 operarios, 3 repuestos', f'2 operarios, 4 repuestos'], color=['#191919', '#AFA98D', '#22AED1', '#6D8EA0'], rwidth=0.85)
    plot.xticks(intervalos)
    plot.xlabel('Tiempo Transcurrido (meses)')
    plot.ylabel('Cantidad de simulaciones')
    plot.title(f'Frecuencia de fallos en meses para {n} simulaciones')
    plot.legend()
    plot.show()


histograma_conjunto(10000)


def histograma_un_operario(n):
    un_op_tres_rep = [UOP.un_operario(7, 3, 1, 1/8) for _ in range(n)]
    un_op_cuatro_rep = [UOP.un_operario(7, 4, 1, 1/8) for _ in range(n)]

    intervalos = range(0, 20)

    plot.hist([un_op_tres_rep, un_op_cuatro_rep], bins=intervalos, label=[
              f'1 operario, 3 repuestos', f'1 operario, 4 repuestos'], color=['#191919', '#AFA98D'], rwidth=0.85)
    plot.xticks(intervalos)
    plot.xlabel('Tiempo Transcurrido (meses)')
    plot.ylabel('Cantidad de simulaciones')
    plot.title(f'Frecuencia de fallos en meses para {n} simulaciones')
    plot.legend()
    plot.show()


histograma_un_operario(10000)


def histograma_dos_operarios(n):
    dos_op_tres_rep = [DOP.dos_operarios(7, 3, 1, 1/8) for _ in range(n)]
    dos_op_cuatro_rep = [DOP.dos_operarios(7, 4, 1, 1/8) for _ in range(n)]

    intervalos = range(0, 40)

    plot.hist([dos_op_tres_rep, dos_op_cuatro_rep], bins=intervalos, label=[
              f'2 operario, 3 repuestos', f'2 operario, 4 repuestos'], color=['#22AED1', '#6D8EA0'], rwidth=2)
    plot.xticks(intervalos)
    plot.xlabel('Tiempo Transcurrido (meses)')
    plot.ylabel('Cantidad de simulaciones')
    plot.title(f'Frecuencia de fallos en meses para {n} simulaciones')
    plot.legend()
    plot.show()


histograma_dos_operarios(10000)