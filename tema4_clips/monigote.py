"""Monigote articulado y efectos para animaciones de combate en Manim.

El monigote es un esqueleto de cinemática directa: su postura es un
diccionario de parámetros (posición de la cadera, inclinación del tronco,
ángulos de brazos y piernas, giro global) que se interpola linealmente con
la animación Postura. Los ángulos de las extremidades se miden desde la
vertical hacia abajo y son positivos hacia donde mira el personaje.
"""
from estilo import *

# Longitudes del esqueleto (unidades de escena)
ESCALA = 1.3
TRONCO, CABEZA = 0.95 * ESCALA, 0.25 * ESCALA
BRAZO, ANTEBRAZO = 0.52 * ESCALA, 0.46 * ESCALA
MUSLO, PIERNA = 0.58 * ESCALA, 0.56 * ESCALA
ALTURA_CADERA = MUSLO + PIERNA - 0.04    # cadera sobre el suelo con piernas casi rectas

# Posturas base (ángulos en radianes)
GUARDIA = dict(lean=0.12, ra1=0.9, ra2=1.9, la1=0.5, la2=2.2,
               rl1=0.35, rl2=-0.15, ll1=-0.3, ll2=-0.35, spin=0.0)
REPOSO = dict(lean=0.0, ra1=0.15, ra2=0.15, la1=-0.15, la2=-0.15,
              rl1=0.12, rl2=0.0, ll1=-0.12, ll2=0.0, spin=0.0)
AGACHADO = dict(lean=0.35, ra1=1.1, ra2=1.6, la1=0.4, la2=1.9,
                rl1=1.2, rl2=-1.1, ll1=-0.2, ll2=-1.6, spin=0.0)
LANZAR_CARGA = dict(lean=-0.25, ra1=-2.4, ra2=-2.9, la1=0.9, la2=1.4,
                    rl1=0.5, rl2=-0.1, ll1=-0.45, ll2=-0.2, spin=0.0)
LANZAR_FIN = dict(lean=0.35, ra1=1.75, ra2=1.6, la1=-0.4, la2=-0.2,
                  rl1=0.65, rl2=-0.2, ll1=-0.35, ll2=-0.5, spin=0.0)
BRAZOS_ARRIBA = dict(lean=-0.05, ra1=2.7, ra2=2.9, la1=-2.7, la2=-2.9,
                     rl1=0.25, rl2=0.0, ll1=-0.25, ll2=0.0, spin=0.0)
ESCUDO = dict(lean=0.18, ra1=1.55, ra2=1.55, la1=1.35, la2=1.75,
              rl1=0.55, rl2=-0.35, ll1=-0.45, ll2=-0.25, spin=0.0)
GOLPE_SUELO = dict(lean=0.75, ra1=0.55, ra2=0.4, la1=0.3, la2=0.6,
                   rl1=1.25, rl2=-1.2, ll1=-0.35, ll2=-1.4, spin=0.0)
PUNETAZO = dict(lean=0.2, ra1=1.6, ra2=1.6, la1=0.6, la2=2.3,
                rl1=0.55, rl2=-0.1, ll1=-0.45, ll2=-0.3, spin=0.0)


def _dir(ang, f):
    """Vector unitario a 'ang' de la vertical hacia abajo, hacia el frente f."""
    return np.array([f * np.sin(ang), -np.cos(ang), 0.0])


