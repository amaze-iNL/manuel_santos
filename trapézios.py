import math

# Exercício 1: Regra dos Trapézios simples

def T(f, c, d):
    return (d - c) * (f(c) + f(d)) / 2

# Exercício 2 e 3: Regra dos Trapézios iterativa

def Tn_iter(f, c, d, n):
    intervals = [(c, d)]
    for _ in range(n):
        new_intervals = []
        for (start, end) in intervals:
            mid = (start + end) / 2
            new_intervals.append((start, mid))
            new_intervals.append((mid, end))
        intervals = new_intervals

    total = 0
    for (start, end) in intervals:
        total += T(f, start, end)
    return total

# Exercício 4: Abordagem à força bruta

def força_bruta_Tn(f, c, d, max_iter=1000):
    n = 0
    T_prev = Tn_iter(f, c, d, n)
    while n < max_iter:
        n += 1
        T_curr = Tn_iter(f, c, d, n)
        if abs(T_curr - T_prev) < 1e-12:
            return T_curr, n
        T_prev = T_curr
    return None, n

# Exercício 5: Regra de Simpson simples

def S(f, c, d):
    mid = (c + d) / 2
    return (d - c) / 6 * (f(c) + 4*f(mid) + f(d))

# Exercício 6: Regra de Simpson recursiva

def Sn_rec(f, c, d, n):
    if n == 0:
        return S(f, c, d)
    else:
        mid = (c + d) / 2
        return Sn_rec(f, c, mid, n-1) + Sn_rec(f, mid, d, n-1)

# Exercício 7: Abordagem Greedy

def greedy_Tn(f, c, d, epsilon=1e-6, max_n=30):
    T_prev = Tn_iter(f, c, d, 0)
    for n in range(1, max_n):
        T_curr = Tn_iter(f, c, d, n)
        S_curr = Sn_rec(f, c, d, n)
        if abs(T_curr - T_prev) < epsilon and abs(T_curr - S_curr) < epsilon:
            return T_curr, n
        T_prev = T_curr
    return None, max_n

# Exercício 8: Backtracking

def greedy_salto_Tn(f, c, d, epsilon=1e-6, max_n=30):
    n = 1
    T_prev = Tn_iter(f, c, d, 0)
    while n < max_n:
        T_curr = Tn_iter(f, c, d, n)
        S_curr = Sn_rec(f, c, d, n)
        if abs(T_curr - T_prev) < epsilon and abs(T_curr - S_curr) < epsilon:
            return T_curr, n
        T_prev = T_curr
        n *= 2  # Salto de n para 2n
    return None, max_n

# Exercício 9: Abordagem dinâmica

def adaptativo_T(f, c, d, epsilon=1e-6, n=0, max_depth=20, f_cache=None):
    if f_cache is None:
        f_cache = {}

    def memo_f(x):
        if x not in f_cache:
            f_cache[x] = f(x)
        return f_cache[x]

    mid = (c + d) / 2
    T_simple = (d - c) * (memo_f(c) + memo_f(d)) / 2
    S_simple = (d - c) / 6 * (memo_f(c) + 4 * memo_f(mid) + memo_f(d))

    if abs(T_simple - S_simple) < epsilon or n >= max_depth:
        return S_simple
    else:
        left = adaptativo_T(f, c, mid, epsilon/2, n+1, max_depth, f_cache)
        right = adaptativo_T(f, mid, d, epsilon/2, n+1, max_depth, f_cache)
        return left + right


# Função de teste

def f(x):
    return math.sin(x)

# Intervalo de integração
c = 0
d = math.pi
