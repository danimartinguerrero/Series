"""Utilidades gráficas comunes a los clips."""
from estilo import *


def curva_recortada(ax, f, x_min, x_max, y_min, y_max, color, ancho=4, n=900):
    """Gráfica de f en [x_min, x_max] sólo donde y ∈ [y_min, y_max].

    Corta la curva en el borde de la ventana (interpolando el punto exacto de
    salida), en lugar de aplastarla contra él. Devuelve un VGroup de tramos.
    """
    xs = np.linspace(x_min, x_max, n)
    with np.errstate(all="ignore"):
        ys = np.array([f(x) for x in xs], dtype=float)
    dentro = np.isfinite(ys) & (ys >= y_min) & (ys <= y_max)
    tramos, actual = [], []

    def borde(x0, y0, x1, y1):
        yb = y_max if (y1 > y_max or y0 > y_max) else y_min
        if not (np.isfinite(y0) and np.isfinite(y1)) or y1 == y0:
            return None
        t = (yb - y0) / (y1 - y0)
        return (x0 + t * (x1 - x0), yb)

    for i in range(n):
        if dentro[i]:
            if not actual and i > 0:
                p = borde(xs[i], ys[i], xs[i - 1], ys[i - 1])
                if p is not None:
                    actual.append(p)
            actual.append((xs[i], ys[i]))
        else:
            if actual:
                p = borde(xs[i - 1], ys[i - 1], xs[i], ys[i])
                if p is not None:
                    actual.append(p)
                tramos.append(actual)
                actual = []
    if actual:
        tramos.append(actual)
    grupo = VGroup()
    for tr in tramos:
        if len(tr) < 2:
            continue
        v = VMobject(stroke_color=color, stroke_width=ancho)
        v.set_points_as_corners([ax.c2p(x, y) for x, y in tr])
        grupo.add(v)
    return grupo


def etiqueta_fondo(mob, buff=0.08, opacidad=0.85):
    """Rótulo sobre fondo oscuro translúcido (para colocar sobre imágenes)."""
    r = BackgroundRectangle(mob, color=FONDO, fill_opacity=opacidad, buff=buff,
                            corner_radius=0.06)
    return VGroup(r, mob)


def cruz(punto, color=BLANCO, tam=0.16, ancho=5):
    return VGroup(
        Line(punto + tam * (UL), punto + tam * (DR), stroke_width=ancho, color=color),
        Line(punto + tam * (UR), punto + tam * (DL), stroke_width=ancho, color=color),
    )


def nodo_coef(tex, color=GRISMEDIO, radio=0.36, size=30):
    c = Circle(radius=radio, stroke_color=color, stroke_width=3,
               fill_color=CAJA, fill_opacity=1)
    t = M(tex, size=size)
    t.move_to(c)
    return VGroup(c, t)


def ajustar(mob, ancho=7.4):
    """Reduce el objeto si excede el ancho útil (zona segura de TikTok)."""
    if mob.width > ancho:
        mob.scale_to_fit_width(ancho)
    return mob
