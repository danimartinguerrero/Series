#!/usr/bin/env python3
"""Genera datos/superposicion.dat para la figura de superposición de impulsos.

Operador: y'' + 2γ y' + ω² y (ω = 1, γ = 0.16); función de Green causal
G(t) = Θ(t) e^{-γt} sen(Ωt)/Ω. Fuente b(s) = sen²(π s / 5.6) en [0, 5.6].
Columnas: x, b(x), r_1..r_K (respuestas b(s_k) G(x - s_k) Δs a los K impulsos),
suma discreta de las r_k y solución exacta y_p = ∫ G(x - s) b(s) ds.
Uso:  python3 scripts/generar_datos.py   (desde la carpeta tema4_latex)
"""
from pathlib import Path
import numpy as np

GAMMA, OMEGA0 = 0.16, 1.0
OM = np.sqrt(OMEGA0**2 - GAMMA**2)
SOP = 5.6
K = 8

def G(t):
    return np.where(t > 0, np.exp(-GAMMA * t) * np.sin(OM * t) / OM, 0.0)

def b(s):
    return np.where((s >= 0) & (s <= SOP), np.sin(np.pi * s / SOP) ** 2, 0.0)

x = np.linspace(0.0, 20.0, 801)
ds = SOP / K
s_k = (np.arange(K) + 0.5) * ds
r = np.array([b(sk) * G(x - sk) * ds for sk in s_k])
suma = r.sum(axis=0)
# integral «exacta» por cuadratura fina (regla del punto medio, 20000 nodos)
sf = (np.arange(20000) + 0.5) * SOP / 20000
yp = np.array([np.sum(b(sf) * G(xi - sf)) * SOP / 20000 for xi in x])

datos = np.column_stack([x, b(x), *r, suma, yp])
cab = "x b " + " ".join(f"r{k+1}" for k in range(K)) + " suma yp"
out = Path(__file__).resolve().parent.parent / "datos" / "superposicion.dat"
np.savetxt(out, datos, fmt="%.6g", header=cab, comments="")
print("Escrito", out, "| impulsos en", np.round(s_k, 3))
