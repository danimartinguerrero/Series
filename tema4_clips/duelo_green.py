"""Duelo en L: δ contra G (a distancia).

Clip vertical (~30 s): dos monigotes pequeños, con cabezas δ y G, se baten a
distancia con armas matemáticas. Cada ataque deja como consecuencia el
objeto del Tema 4 que representa:

  1. Ráfaga de deltas -> G las para con la espada ∫ y, al clavarla, nace la
     función de Green causal (onda que sólo avanza hacia delante).
  2. Serie Σ de e^{λx} -> escudo ∏ (factorización de p(D)) que la parte en
     las exponenciales e^{λ_k x}.
  3. Plano complejo: raíces -γ ± iΩ -> rayo amortiguado e^{-γx} cos Ωx.
  4. Choque de rayos ∫G b dx̃ contra W k' = b: son el mismo cálculo.
"""
from monigote import *
from utiles import ajustar

SUELO = -1.0
XG, XD = -3.05, 2.85
K = 0.56                      # escala de los monigotes
XMAX = 3.6
Z_FX, Z_ARMAS = 3, 6


# --- piezas visuales --------------------------------------------------------------------
def glow(mob, color, ancho=20, opacidad=0.28):
    h = mob.copy().set_fill(opacity=0).set_stroke(color, width=ancho, opacity=opacidad)
    return VGroup(h, mob)


def glifo(tex, color, alto):
    g = MathTex(tex, tex_template=PLANTILLA, color=color)
    g.height = alto
    g.set_stroke(color, width=1.4)
    return glow(g, color)


def rayo(a, b, color, ancho=1.0):
    if np.linalg.norm(b - a) < 1e-3:
        b = a + 1e-3 * RIGHT
    capas = VGroup(
        Line(a, b, stroke_width=40 * ancho, color=color, stroke_opacity=0.12),
        Line(a, b, stroke_width=18 * ancho, color=color, stroke_opacity=0.45),
        Line(a, b, stroke_width=6 * ancho, color=BLANCO, stroke_opacity=0.95),
    )
    for l in capas:
        l.set_cap_style(CapStyleType.ROUND)
    capas.set_z_index(Z_FX + 1)
    return capas


def orbe(c, color, r=0.25):
    o = VGroup(*[Circle(radius=r * f, stroke_width=0, fill_color=col, fill_opacity=op).move_to(c)
                 for f, col, op in ((2.6, color, 0.10), (1.7, color, 0.28), (1.0, BLANCO, 0.95))])
    o.set_z_index(Z_FX + 2)
    return o


def g_resp(t, gam=0.22, om=3.0):
    t = np.asarray(t, dtype=float)
    return np.where(t > 0, np.exp(-gam * t) * np.sin(om * t), 0.0)


def curva(xs, ys, color, ancho=6):
    pts = [np.array([x, y, 0.0]) for x, y in zip(xs, ys)]
    l = VMobject(stroke_color=color, stroke_width=ancho).set_points_smoothly(pts)
    g = VGroup(l.copy().set_stroke(width=ancho * 3.2, opacity=0.18), l)
    g.set_z_index(Z_FX + 1)
    return g


def disparo(mob, ruta, retraso, duracion, total, rate=rush_into, desvanecer=False):
    """Proyectil invisible hasta su turno; luego recorre la ruta (función t -> punto)."""
    fam = mob.get_family()
    op = [(sm.get_fill_opacity(), sm.get_stroke_opacity()) for sm in fam]

    def visible(m, v):
        for sm, (fo, so) in zip(m.get_family(), op):
            sm.set_fill(opacity=fo * v)
            sm.set_stroke(opacity=so * v)

    visible(mob, 0)

    def f(m, a):
        t = (a * total - retraso) / duracion
        if t < 0:
            visible(m, 0)
            return
        t = min(t, 1.0)
        m.move_to(ruta(rate(t)))
        visible(m, 0 if (desvanecer and t >= 1.0) else 1)

    return UpdateFromAlphaFunc(mob, f, run_time=total, rate_func=linear)