class Monigote(VGroup):
    def __init__(self, color, x, suelo, mira=1, simbolo=None, escala=1.0, grosor=11,
                 tam_cabeza=2.45, **postura):
        super().__init__()
        self.simbolo = simbolo
        self.k = escala
        self.color_base = color
        self.mira = mira
        self.pose = dict(REPOSO)
        self.pose.update(x=x, y=suelo + ALTURA_CADERA * escala)
        self.pose.update(postura)
        self.segs = [Line(ORIGIN, RIGHT, stroke_width=grosor, color=color) for _ in range(9)]
        self.halo = [Line(ORIGIN, RIGHT, stroke_width=grosor * 2.9, color=color, stroke_opacity=0.16)
                     for _ in range(9)]
        self.cabeza = Circle(radius=CABEZA * escala, stroke_width=grosor * 0.9, color=color,
                             fill_color=FONDO, fill_opacity=1)
        self.halo_cab = Circle(radius=CABEZA * escala + 0.07, stroke_width=0, fill_color=color,
                               fill_opacity=0.18)
        self.ojo = Dot(radius=0.055, color=color)
        for l in self.segs + self.halo:
            l.set_cap_style(CapStyleType.ROUND)
        if simbolo is None:
            self.add(*self.halo, self.halo_cab, *self.segs, self.cabeza, self.ojo)
        else:
            # cabeza = glifo (Computer Modern) con halo; se reconstruye girado en cada fotograma
            self.glifo_base = MathTex(simbolo, color=color, tex_template=PLANTILLA)
            self.glifo_base.set_height(tam_cabeza * CABEZA * escala)
            self.glifo_base.set_stroke(color, width=1.2)
            self.halo_base = self.glifo_base.copy().set_fill(opacity=0).set_stroke(color, width=16,
                                                                                  opacity=0.22)
            self.glifo_base.set_z_index(5)
            self.halo_base.set_z_index(5)
            self.cabeza = self.glifo_base.copy()
            self.halo_cab = self.halo_base.copy()
            self.add(*self.halo, self.halo_cab, *self.segs, self.cabeza)
        self.set_z_index(5)
        self.actualizar()

    # --- cinemática directa ----------------------------------------------------------
    def articulaciones(self):
        p, f, k = self.pose, self.mira, self.k
        cadera = np.array([p["x"], p["y"], 0.0])
        arriba = np.array([f * np.sin(p["lean"]), np.cos(p["lean"]), 0])
        cuello = cadera + k * TRONCO * arriba
        cab = cuello + k * (CABEZA + 0.04) * arriba
        hombro = cuello - k * 0.06 * arriba
        j = dict(cadera=cadera, cuello=cuello, cabeza=cab)
        j["codo_d"] = hombro + k * BRAZO * _dir(p["ra1"], f)
        j["mano_d"] = j["codo_d"] + k * ANTEBRAZO * _dir(p["ra2"], f)
        j["codo_i"] = hombro + k * BRAZO * _dir(p["la1"], f)
        j["mano_i"] = j["codo_i"] + k * ANTEBRAZO * _dir(p["la2"], f)
        j["rodilla_d"] = cadera + k * MUSLO * _dir(p["rl1"], f)
        j["pie_d"] = j["rodilla_d"] + k * PIERNA * _dir(p["rl1"] + p["rl2"], f)
        j["rodilla_i"] = cadera + k * MUSLO * _dir(p["ll1"], f)
        j["pie_i"] = j["rodilla_i"] + k * PIERNA * _dir(p["ll1"] + p["ll2"], f)
        j["hombro"] = hombro
        # giro global alrededor de la cadera (volteretas, derribos)
        if abs(p.get("spin", 0.0)) > 1e-9:
            c, s = np.cos(p["spin"]), np.sin(p["spin"])
            for k, v in j.items():
                d = v - cadera
                j[k] = cadera + np.array([c * d[0] - s * d[1], s * d[0] + c * d[1], 0])
        return j

    def actualizar(self):
        j = self.articulaciones()
        pares = [("cadera", "cuello"), ("hombro", "codo_d"), ("codo_d", "mano_d"),
                 ("hombro", "codo_i"), ("codo_i", "mano_i"), ("cadera", "rodilla_d"),
                 ("rodilla_d", "pie_d"), ("cadera", "rodilla_i"), ("rodilla_i", "pie_i")]
        for seg, halo, (a, b) in zip(self.segs, self.halo, pares):
            pa, pb = j[a], j[b]
            if np.linalg.norm(pb - pa) < 1e-6:
                pb = pa + 1e-3 * RIGHT
            seg.put_start_and_end_on(pa, pb)
            halo.put_start_and_end_on(pa, pb)
        if self.simbolo is None:
            self.cabeza.move_to(j["cabeza"])
            self.halo_cab.move_to(j["cabeza"])
        else:
            ang = -self.mira * self.pose["lean"] + self.pose.get("spin", 0.0)
            arriba = np.array([self.mira * np.sin(self.pose["lean"]), np.cos(self.pose["lean"]), 0])
            if abs(self.pose.get("spin", 0.0)) > 1e-9:
                c, s_ = np.cos(self.pose["spin"]), np.sin(self.pose["spin"])
                arriba = np.array([c * arriba[0] - s_ * arriba[1], s_ * arriba[0] + c * arriba[1], 0])
            centro = j["cuello"] + (self.glifo_base.height / 2 + 0.06 * self.k) * arriba
            self.cabeza.become(self.glifo_base.copy().rotate(ang).move_to(centro))
            self.halo_cab.become(self.halo_base.copy().rotate(ang).move_to(centro))
            return self
        self.ojo.move_to(j["cabeza"] + np.array([0.13 * self.mira, 0.05, 0]))
        return self

    def punto(self, nombre):
        return self.articulaciones()[nombre]

    def girar(self):
        """Cambia instantáneamente hacia dónde mira."""
        self.mira *= -1
        return self.actualizar()


class Postura(Animation):
    """Interpola la postura del monigote hacia los valores dados."""

    def __init__(self, fig, rate_func=smooth, run_time=0.5, **objetivo):
        self.objetivo = objetivo
        super().__init__(fig, rate_func=rate_func, run_time=run_time)

    def begin(self):
        self.inicio = dict(self.mobject.pose)
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        p = dict(self.inicio)
        for k, v in self.objetivo.items():
            p[k] = self.inicio.get(k, 0.0) + (v - self.inicio.get(k, 0.0)) * a
        self.mobject.pose = p
        self.mobject.actualizar()


