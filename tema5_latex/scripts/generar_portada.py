#!/usr/bin/env python3
"""Renderiza la superficie de la portada: |f(z)| para f(z) = 1/(1+z^2),
coloreada según la fase arg f(z) e iluminada con una fuente de luz para dar
relieve. Salida: figuras/portada_superficie.png (fondo transparente).

Uso:  python3 scripts/generar_portada.py   (desde la carpeta tema5_latex)
Requiere numpy y matplotlib.
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LightSource

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "figuras" / "portada_superficie.png"

# --- Malla: más densa cerca de los polos z = ±i --------------------------------
def malla_estirada(n, centros, ancho=0.35, intensidad=4.0):
    """Nodos en [-2, 2] concentrados alrededor de los valores de «centros»."""
    t = np.linspace(-2.0, 2.0, 20 * n)
    dens = np.ones_like(t)
    for c in centros:
        dens += intensidad * np.exp(-((t - c) / ancho) ** 2)
    acum = np.concatenate([[0.0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(t))])
    acum /= acum[-1]
    return np.interp(np.linspace(0.0, 1.0, n), acum, t)

x = malla_estirada(520, [0.0])
y = malla_estirada(620, [-1.0, 1.0])
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y
F = 1.0 / (1.0 + Z ** 2 + 1e-12)

H = 5.2                                   # altura de corte de los picos
modulo = np.minimum(np.abs(F), H)
fase = np.angle(F)                         # en (-pi, pi]

# --- Colores: mismo mapa cíclico «fase» que las figuras del documento ---------
fase_cmap = LinearSegmentedColormap.from_list("fase", [
    (255/255, 40/255, 60/255), (255/255, 150/255, 20/255), (250/255, 230/255, 40/255),
    (60/255, 220/255, 90/255), (30/255, 200/255, 230/255), (60/255, 90/255, 255/255),
    (190/255, 60/255, 240/255), (255/255, 40/255, 60/255)], N=1024)
rgb = fase_cmap((fase + np.pi) / (2 * np.pi))[..., :3]

# Iluminación (sombreado suave según la normal de la superficie)
luz = LightSource(azdeg=300, altdeg=38)
rgb = luz.shade_rgb(rgb, modulo, vert_exag=0.35, blend_mode="soft", fraction=1.0)

# Rejilla sutil sobre la superficie (oscureciendo filas/columnas regulares,
# lo que respeta el orden de profundidad, a diferencia de una malla aparte)
def lineas(v, paso=0.25, grosor=0.0045):
    r = np.abs((v + 2.0) / paso - np.round((v + 2.0) / paso)) * paso
    return r < grosor
mascara = lineas(X) | lineas(Y)
rgb[mascara] *= 0.80

# --- Render ------------------------------------------------------------------
fig = plt.figure(figsize=(9.0, 6.2), dpi=600)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1], projection="3d")
ax.set_facecolor((0, 0, 0, 0))
ax.plot_surface(X, Y, modulo, facecolors=rgb, rstride=1, cstride=1,
                linewidth=0, antialiased=False, shade=False)
ax.view_init(elev=24, azim=-118)
ax.set_box_aspect((1.0, 1.0, 0.78))
ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(0, H)
ax.set_axis_off()
fig.savefig(SALIDA, transparent=True, dpi=600, bbox_inches="tight", pad_inches=0.0)
# Recorte al contenido (canal alfa) con un pequeño margen
from PIL import Image
im = Image.open(SALIDA)
x0, y0, x1, y1 = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
m = 18
im.crop((max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, im.width), min(y1 + m, im.height))).save(SALIDA, optimize=True)
print("Portada generada en", SALIDA)