def fx(par):
    anim, grupo = par
    grupo.set_z_index(Z_FX + 3)
    return anim, grupo


class DueloGreen(MovingCameraScene):
    def sacudir(self, fuerza=0.12, veces=5):
        marco = self.camera.frame
        rng = np.random.default_rng(int(fuerza * 1000) + veces)
        anims = [marco.animate(run_time=0.035, rate_func=linear).move_to(
            fuerza * np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0])) for _ in range(veces)]
        anims.append(marco.animate(run_time=0.05).move_to(ORIGIN))
        return Succession(*anims)

    def rotulo(self, titulo, formula, color, size=48):
        f = ajustar(M(formula, size=size, color=BLANCO), 6.9)
        return caja(f, color, titulo=titulo, buff=0.28).move_to(UP * 4.15 + LEFT * 0.35)

    def cambiar_rotulo(self, nuevo, t_out=0.14, t_in=0.24):
        anims = []
        if getattr(self, "rot_actual", None) is not None:
            anims.append(FadeOut(self.rot_actual, shift=UP * 0.15, run_time=t_out))
        anims.append(FadeIn(nuevo, shift=DOWN * 0.15, scale=0.96, run_time=t_in))
        self.rot_actual = nuevo
        return Succession(*anims)

    def registro(self):
        marco = RoundedRectangle(corner_radius=0.12, width=7.9, height=3.35, stroke_color=GRISMEDIO,
                                 stroke_width=2, fill_color=CAJA, fill_opacity=0.9)
        marco.move_to(np.array([-0.35, -3.25, 0]))
        et = T(r"\sffamily\bfseries Registro del duelo", size=24, color=FONDO)
        pest = RoundedRectangle(corner_radius=0.07, width=et.width + 0.3, height=et.height + 0.18,
                                stroke_width=0, fill_color=GRIS, fill_opacity=1)
        pest.move_to(marco.get_corner(UL) + RIGHT * (pest.width / 2 + 0.25))
        et.move_to(pest)
        self.reg = VGroup(marco, pest, et)
        self.n_reg = 0
        return self.reg

    def anotar(self, tex, color):
        y = -2.1 - 0.72 * self.n_reg
        punto = Dot(radius=0.07, color=color).move_to(np.array([-3.95, y, 0]))
        linea = ajustar(T(tex, size=31, color=TEXTO), 7.0)
        linea.next_to(punto, RIGHT, buff=0.22)
        self.n_reg += 1
        e = VGroup(punto, linea)
        self.reg.add(e)
        return FadeIn(e, shift=RIGHT * 0.25, run_time=0.4)

    def limpiar(self, *grupos):
        for g in grupos:
            for sm in g.get_family():
                self.remove(sm)

    # ------------------------------------------------------------------------------------
    def construct(self):
        cab = cabecera(1, 1, r"Duelo en $\mathcal L$: \ $\delta$ contra $G$")
        cab.remove(cab[1])
        self.add(pie())
        # cielo estrellado tenue y suelo
        rng = np.random.default_rng(7)
        estrellas = VGroup(*[Dot(np.array([rng.uniform(-4.3, 4.3), rng.uniform(-0.8, 3.3), 0]),
                                 radius=rng.uniform(0.008, 0.022), color=BLANCO)
                             .set_opacity(rng.uniform(0.15, 0.45)) for _ in range(70)])
        suelo = Line(LEFT * 4.35 + UP * SUELO, RIGHT * 4.35 + UP * SUELO, stroke_width=3, color=GRISMEDIO)
        marcas = VGroup(*[Line(np.array([x, SUELO - 0.06, 0]), np.array([x, SUELO + 0.06, 0]),
                               stroke_width=2, color=GRISMEDIO) for x in range(-4, 5)])
        eje = M(r"\mathbb R", size=28, color=GRISMEDIO).next_to(suelo.get_start(), UP, buff=0.1)
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), Write(cab[1]), GrowFromEdge(cab[2], LEFT),
                  GrowFromCenter(suelo), FadeIn(estrellas, lag_ratio=0.02), run_time=0.9)
        vs = M(r"\delta\ \ \text{vs}\ \ G", size=120, color=BLANCO).move_to(UP * 1.6 + LEFT * 0.35)
        vs[0][0].set_color(CIAN)
        vs[0][-1].set_color(AMBAR)
        self.play(FadeIn(marcas, lag_ratio=0.1), FadeIn(eje), Write(vs), run_time=0.6)
        self.wait(0.25)
        self.play(vs.animate.scale(1.3).set_opacity(0), run_time=0.3, rate_func=rush_into)
        self.remove(vs)

        # --- luchadores -----------------------------------------------------------------
        G = Monigote(AMBAR, XG, SUELO, mira=1, simbolo="G", escala=K, grosor=7, tam_cabeza=3.0, **GUARDIA)
        D = Monigote(CIAN, XD, SUELO, mira=-1, simbolo=r"\delta", escala=K, grosor=7, tam_cabeza=3.2,
                     **GUARDIA)
        for f in (G, D):
            f.pose["y"] = y_apoyado(f, SUELO, **GUARDIA)
            f.actualizar()
        aparic = [fx(destello(f.punto("cadera"), f.color_base, radio=1.3, run_time=0.4)) for f in (G, D)]
        self.play(FadeIn(G, scale=0.5), FadeIn(D, scale=0.5), *[a[0] for a in aparic], run_time=0.45)
        self.limpiar(*[a[1] for a in aparic])
        self.play(FadeIn(self.registro(), shift=UP * 0.2), run_time=0.35)

        # espada integral de G, sujeta a su mano
        alto_esp = ValueTracker(1.3)
        esp_base = glifo(r"\int", AMBAR, 1.0)

        def construir_espada():
            j = G.articulaciones()
            d = j["mano_d"] - j["codo_d"]
            d = d / (np.linalg.norm(d) + 1e-9)
            h = alto_esp.get_value()
            e = esp_base.copy().set_height(h)
            e.rotate(np.arctan2(d[1], d[0]) - PI / 2)
            e.move_to(j["mano_d"] + d * h * 0.42)
            e.set_z_index(Z_ARMAS)
            return e

        def punta_espada():
            j = G.articulaciones()
            d = j["mano_d"] - j["codo_d"]
            d = d / (np.linalg.norm(d) + 1e-9)
            return j["mano_d"] + d * alto_esp.get_value() * 0.9

        # --- 1. Ráfaga de deltas y espada integral --------------------------------------
        r1 = self.rotulo(r"Ráfaga de impulsos", r"\delta(x-\tilde x)", CIAN, size=62)
        self.play(PA(D, LANZAR_CARGA, SUELO, run_time=0.3, x=XD), self.cambiar_rotulo(r1))
        espada = always_redraw(construir_espada)
        destello_esp, gr_e = fx(destello(punto_en_postura(G, PUNETAZO, SUELO, "mano_d", x=XG),
                                         AMBAR, radio=0.9, run_time=0.35))
        self.play(PA(G, PUNETAZO, SUELO, run_time=0.3, x=XG), FadeIn(espada, scale=0.4), destello_esp)
        self.limpiar(gr_e)
        # cinco deltas horizontales
        objetivo = punta_espada() + RIGHT * 0.1
        origen = punto_en_postura(D, LANZAR_FIN, SUELO, "mano_d", x=XD)
        proy, anims_p = [], []
        for k in range(5):
            dlt = delta_flecha(ORIGIN, altura=0.95, color=CIAN).rotate(PI / 2)
            dlt.set_z_index(Z_ARMAS)
            proy.append(dlt)
            o_k = origen + UP * 0.08 * (k % 2)
            dest = objetivo + UP * (0.18 * ((k % 3) - 1))
            anims_p.append(disparo(dlt, lambda t, o=o_k, d=dest: o + (d - o) * t, 0.16 * k, 0.36, 1.2,
                                   rate=linear, desvanecer=True))
        self.play(PA(D, LANZAR_FIN, SUELO, run_time=0.25, x=XD), *anims_p,
                  Succession(*[Succession(Wait(0.16 if k else 0.3),
                                          P(G, PUNETAZO, ra1=1.6 + 0.35 * (-1) ** k, run_time=0.14))
                               for k in range(5)]),
                  run_time=1.2)
        sp = [fx(destello(objetivo + UP * 0.15 * (k - 1), CIAN, radio=0.55, n_rayos=7, run_time=0.25))
              for k in range(3)]
        self.play(*[s[0] for s in sp], self.sacudir(0.05, 2), run_time=0.25)
        self.limpiar(*[s[1] for s in sp], *proy)

        # G clava la espada: nace la función de Green (respuesta causal)
        r2 = self.rotulo(r"Respuesta al impulso", r"\mathcal L_x\,G(x,\tilde x)=\delta(x-\tilde x)", AMBAR,
                         size=52)
        xt = XG + 0.95
        self.play(PA(G, BRAZOS_ARRIBA, SUELO, run_time=0.25, x=XG), self.cambiar_rotulo(r2))
        espada.clear_updaters()
        clavada = esp_base.copy().set_height(1.3).rotate(PI).move_to(np.array([xt, SUELO + 0.48, 0]))
        clavada.set_z_index(Z_ARMAS)
        self.play(PA(G, GOLPE_SUELO, SUELO, run_time=0.2, x=XG, rate_func=rush_into),
                  Transform(espada, clavada, run_time=0.2, rate_func=rush_into))
        golpe, gr_g = fx(destello(np.array([xt, SUELO, 0]), AMBAR, radio=1.7))
        etq = M(r"\tilde x", size=32, color=AMBAR).move_to(np.array([xt, SUELO - 0.38, 0]))
        self.play(golpe, self.sacudir(0.14, 5), FadeIn(etq), run_time=0.4)
        self.limpiar(gr_g)
        frente = ValueTracker(xt + 0.03)
        A_ONDA = 1.0

        def onda_g():
            xs = np.linspace(xt, frente.get_value(), 160)
            return curva(xs, SUELO + A_ONDA * g_resp(xs - xt), AMBAR, ancho=6)

        onda = always_redraw(onda_g)
        self.add(onda)
        T_O = 1.6
        t_salto = (XD - 0.9 - xt) / (XMAX - xt) * T_O
        self.play(frente.animate(rate_func=linear).set_value(XMAX),
                  Succession(Wait(t_salto),
                             P(D, AGACHADO, y=SUELO + 1.9, spin=-TAU, run_time=0.5, rate_func=smooth),
                             PA(D, GUARDIA, SUELO, x=XD, spin=-TAU, run_time=0.22, rate_func=rush_into)),
                  run_time=T_O)
        D.pose["spin"] = 0.0
        D.actualizar()
        onda.clear_updaters()
        aterriza, gr_a = fx(particulas(np.array([XD, SUELO, 0]), CIAN, n=10, alcance=0.8, semilla=3))
        self.play(onda.animate.set_opacity(0), aterriza, FadeOut(etq),
                  self.anotar(r"$\delta(x-\tilde x)\ \longrightarrow\ G(x,\tilde x)$: respuesta causal", AMBAR),
                  run_time=0.45)
        self.limpiar(onda, gr_a)
        # G recupera la espada
        self.play(PA(G, GUARDIA, SUELO, run_time=0.3, x=XG), FadeOut(espada, run_time=0.15))
        self.remove(espada)
        espada = always_redraw(construir_espada)
        self.play(FadeIn(espada, scale=0.5), run_time=0.2)

        # --- 2. Serie Σ contra escudo ∏ -----------------------------------------------
        r3 = self.rotulo(r"Serie exponencial", r"e^{\lambda x}=\sum_{n\ge0}\frac{(\lambda x)^n}{n!}", AMBAR,
                         size=48)
        sigma = glifo(r"\Sigma", AMBAR, 1.3).move_to(np.array([XG + 1.7, SUELO + 3.65, 0]))
        sigma.set_z_index(Z_ARMAS)
        self.play(PA(G, BRAZOS_ARRIBA, SUELO, run_time=0.3, x=XG), self.cambiar_rotulo(r3),
                  GrowFromCenter(sigma), run_time=0.4)
        self.play(Rotate(sigma, TAU, run_time=0.45, rate_func=smooth))
        self.wait(0.5)
        # escudo ∏ de δ
        r4 = self.rotulo(r"Factorización", r"\mathcal L=a_n\prod_{k}(D-\lambda_k)^{m_k}", CIAN, size=52)
        xs_esc = XD - 0.75
        pi_esc = glifo(r"\prod", CIAN, 1.6).move_to(np.array([xs_esc, SUELO + 0.95, 0]))
        aura = Circle(radius=1.1, stroke_color=CIAN, stroke_width=3, fill_color=CIAN, fill_opacity=0.08)
        aura.move_to(pi_esc)
        pi_esc.set_z_index(Z_ARMAS)
        aura.set_z_index(Z_ARMAS - 1)
        terminos = [r"1", r"+\lambda x", r"+\tfrac{(\lambda x)^2}{2!}", r"+\tfrac{(\lambda x)^3}{3!}", r"+\cdots"]
        impactos = [aura.get_left() + UP * 0.3 * (k - 2) + RIGHT * 0.15 for k in range(5)]
        proy, anims_p = [], []
        for k, t in enumerate(terminos):
            p = glifo(t, AMBAR, 0.5 if k < 2 else 0.78).move_to(sigma.get_center())
            p.set_z_index(Z_ARMAS)
            proy.append(p)
            ruta = ArcBetweenPoints(sigma.get_center(), impactos[k], angle=-PI / 6)
            anims_p.append(disparo(p, lambda u, r=ruta: r.point_from_proportion(u), 0.17 * k, 0.45, 1.15))
        self.play(PA(D, ESCUDO, SUELO, run_time=0.3, x=XD), FadeIn(aura, scale=0.6), GrowFromCenter(pi_esc),
                  PA(G, LANZAR_FIN, SUELO, run_time=0.3, x=XG), self.cambiar_rotulo(r4),
                  *anims_p, FadeOut(sigma, run_time=0.4), run_time=1.15)
        sp = [fx(destello(impactos[k], AMBAR, radio=0.5, n_rayos=6, run_time=0.25)) for k in range(5)]
        self.play(*[s[0] for s in sp], *[FadeOut(p, scale=0.4) for p in proy],
                  aura.animate.set_stroke(width=6), self.sacudir(0.06, 2), run_time=0.3)
        self.limpiar(*[s[1] for s in sp])
        # el escudo parte la serie en las exponenciales e^{λ_k x}
        trozos = VGroup(*[glifo(t, c, 0.5) for t, c in
                          ((r"e^{\lambda_1x}", CIAN), (r"e^{\lambda_2x}", VERDE), (r"x\,e^{\lambda_2x}", MAGENTA))])
        destinos = [np.array([0.3, 2.7, 0]), np.array([-0.9, 1.9, 0]), np.array([0.6, 1.15, 0])]
        for t in trozos:
            t.move_to(aura.get_left())
            t.set_z_index(Z_ARMAS)
        self.play(*[t.animate(rate_func=rush_from).move_to(d) for t, d in zip(trozos, destinos)],
                  aura.animate.set_stroke(width=3),
                  self.anotar(r"$\sum\frac{(\lambda x)^n}{n!}\ \longrightarrow\ e^{\lambda_k x}$: "
                              r"factorización $\prod(D-\lambda_k)^{m_k}$", CIAN), run_time=0.55)
        self.wait(0.85)
        self.play(FadeOut(trozos, shift=UP * 0.2), FadeOut(pi_esc), FadeOut(aura),
                  PA(D, GUARDIA, SUELO, run_time=0.35, x=XD), PA(G, GUARDIA, SUELO, run_time=0.35, x=XG),
                  run_time=0.4)

        # --- 3. Plano complejo: rayo amortiguado --------------------------------------
        r5 = self.rotulo(r"Raíces complejas \ $\lambda=-\gamma\pm i\Omega$",
                         r"y=e^{-\gamma x}\bigl(A\cos\Omega x+B\sen\Omega x\bigr)", VIOLETA, size=48)
        L = 1.6
        c_pl = np.array([1.25, 1.85, 0])
        lado = 2.3
        r1c, r2c = complex(-0.65, 1.15), complex(-0.65, -1.15)
        img = imagen_fase(lambda z: 1 / ((z - r1c) * (z - r2c)), (-L, L), (-L, L), res=500, brillo=0.88)
        img.set(width=lado, height=lado).move_to(c_pl).set_opacity(0.85)
        plano = NumberPlane(x_range=[-L, L, 0.5], y_range=[-L, L, 0.5], x_length=lado, y_length=lado,
                            background_line_style=dict(stroke_color=BLANCO, stroke_width=0.8,
                                                       stroke_opacity=0.18),
                            axis_config=dict(stroke_color=BLANCO, stroke_width=1.6, stroke_opacity=0.6))
        plano.move_to(c_pl)
        marco = Square(side_length=lado, stroke_color=VIOLETA, stroke_width=3).move_to(c_pl)
        circ = Circle(radius=lado / (2 * L) * abs(r1c), stroke_color=BLANCO, stroke_width=2,
                      stroke_opacity=0.5).move_to(plano.c2p(0, 0))
        raices = VGroup(*[orbe(plano.c2p(r.real, r.imag), VIOLETA, r=0.07) for r in (r1c, r2c)])
        etq_c = M(r"\mathbb C", size=34, color=BLANCO).next_to(marco, UP, buff=0.08).align_to(marco, RIGHT)
        grupo_pl = Group(img, plano, circ, marco, raices, etq_c)
        for m in grupo_pl:
            m.set_z_index(Z_FX)
        self.play(PA(D, BRAZOS_ARRIBA, SUELO, run_time=0.35, x=XD), self.cambiar_rotulo(r5),
                  FadeIn(img, scale=0.3), Create(plano), Create(marco), run_time=0.55)
        self.play(Create(circ), LaggedStart(*[GrowFromCenter(o) for o in raices], lag_ratio=0.3),
                  FadeIn(etq_c), run_time=0.5)
        fasor = Arrow(plano.c2p(0, 0), plano.c2p(r1c.real, r1c.imag), buff=0, stroke_width=4, color=BLANCO)
        fasor.set_z_index(Z_FX + 2)
        self.play(GrowArrow(fasor), Indicate(raices, color=BLANCO, scale_factor=1.6), run_time=0.45)
        self.remove(fasor)
        # rayo: oscilación amortiguada que viaja de δ hacia G
        mano = punto_en_postura(D, PUNETAZO, SUELO, "mano_d", x=XD)
        yh = mano[1]
        x_ini, x_fin = mano[0] - 0.1, punta_espada()[0] + 0.25
        gam, om, A = 0.42, 5.2, 0.62
        perfil = lambda s: yh + A * np.exp(-gam * s) * np.cos(om * s)
        fr = ValueTracker(0.02)

        def rayo_complejo():
            s = np.linspace(0, fr.get_value(), 220)
            return curva(x_ini - s, perfil(s), MAGENTA, ancho=6)

        rayo_c = always_redraw(rayo_complejo)
        env = VGroup(*[DashedVMobject(VMobject(stroke_color=VIOLETA, stroke_width=2).set_points_smoothly(
            [np.array([x_ini - s, yh + sg * A * np.exp(-gam * s), 0]) for s in np.linspace(0, x_ini - x_fin, 40)]),
            num_dashes=28) for sg in (1, -1)])
        env.set_opacity(0.6)
        self.add(rayo_c)
        self.play(PA(D, PUNETAZO, SUELO, run_time=0.25, x=XD),
                  fr.animate(rate_func=linear).set_value(x_ini - x_fin), Create(env), run_time=1.15)
        rayo_c.clear_updaters()
        par, gr_p = fx(destello(np.array([x_fin, perfil(x_ini - x_fin), 0]), MAGENTA, radio=0.6,
                                run_time=0.3))
        amort = M(r"\text{amortiguado: }\ e^{-\gamma x}\to0", size=30, color=VIOLETA)
        amort.move_to(np.array([(x_ini + x_fin) / 2, yh - 0.95, 0]))
        self.play(par, P(G, ESCUDO, run_time=0.2), FadeIn(amort),
                  self.anotar(r"$\lambda=-\gamma\pm i\Omega\ \longrightarrow\ e^{-\gamma x}\cos\Omega x$: "
                              r"oscilación amortiguada", VIOLETA), run_time=0.4)
        self.limpiar(gr_p)
        self.wait(0.9)
        self.play(FadeOut(rayo_c), FadeOut(env), FadeOut(amort), FadeOut(grupo_pl),
                  PA(G, GUARDIA, SUELO, run_time=0.3, x=XG), PA(D, GUARDIA, SUELO, run_time=0.3, x=XD),
                  run_time=0.45)

        # --- 4. Choque de rayos ------------------------------------------------------------
        r6 = self.rotulo(r"Choque final", r"\int G\,b\,d\tilde x\quad\text{vs}\quad W\bm k'=\bm b", BLANCO,
                         size=50)
        self.play(PA(G, BRAZOS_ARRIBA, SUELO, run_time=0.3, x=XG), alto_esp.animate.set_value(1.55),
                  PA(D, LANZAR_CARGA, SUELO, run_time=0.3, x=XD), self.cambiar_rotulo(r6), run_time=0.4)
        self.play(PA(G, PUNETAZO, SUELO, run_time=0.2, x=XG), PA(D, PUNETAZO, SUELO, run_time=0.2, x=XD))
        a_pt = punta_espada
        b_pt = lambda: D.punto("mano_d")
        y_haz = (a_pt()[1] + b_pt()[1]) / 2
        choque = ValueTracker(-0.05)
        cpt = lambda: np.array([choque.get_value(), y_haz, 0])
        haz_g = always_redraw(lambda: rayo(a_pt(), cpt(), AMBAR, 1.15))
        haz_d = always_redraw(lambda: rayo(b_pt(), cpt(), CIAN, 1.15))
        bola = always_redraw(lambda: orbe(cpt(), BLANCO, r=0.27 + 0.06 * np.sin(14 * choque.get_value())))
        lab_g = M(r"\int G(x,\tilde x)\,b(\tilde x)\,d\tilde x", size=38, color=AMBAR)
        lab_d = M(r"W\,\bm k'=\bm b", size=42, color=CIAN)
        lab_g.move_to(np.array([-1.45, y_haz + 0.95, 0]))
        lab_d.move_to(np.array([1.45, y_haz - 0.85, 0]))
        self.add(haz_g, haz_d, bola)
        self.play(FadeIn(lab_g), FadeIn(lab_d), self.sacudir(0.05, 4), run_time=0.4)
        for v in (0.6, -0.5, 0.45, -0.6, 0.3, -0.15, 0.0):
            self.play(choque.animate(rate_func=smooth).set_value(v), self.sacudir(0.04, 3), run_time=0.32)
        # explosión
        for m in (haz_g, haz_d, bola):
            m.clear_updaters()
        boom, gr_b = destello(cpt(), BLANCO, radio=4.0, n_rayos=16, run_time=0.65)
        gr_b.set_z_index(Z_ARMAS + 2)
        flash = Rectangle(width=12, height=20, stroke_width=0, fill_color=BLANCO, fill_opacity=0)
        flash.set_z_index(Z_ARMAS + 3)
        self.add(flash)
        self.play(boom, self.sacudir(0.24, 7), flash.animate(rate_func=there_and_back).set_fill(opacity=0.65),
                  FadeOut(haz_g), FadeOut(haz_d), FadeOut(bola), FadeOut(lab_g), FadeOut(lab_d), run_time=0.65)
        self.limpiar(gr_b, flash)

        # --- 5. Revelación ---------------------------------------------------------------------
        igual = VGroup(
            T(r"variación de constantes $\;\equiv\;$ método de Green", size=40, color=BLANCO),
            M(r"G(x,\tilde x)=\Theta(x-\tilde x)\,\hat{\bm y}^{\mathsf T}(x)\,W^{-1}(\tilde x)\,"
              r"\frac{\bm e_n}{a_n(\tilde x)}", size=44, color=BLANCO)).arrange(DOWN, buff=0.3)
        rfin = caja(ajustar(igual, 6.9), BLANCO, titulo=r"Son el mismo cálculo", buff=0.3)
        rfin.move_to(UP * 3.95 + LEFT * 0.35)
        halo_c = VGroup(*[Circle(radius=r, stroke_color=c, stroke_width=3, stroke_opacity=o)
                          .move_to(np.array([0, y_haz, 0])) for r, c, o in ((0.5, AMBAR, 0.8), (0.8, CIAN, 0.5))])
        self.play(self.cambiar_rotulo(rfin, t_in=0.5), FadeOut(espada),
                  self.anotar(r"$\int G\,b\,d\tilde x\ \equiv\ W\bm k'=\bm b$: el mismo cálculo", BLANCO),
                  PA(G, REPOSO, SUELO, run_time=0.5, x=XG), PA(D, REPOSO, SUELO, run_time=0.5, x=XD),
                  Succession(FadeIn(halo_c, scale=0.3, run_time=0.25),
                             halo_c.animate(run_time=0.55).scale(2.2).set_opacity(0)),
                  run_time=0.8)
        self.limpiar(halo_c)
        self.wait(2.2)
        fin = VGroup(T(r"\bfseries Funciones de Green", size=60, color=BLANCO),
                     T(r"la respuesta a un impulso, sumada sobre todos los impulsos", size=30, color=GRIS)
                     ).arrange(DOWN, buff=0.25).move_to(DOWN * 2.75 + LEFT * 0.35)
        firma = VGroup(T(r"\textsc{Apuntes formalizados}", size=24, color=CIAN),
                       T(AUTOR, size=28, color=TEXTO)).arrange(DOWN, buff=0.1).next_to(fin, DOWN, buff=0.45)
        self.play(FadeOut(self.reg, shift=DOWN * 0.2), run_time=0.4)
        self.play(FadeIn(fin, shift=UP * 0.2), PA(G, BRAZOS_ARRIBA, SUELO, run_time=0.5, x=XG),
                  PA(D, BRAZOS_ARRIBA, SUELO, run_time=0.5, x=XD), run_time=0.6)
        self.play(FadeIn(firma), PA(G, REPOSO, SUELO, run_time=0.5, x=XG),
                  PA(D, REPOSO, SUELO, run_time=0.5, x=XD), run_time=0.5)
        self.wait(2.4)
