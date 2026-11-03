#!/usr/bin/env python3
"""Genera las tablas numéricas (datos/*.dat) que usan las figuras pgfplots.

Todas las curvas se obtienen sumando las propias series de potencias del
texto en aritmética decimal de alta precisión (50 cifras), de modo que las
gráficas reproducen exactamente las soluciones construidas en el documento.
Uso:  python3 scripts/generar_datos.py   (desde la carpeta tema5_latex)
"""
from decimal import Decimal as D, getcontext
from pathlib import Path

getcontext().prec = 60
OUT = Path(__file__).resolve().parent.parent / "datos"
OUT.mkdir(exist_ok=True)


def rango(a, b, h):
    a, b, h = D(a), D(b), D(h)
    n = int(round((b - a) / h))
    return [D(a) + D(h) * i for i in range(n + 1)]


def serie(coefs, x):
    s, xp = D(0), D(1)
    for c in coefs:
        s += c * xp
        xp *= x
    return s


def coef_recurrencia(a0, a1, regla, N):
    """a_{n+2} = regla(n, a) con a = lista de coeficientes previos."""
    a = [D(a0), D(a1)]
    for n in range(N - 2):
        a.append(regla(n, a))
    return a


def escribir(nombre, cabecera, filas):
    with open(OUT / nombre, "w") as f:
        f.write(cabecera + "\n")
        for fila in filas:
            f.write(" ".join(f"{float(v):.8g}" for v in fila) + "\n")


# --- Airy: (n+2)(n+1) a_{n+2} = a_{n-1},  a_2 = 0 --------------------------
def airy(n, a):
    if n == 0:
        return D(0)
    return a[n - 1] / ((n + 2) * (n + 1))

N = 260
A1 = coef_recurrencia(1, 0, airy, N)
A2 = coef_recurrencia(0, 1, airy, N)
escribir("airy.dat", "x y1 y2",
         [(x, serie(A1, x), serie(A2, x)) for x in rango("-9", "2.4", "0.01")])

# --- y'' + x y' + y = 0:  a_{n+2} = -a_n/(n+2) -------------------------------
def ej1(n, a):
    return -a[n] / (n + 2)

N = 200
E1 = coef_recurrencia(1, 0, ej1, N)
E2 = coef_recurrencia(0, 1, ej1, N)
escribir("ejemplo_gauss.dat", "x y1 y2",
         [(x, serie(E1, x), serie(E2, x)) for x in rango("-5", "5", "0.02")])

# --- Legendre l = 1: a_{n+2} = (n-1)/(n+1) a_n --------------------------------
# y1 = 1 - x artanh x ; sumas parciales S_N = 1 - sum_{k=1}^{N} x^{2k}/(2k-1)
filas = []
for x in rango("-0.995", "0.995", "0.005"):
    fila = [x]
    for M in (1, 2, 4, 8):
        fila.append(D(1) - sum(x ** (2 * k) / (2 * k - 1) for k in range(1, M + 1)))
    filas.append(fila)
escribir("legendre_l1_parciales.dat", "x S1 S2 S4 S8", filas)
print("Datos generados en", OUT)
