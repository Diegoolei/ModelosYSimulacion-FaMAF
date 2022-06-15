from random import random
from math import inf, log


def init(N, lambda_F):
    t, r = 0, 0
    t_rep = [inf, inf]
    X = []
    for _ in range(N):
        exp_distr = -log(random())/lambda_F
        X.append(exp_distr)
    X.sort()
    return X, t, r, t_rep


def dos_operarios(N, lambda_F, lambda_R, s):
    X, t, r, t_rep = init(N, lambda_F)
    repuestos = s
    while True:
        # Caso 1
        if X[0] < t_rep[0]:
            t = X[0]
            r += 1
            if r == repuestos + 1:
                return t
            if r < repuestos + 1:
                exp_distr = -log(random())/lambda_F
                X[0] = t + exp_distr
                X.sort()
            if r == 1:
                t_rep[0] = t - log(random())*lambda_R
                t_rep.sort()
            if r == 2:
                t_rep[1] = t - log(random())*lambda_R
                t_rep.sort()
        # Caso 2
        if t_rep[0] < X[0]:
            t = t_rep[0]
            r -= 1
            if r > 1:
                t_rep[0] = t - log(random())*lambda_R
            else:
                t_rep[0] = inf
            t_rep.sort()
