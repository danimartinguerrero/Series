"""Estilo común de los clips verticales del Tema 5 (Manim Community).

Paleta y tipografía idénticas a las de los apuntes en LaTeX: fondo negro,
texto claro en Computer Modern, acentos cian / violeta / ámbar.

Formato: 1080 x 1920 (9:16), 60 fps. El marco mide 9 x 16 unidades
(120 px por unidad). Zonas seguras para la interfaz de TikTok: el contenido
importante se mantiene en x ∈ [-4.1, 3.3] e y ∈ [-4.6, 6.6].
"""
from manim import *
import numpy as np

# --- Configuración del vídeo ----------------------------------------------------
import os
_PREVIA = os.environ.get("CLIP_PREVIA") == "1"   # render rápido de prueba
config.pixel_width = 540 if _PREVIA else 1080
config.pixel_height = 960 if _PREVIA else 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 15 if _PREVIA else 60
config.background_color = "#000000"
if not _PREVIA:   # codificación de alta calidad (x264, CRF 14, ajuste para animación)
    config.video_encoder_options = {"crf": "14", "preset": "slow", "tune": "animation"}

# --- Paleta del documento -------------------------------------------------------
FONDO = "#000000"
TEXTO = "#ECECEC"
BLANCO = "#FFFFFF"
GRIS = "#9CA0A8"
GRISMEDIO = "#5B5F67"
GRISOSCURO = "#2E3036"
CAJA = "#0E1014"
CIAN = "#20B4CE"
VIOLETA = "#A48BFA"
AMBAR = "#F4B740"
MAGENTA = "#E5579D"
VERDE = "#4FD68A"
NARANJA = "#FA8F45"
ROJO = "#F25F5C"
PROGRESION = ["#3C5AFF", "#2D91F0", "#1EC8E6", "#3CDC5A", "#FAE628",
              "#FF9614", "#FF283C", "#BE3CF0"]

# --- LaTeX: Computer Modern, como en los apuntes -------------------------------------
PLANTILLA = TexTemplate()
PLANTILLA.add_to_preamble(r"""
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,mathtools,bm}
\DeclareMathOperator{\sen}{sen}
\DeclareMathOperator{\artanh}{artanh}
\DeclareMathOperator{\Ai}{Ai}
\DeclareMathOperator{\Bi}{Bi}
\newcommand{\dist}{\operatorname{dist}}
""")
MathTex.set_default(tex_template=PLANTILLA, color=TEXTO)
Tex.set_default(tex_template=PLANTILLA, color=TEXTO)

SERIE_TITULO = r"Ecuaciones Diferenciales \,$\cdot$\, Tema 4"
SUBTITULO_SERIE = r"Parte I $\cdot$ Funciones de Green"
AUTOR = r"Daniel Martín Guerrero"


def M(tex, size=44, color=TEXTO, **kw):
    """Fórmula en modo matemático."""
    return MathTex(tex, font_size=size, color=color, **kw)


def T(tex, size=36, color=TEXTO, **kw):
    """Texto en modo texto (LaTeX)."""
    return Tex(tex, font_size=size, color=color, **kw)


def cabecera(numero, total, titulo):
    """Cabecera fija: serie (versalitas), número de clip, título y regla cian."""
    serie = T(r"\textsc{" + SERIE_TITULO + "}", size=26, color=GRIS)
    serie.to_edge(UP, buff=0.95).to_edge(LEFT, buff=0.55)
    num = T(r"\textsc{%02d\,/\,%02d}" % (numero, total), size=26, color=CIAN)
    num.move_to(serie).to_edge(RIGHT, buff=0.55)
    tit = T(r"\bfseries " + titulo, size=50, color=BLANCO)
    if tit.width > 7.9:
        tit.scale_to_fit_width(7.9)
    tit.next_to(serie, DOWN, buff=0.42).to_edge(LEFT, buff=0.55)
    regla = Line(LEFT, RIGHT, stroke_width=3, color=CIAN).set_length(1.6)
    regla.next_to(tit, DOWN, buff=0.28).align_to(tit, LEFT)
    return VGroup(serie, num, tit, regla)


def pie():
    """Pie discreto (por debajo de la zona importante)."""
    t = T(r"\textsc{" + SUBTITULO_SERIE + "}", size=22, color=GRISMEDIO)
    t.to_edge(DOWN, buff=0.75)
    return t


def caja(mob, color=AMBAR, buff=0.32, titulo=None):
    """Caja redondeada con pestaña de título, como en los apuntes."""
    rect = RoundedRectangle(corner_radius=0.12, width=mob.width + 2 * buff,
                            height=mob.height + 2 * buff, stroke_color=color,
                            stroke_width=2.4, fill_color=CAJA, fill_opacity=1)
    rect.move_to(mob)
    grupo = VGroup(rect, mob)
    if titulo is not None:
        et = T(r"\sffamily\bfseries " + titulo, size=24, color=FONDO)
        pest = RoundedRectangle(corner_radius=0.07, width=et.width + 0.3,
                                height=et.height + 0.18, stroke_width=0,
                                fill_color=color, fill_opacity=1)
        pest.move_to(rect.get_corner(UL) + RIGHT * (pest.width / 2 + 0.25))
        et.move_to(pest)
        grupo.add(pest, et)
    return grupo


def nota(tex, size=30, color=GRIS):
    return T(tex, size=size, color=color)


def ejes(x_range, y_range, x_length=7.2, y_length=4.6, **kw):
    """Ejes con el estilo de las figuras del documento."""
    ax = Axes(x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
              axis_config=dict(color=GRISMEDIO, stroke_width=2, include_tip=False,
                               font_size=22, decimal_number_config=dict(color=GRIS)),
              **kw)
    return ax


def cierre(scene, mensaje, conservar=()):
    """Tarjeta final común: mensaje clave y firma."""
    firma = VGroup(
        T(r"\textsc{Apuntes formalizados}", size=24, color=CIAN),
        T(AUTOR, size=28, color=TEXTO),
    ).arrange(DOWN, buff=0.12)
    firma.to_edge(DOWN, buff=1.9)
    return firma


# --- Mapa de colores cíclico de fase (el del documento) -------------------------------
_FASE = np.array([(255, 40, 60), (255, 150, 20), (250, 230, 40), (60, 220, 90),
                  (30, 200, 230), (60, 90, 255), (190, 60, 240), (255, 40, 60)],
                 dtype=float) / 255.0


def color_fase(theta):
    """theta en (-pi, pi] -> RGB (array N x 3)."""
    t = (np.asarray(theta) + np.pi) / (2 * np.pi) * (len(_FASE) - 1)
    i = np.clip(np.floor(t).astype(int), 0, len(_FASE) - 2)
    f = (t - i)[..., None]
    return _FASE[i] * (1 - f) + _FASE[i + 1] * f


def imagen_fase(func, xr, yr, res=900, brillo=0.9):
    """ImageMobject con el retrato de fase de func en [xr] x [yr]."""
    nx = res
    ny = int(res * (yr[1] - yr[0]) / (xr[1] - xr[0]))
    x = np.linspace(xr[0], xr[1], nx)
    y = np.linspace(yr[1], yr[0], ny)
    X, Y = np.meshgrid(x, y)
    with np.errstate(all="ignore"):
        F = func(X + 1j * Y)
    rgb = color_fase(np.angle(F)) * brillo
    img = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return ImageMobject(img)
