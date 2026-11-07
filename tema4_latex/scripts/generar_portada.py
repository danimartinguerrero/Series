#!/usr/bin/env python3
"""Renderiza la imagen de la portada: superposición de respuestas a impulsos.

Una fuente b(s) se trocea en impulsos situados en s_k. Cada impulso produce
la respuesta b(s_k) G(x - s_k), con G la función de Green causal del
oscilador amortiguado y'' + 2γ y' + ω² y = δ:

    G(t) = Θ(t) · exp(-γ t) · sen(Ω t) / Ω,      Ω = sqrt(ω² - γ²).

Las respuestas se dibujan en «cascada» (una lámina por impulso, coloreadas
de forma progresiva) y, en primer plano, su superposición
y_p(x) = Σ_k b(s_k) G(x - s_k) Δs, que es la solución particular.
Salida: figuras/portada_superficie.png (fondo transparente, 600 ppp).

Uso:  python3 scripts/generar_portada.py   (desde la carpeta tema4_latex)
Requiere numpy, matplotlib y Pillow.
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "figuras" / "portada_superficie.png"

GAMMA, OMEGA0 = 0.16, 1.0
OM = np.sqrt(OMEGA0**2 - GAMMA**2)
G = lambda t: np.where(t > 0, np.exp(-GAMMA * t) * np.sin(OM * t) / OM, 0.0)

XMAX = 22.0
x = np.linspace(0.0, XMAX, 2200)
N = 15
s_k = np.linspace(0.3, 5.3, N)
ds = s_k[1] - s_k[0]
b = lambda s: np.sin(np.pi * s / 5.6) ** 2

respuestas = [b(sk) * G(x - sk) for sk in s_k]
yp = ds * np.sum(respuestas, axis=0)

mapa = LinearSegmentedColormap.from_list("prog", [
    (60/255, 90/255, 255/255), (30/255, 200/255, 230/255), (60/255, 220/255, 90/255),
    (250/255, 230/255, 40/255), (255/255, 150/255, 20/255), (255/255, 40/255, 60/255),
    (190/255, 60/255, 240/255)], N=512)

fig = plt.figure(figsize=(10.0, 6.0), dpi=600)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1], projection="3d")
ax.set_facecolor((0, 0, 0, 0))

ESC = 1.0          # escala vertical de cada respuesta
SEP = 1.0          # separación entre láminas
z0 = 0.0

def lamina(y_curva, prof, color, alfa_relleno, ancho, z_base=z0):
    verts = [(xi, prof, zi) for xi, zi in zip(x, y_curva)]
    poly = [(x[0], prof, z_base)] + verts + [(x[-1], prof, z_base)]
    ax.add_collection3d(Poly3DCollection([poly], facecolors=[(*color[:3], alfa_relleno)],
                                         edgecolors="none"))
    segs = [[verts[i], verts[i + 1]] for i in range(len(verts) - 1)]
    ax.add_collection3d(Line3DCollection(segs, colors=[color], linewidths=ancho))

# Láminas del fondo al frente: la más lejana es el último impulso
for k in range(N - 1, -1, -1):
    c = mapa(k / (N - 1))
    lamina(ESC * respuestas[k], SEP * (k + 3), c, 0.30, 1.1)
    # marca del impulso (delta) en s_k
    ax.plot([s_k[k], s_k[k]], [SEP * (k + 3)] * 2, [z0, z0 + 0.2 + 1.1 * b(s_k[k])],
            color=c, linewidth=1.4, alpha=0.95)

# Superposición en primer plano (escalada para comparar formas)
yp_esc = yp / np.abs(yp).max() * 1.05
lamina(yp_esc, 0.0, (1.0, 1.0, 1.0, 1.0), 0.0, 2.2)

ax.view_init(elev=26, azim=-62)
ax.set_box_aspect((2.3, 1.25, 0.42))
ax.set_xlim(0, XMAX); ax.set_ylim(-0.5, SEP * (N + 3)); ax.set_zlim(-1.05, 1.2)
ax.set_axis_off()
fig.savefig(SALIDA, transparent=True, dpi=600, bbox_inches="tight", pad_inches=0.0)

im = Image.open(SALIDA)
x0, y0, x1, y1 = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
m = 18
im.crop((max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, im.width), min(y1 + m, im.height))).save(SALIDA, optimize=True)
print("Portada generada en", SALIDA)
