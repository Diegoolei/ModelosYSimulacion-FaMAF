from random import random
from math import inf, log


def init(N, lambda_F):
    t, r = 0, 0
    t_rep = inf
    X = []
    for _ in range(N):
        exp_distr = -log(random())/lambda_F
        X.append(exp_distr)
    X.sort()
    return X, t, r, t_rep


def un_operario(N, lambda_F, lambda_R, s):
    X, t, r, t_rep = init(N, lambda_F)
    while True:
        # Caso 1
        if X[0] < t_rep:
            t = X[0]
            r += 1
            if r == s + 1:
                return t
            if r < s + 1:
                exp_distr = -log(random())/lambda_F
                X[0] = t + exp_distr
                X.sort()
            if r == 1:
                t_rep = t - log(random())*lambda_R

        # Caso 2
        if t_rep < X[0]:
            t = t_rep
            r -= 1
            if r > 0:
                t_rep = t - log(random())*lambda_R
            if r == 0:
                t_rep = inf