def P(fig, base=None, rate_func=smooth, run_time=0.5, **extra):
    """Atajo: postura base (diccionario) más ajustes."""
    obj = dict(base or {})
    obj.update(extra)
    return Postura(fig, rate_func=rate_func, run_time=run_time, **obj)


# --- Efectos -------------------------------------------------------------------------------
def destello(punto, color=BLANCO, radio=1.4, n_rayos=10, run_time=0.45):
    """Impacto: anillo expansivo, rayos radiales y núcleo brillante."""
    anillo = Circle(radius=0.08, stroke_color=color, stroke_width=7).move_to(punto)
    nucleo = Circle(radius=0.13, stroke_width=0, fill_color=BLANCO, fill_opacity=0.85).move_to(punto)
    rayos = VGroup()
    for k in range(n_rayos):
        th = TAU * k / n_rayos + 0.2
        d = np.array([np.cos(th), np.sin(th), 0])
        rayos.add(Line(punto + 0.25 * d, punto + 0.55 * d, stroke_width=5, color=color))
    anims = [
        anillo.animate(rate_func=rush_from).scale(radio / 0.08).set_stroke(opacity=0, width=2),
        nucleo.animate(rate_func=rush_from, run_time=run_time * 0.6).scale(2.2).set_fill(opacity=0),
    ]
    for r in rayos:
        d = r.get_end() - r.get_start()
        anims.append(r.animate(rate_func=rush_from).shift(d * 2.8).set_stroke(opacity=0))
    return AnimationGroup(*anims, run_time=run_time), VGroup(anillo, nucleo, rayos)


def particulas(punto, color, n=14, alcance=1.4, run_time=0.6, semilla=0, arriba=True):
    rng = np.random.default_rng(semilla)
    grupo, anims = VGroup(), []
    for _ in range(n):
        th = rng.uniform(0.15, np.pi - 0.15) if arriba else rng.uniform(0, TAU)
        r = rng.uniform(0.4, 1.0) * alcance
        d = Dot(punto, radius=rng.uniform(0.025, 0.06), color=color)
        grupo.add(d)
        anims.append(d.animate(rate_func=rush_from).shift(r * np.array([np.cos(th), np.sin(th), 0]))
                     .set_opacity(0))
    return AnimationGroup(*anims, run_time=run_time), grupo


def delta_flecha(base, altura=1.6, color=CIAN):
    """La delta de Dirac como impulso: flecha vertical con halo."""
    f = Arrow(base, base + UP * altura, buff=0, stroke_width=9, color=color,
              max_tip_length_to_length_ratio=0.22, max_stroke_width_to_length_ratio=12)
    halo = Line(base, base + UP * altura * 0.85, stroke_width=26, color=color, stroke_opacity=0.18)
    return VGroup(halo, f)


def y_apoyado(fig, suelo, **postura):
    """Altura de cadera para que el pie más bajo de la postura toque el suelo."""
    guardada = dict(fig.pose)
    fig.pose.update(postura)
    fig.pose["spin"] = postura.get("spin", 0.0)
    j = fig.articulaciones()
    y_min = min(j["pie_d"][1], j["pie_i"][1])
    y = fig.pose["y"] + (suelo - y_min)
    fig.pose = guardada
    fig.actualizar()
    return y


def PA(fig, base, suelo, rate_func=smooth, run_time=0.5, **extra):
    """Postura apoyada en el suelo (calcula la altura de la cadera)."""
    obj = dict(base)
    obj.update(extra)
    obj["y"] = y_apoyado(fig, suelo, **obj)
    return Postura(fig, rate_func=rate_func, run_time=run_time, **obj)


def caminar(fig, x_final, suelo, pasos=2, run_time=0.6):
    """Paso alternado sencillo hasta x_final."""
    x0 = fig.pose["x"]
    anims = []
    for k in range(pasos):
        xk = x0 + (x_final - x0) * (k + 1) / pasos
        s = 1 if k % 2 == 0 else -1
        anims.append(PA(fig, REPOSO, suelo, run_time=run_time / pasos, rate_func=linear, x=xk,
                        rl1=0.45 * s, rl2=-0.25 if s > 0 else 0.0,
                        ll1=-0.45 * s, ll2=-0.25 if s < 0 else 0.0,
                        ra1=-0.35 * s, la1=0.35 * s, ra2=-0.2 * s, la2=0.2 * s))
    anims.append(PA(fig, REPOSO, suelo, run_time=0.12, x=x_final))
    return Succession(*anims)


def punto_en_postura(fig, base, suelo, nombre, **extra):
    """Posición de una articulación si el monigote adoptara esa postura apoyada."""
    guardada = dict(fig.pose)
    obj = dict(base); obj.update(extra)
    obj["y"] = y_apoyado(fig, suelo, **obj)
    fig.pose.update(obj)
    pto = fig.articulaciones()[nombre]
    fig.pose = guardada
    fig.actualizar()
    return pto
