"""Duelo en L: δ contra G.

Clip vertical (~30 s) de combate entre dos monigotes originales que luchan
con las herramientas del Tema 4: la delta de Dirac (impulso unitario), la
función de Green causal (respuesta al impulso), la superposición
y_p = ∫ G b dx̃ y la variación de las constantes (W k' = b). El combate
termina descubriendo que los dos métodos son el mismo cálculo.
"""
from monigote import *
from utiles import ajustar

SUELO = -1.4
XMAX = 4.3
GAMMA, OMEGA = 0.18, 2.3
Z_EFECTOS = 3          # efectos por detrás de los personajes (z = 5)


def g_resp(t):
    """Perfil de la respuesta causal (función de Green del oscilador amortiguado)."""
    t = np.asarray(t, dtype=float)
    return np.where(t > 0, np.exp(-GAMMA * t) * np.sin(OMEGA * t), 0.0)


def curva_onda(x0, frente, perfil, color, ancho=6, paso=0.02, x_tope=XMAX):
    """Onda sobre el suelo desde x0 hasta el frente (con halo)."""
    x1 = min(frente, x_tope)
    if x1 <= x0 + 0.02:
        x1 = x0 + 0.02
    xs = np.arange(x0, x1 + 1e-9, paso)
    pts = [np.array([x, SUELO + float(perfil(x)), 0.0]) for x in xs]
    linea = VMobject(stroke_color=color, stroke_width=ancho).set_points_smoothly(pts)
    halo = linea.copy().set_stroke(width=ancho * 3.2, opacity=0.16)
    g = VGroup(halo, linea)
    g.set_z_index(4)
    return g


def fx(anim_grupo):
    """Coloca un efecto (destello/partículas) por detrás de los personajes."""
    anim, grupo = anim_grupo
    grupo.set_z_index(Z_EFECTOS)
    return anim, grupo


class DueloGreen(MovingCameraScene):
    # --- utilidades de escena ------------------------------------------------------------
    def sacudir(self, fuerza=0.12, veces=5):
        marco = self.camera.frame
        rng = np.random.default_rng(int(fuerza * 1000) + veces)
        anims = []
        for _ in range(veces):
            d = fuerza * np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0])
            anims.append(marco.animate(run_time=0.035, rate_func=linear).move_to(d))
        anims.append(marco.animate(run_time=0.05).move_to(ORIGIN))
        return Succession(*anims)

    def rotulo(self, titulo, formula, color, size=44):
        """Cartel del «golpe» en la franja superior (pestaña + fórmula)."""
        f = ajustar(M(formula, size=size, color=BLANCO), 6.9)
        c = caja(f, color, titulo=titulo, buff=0.28)
        c.move_to(UP * 4.2 + LEFT * 0.35)
        return c

    def cambiar_rotulo(self, nuevo, t_out=0.14, t_in=0.24):
        """Sustituye el cartel: primero sale el anterior y después entra el nuevo."""
        anims = []
        if getattr(self, "rot_actual", None) is not None:
            anims.append(FadeOut(self.rot_actual, shift=UP * 0.15, run_time=t_out))
        anims.append(FadeIn(nuevo, shift=DOWN * 0.15, scale=0.96, run_time=t_in))
        self.rot_actual = nuevo
        return Succession(*anims)

    def limpiar(self, *grupos):
        for g in grupos:
            self.remove(g)
            for sm in g.get_family():
                self.remove(sm)

    # --- guion ---------------------------------------------------------------------------
    def construct(self):
        # Cabecera y escenario
        cab = cabecera(1, 1, r"Duelo en $\mathcal L$: \ $\delta$ contra $G$")
        cab.remove(cab[1])
        self.add(pie())
        suelo = Line(LEFT * 4.35 + UP * SUELO, RIGHT * 4.35 + UP * SUELO, stroke_width=3,
                     color=GRISMEDIO)
        marcas = VGroup(*[Line(np.array([x, SUELO - 0.07, 0]), np.array([x, SUELO + 0.07, 0]),
                               stroke_width=2, color=GRISMEDIO) for x in range(-4, 5)])
        eje_r = M(r"\mathbb R", size=30, color=GRISMEDIO).next_to(suelo.get_start(), UP, buff=0.12)
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), Write(cab[1]), GrowFromEdge(cab[2], LEFT),
                  GrowFromCenter(suelo), run_time=0.9)
        vs = M(r"\delta\ \ \text{vs}\ \ G", size=120, color=BLANCO).move_to(UP * 1.2 + LEFT * 0.35)
        vs[0][0].set_color(CIAN)
        vs[0][-1].set_color(AMBAR)
        self.play(FadeIn(marcas, lag_ratio=0.1), FadeIn(eje_r), Write(vs), run_time=0.7)
        self.wait(0.35)
        self.play(vs.animate.scale(1.3).set_opacity(0), run_time=0.35, rate_func=rush_into)
        self.remove(vs)

        # --- 1. Entrada de los luchadores ----------------------------------------------
        G = Monigote(AMBAR, -2.7, SUELO, mira=1, simbolo="G")
        D = Monigote(CIAN, 2.2, SUELO, mira=-1, simbolo=r"\delta")
        Y_AIRE = SUELO + ALTURA_CADERA + 2.5
        entradas = []
        for fig in (G, D):
            fig.pose.update(BRAZOS_ARRIBA)
            fig.pose["y"] = Y_AIRE
            fig.actualizar()
            a, gr = fx(destello(fig.punto("cuello"), fig.color_base, radio=1.6, n_rayos=10,
                                run_time=0.4))
            entradas.append((a, gr))
        self.play(FadeIn(G, scale=0.6), FadeIn(D, scale=0.6), *[e[0] for e in entradas], run_time=0.4)
        self.limpiar(*[e[1] for e in entradas])
        self.play(P(G, BRAZOS_ARRIBA, y=SUELO + ALTURA_CADERA, rate_func=rush_into, run_time=0.38),
                  Succession(Wait(0.1), P(D, BRAZOS_ARRIBA, y=SUELO + ALTURA_CADERA,
                                          rate_func=rush_into, run_time=0.38)))
        polvo = [fx(particulas(np.array([f.pose["x"], SUELO, 0]), GRIS, n=14, alcance=1.1, semilla=k))
                 for k, f in enumerate((G, D))]
        self.play(PA(G, AGACHADO, SUELO, run_time=0.13), PA(D, AGACHADO, SUELO, run_time=0.13),
                  *[p[0] for p in polvo], self.sacudir(0.12, 3))
        placa_g = M(r"G(x,\tilde x)", size=42, color=AMBAR).move_to(np.array([-2.7, SUELO - 0.6, 0]))
        placa_d = M(r"\delta(x-\tilde x)", size=42, color=CIAN).move_to(np.array([2.2, SUELO - 0.6, 0]))
        self.play(PA(G, GUARDIA, SUELO, run_time=0.35), PA(D, GUARDIA, SUELO, run_time=0.35),
                  FadeIn(placa_g, shift=UP * 0.1), FadeIn(placa_d, shift=UP * 0.1))
        # balanceo en guardia
        for dy in (-0.09, 0.0):
            self.play(P(G, y=G.pose["y"] + dy, run_time=0.2), P(D, y=D.pose["y"] + dy, run_time=0.2))

        # --- 2. δ lanza un impulso unitario --------------------------------------------
        r1 = self.rotulo(r"Impulso unitario", r"\delta(x-\tilde x)", CIAN, size=60)
        self.play(PA(D, LANZAR_CARGA, SUELO, run_time=0.35), self.cambiar_rotulo(r1))
        mano = D.punto("mano_d")
        lanza = delta_flecha(mano + DOWN * 0.7, altura=1.6, color=CIAN)
        lanza.set_z_index(6)
        self.play(GrowFromPoint(lanza, mano), run_time=0.3)
        self.wait(0.35)
        destino = punto_en_postura(G, ESCUDO, SUELO, "mano_d") + RIGHT * 0.05
        arco = ArcBetweenPoints(lanza.get_center(), destino, angle=-PI / 5)
        estela = TracedPath(lambda: lanza.get_center(), dissipating_time=0.3,
                            stroke_color=CIAN, stroke_width=8, stroke_opacity=0.85)
        estela.set_z_index(4)
        self.add(estela)
        lanza_0 = lanza.copy()

        def vuelo(m, a):
            m.become(lanza_0.copy().rotate(PI / 2 * a).move_to(arco.point_from_proportion(a)))

        self.play(PA(D, LANZAR_FIN, SUELO, run_time=0.22, rate_func=rush_from),
                  UpdateFromAlphaFunc(lanza, vuelo, rate_func=rush_into, run_time=0.55))

        # --- 3. G lo atrapa y lo clava: respuesta causal ---------------------------------
        r2 = self.rotulo(r"Respuesta causal", r"\mathcal L_x\,G(x,\tilde x)=\delta(x-\tilde x)", AMBAR,
                         size=50)
        chispa, gr_ch = fx(destello(destino, CIAN, radio=1.1, run_time=0.35))
        self.play(PA(G, ESCUDO, SUELO, run_time=0.14), chispa, self.cambiar_rotulo(r2))
        self.limpiar(gr_ch, estela)
        polvo_g = fx(particulas(np.array([-2.8, SUELO, 0]), GRIS, n=10, alcance=0.8, semilla=4))
        self.play(PA(G, ESCUDO, SUELO, x=-3.05, run_time=0.3, rate_func=rush_from),
                  lanza.animate(rate_func=rush_from, run_time=0.3).shift(LEFT * 0.35), polvo_g[0])
        self.wait(0.45)
        xt = -2.0
        arriba = punto_en_postura(G, BRAZOS_ARRIBA, SUELO, "mano_d", x=-2.85)
        self.play(PA(G, BRAZOS_ARRIBA, SUELO, run_time=0.28, x=-2.85),
                  lanza.animate(run_time=0.28).rotate(-PI / 2).move_to(arriba + UP * 0.3))
        self.play(PA(G, GOLPE_SUELO, SUELO, x=-2.85, run_time=0.2, rate_func=rush_into),
                  lanza.animate(run_time=0.2, rate_func=rush_into)
                  .rotate(PI).move_to(np.array([xt, SUELO + 0.8, 0])))
        pico = delta_flecha(np.array([xt, SUELO, 0]), altura=1.7, color=CIAN)
        golpe, gr_g = fx(destello(np.array([xt, SUELO, 0]), AMBAR, radio=1.8))
        etq_xt = M(r"\tilde x", size=36, color=CIAN).move_to(np.array([xt, SUELO - 0.5, 0]))
        self.remove(lanza)
        self.add(pico)
        self.play(golpe, self.sacudir(0.16, 5), FadeIn(etq_xt), FadeOut(placa_g), run_time=0.4)
        self.limpiar(gr_g)

        # la respuesta viaja sólo hacia delante (causalidad) y derriba a δ
        frente = ValueTracker(xt)
        onda = always_redraw(lambda: curva_onda(xt, frente.get_value(),
                                                lambda x: 1.15 * g_resp(x - xt), AMBAR))
        r3 = self.rotulo(r"Función de Green",
                         r"G=\Theta(x-\tilde x)\,e^{-\gamma(x-\tilde x)}\,\frac{\sin\Omega(x-\tilde x)}{\Omega}",
                         AMBAR, size=44)
        self.add(onda)
        T_ONDA = 2.0
        t_imp = (D.pose["x"] - 0.4 - xt) / (XMAX - xt) * T_ONDA
        self.play(frente.animate(rate_func=linear).set_value(XMAX), self.cambiar_rotulo(r3),
                  PA(G, GUARDIA, SUELO, run_time=0.45, x=-2.85), FadeOut(pico, run_time=0.5),
                  Succession(Wait(t_imp),
                             P(D, AGACHADO, x=2.85, y=SUELO + 2.2, spin=-1.3, run_time=0.38,
                               rate_func=rush_from),
                             PA(D, AGACHADO, SUELO, x=2.95, spin=0.0, run_time=0.3,
                                rate_func=rush_into)),
                  FadeOut(placa_d, run_time=0.3), run_time=T_ONDA)
        golpe_d, gr_d = fx(destello(np.array([2.95, SUELO, 0]), CIAN, radio=1.1, run_time=0.3))
        self.play(golpe_d, self.sacudir(0.1, 3), run_time=0.35)
        onda.clear_updaters()
        self.limpiar(gr_d)
        self.play(onda.animate.set_opacity(0), PA(D, GUARDIA, SUELO, x=2.2, run_time=0.45),
                  run_time=0.5)
        self.limpiar(onda)
        self.wait(0.8)

        # --- 4. δ responde con una lluvia de impulsos ------------------------------------
        r4 = self.rotulo(r"Lluvia de impulsos",
                         r"b(x)=\int b(\tilde x)\,\delta(x-\tilde x)\,d\tilde x", CIAN, size=48)
        DX = 0.3
        xs_k = np.array([-1.4 + DX * k for k in range(7)])
        b = lambda s: np.sin(np.pi * (s + 1.55) / 2.1) ** 2
        base_b = 2.0
        fuente = VMobject(stroke_color=CIAN, stroke_width=5).set_points_smoothly(
            [np.array([s, base_b + 0.75 * b(s), 0]) for s in np.linspace(-1.55, 0.55, 60)])
        fuente_h = fuente.copy().set_stroke(width=16, opacity=0.18)
        etq_b = M(r"b(\tilde x)", size=36, color=CIAN).next_to(fuente, RIGHT, buff=0.2).shift(DOWN * 0.25)
        self.play(PA(D, BRAZOS_ARRIBA, SUELO, run_time=0.3), self.cambiar_rotulo(r4),
                  Create(fuente), FadeIn(fuente_h), FadeIn(etq_b), FadeOut(etq_xt), run_time=0.6)
        self.wait(0.7)
        flechas = VGroup()
        for s in xs_k:
            fl = delta_flecha(np.array([s, SUELO, 0]), altura=0.4 + 1.2 * b(s), color=CIAN)
            fl.rotate(PI).move_to(np.array([s, base_b + 0.75 * b(s), 0]), aligned_edge=UP)
            flechas.add(fl)
        self.add(flechas)
        caidas = [Succession(Wait(0.07 * k),
                             fl.animate(rate_func=rush_into, run_time=0.32)
                             .move_to(np.array([xs_k[k], SUELO, 0]), aligned_edge=DOWN))
                  for k, fl in enumerate(flechas)]
        self.play(*caidas, P(D, LANZAR_FIN, run_time=0.45), run_time=0.82)
        self.limpiar(flechas)
        picos = VGroup(*[delta_flecha(np.array([s, SUELO, 0]), altura=0.4 + 1.2 * b(s), color=CIAN)
                         for s in xs_k])
        chispas = [fx(destello(np.array([s, SUELO, 0]), CIAN, radio=0.55, n_rayos=6, run_time=0.3))
                   for s in xs_k]
        self.add(picos)
        self.play(*[c[0] for c in chispas], self.sacudir(0.07, 3), run_time=0.3)
        self.limpiar(*[c[1] for c in chispas])
        # cada impulso produce su propia respuesta (superposición discreta)
        tau = ValueTracker(0.0)
        malla = np.linspace(-1.4, XMAX, 500)
        S = 1.45 / max(np.sum([b(s) * DX * g_resp(x - s) for s in xs_k]) for x in malla)
        ondas_k = VGroup(*[
            always_redraw(lambda s=s, k=k: curva_onda(
                s, s + tau.get_value(), lambda x, s=s: S * b(s) * DX * g_resp(x - s),
                PROGRESION[k], ancho=3.5))
            for k, s in enumerate(xs_k)])
        self.add(ondas_k)
        self.play(tau.animate(rate_func=linear).set_value(1.2), FadeOut(picos),
                  PA(D, GUARDIA, SUELO, run_time=0.4), run_time=0.9)

        # --- 5. G integra: superposición y_p = ∫ G b dx~ --------------------------------
        r5 = self.rotulo(r"Superposición",
                         r"y_p(x)=\int G(x,\tilde x)\,b(\tilde x)\,d\tilde x", AMBAR, size=52)
        mano_g = punto_en_postura(G, PUNETAZO, SUELO, "mano_d")
        integral = M(r"\int", size=170, color=AMBAR).move_to(mano_g + RIGHT * 0.75 + UP * 0.25)
        integral_h = integral.copy().set_stroke(AMBAR, width=14, opacity=0.25)
        self.play(PA(G, PUNETAZO, SUELO, run_time=0.25), self.cambiar_rotulo(r5),
                  FadeIn(integral, scale=0.5), FadeIn(integral_h, scale=0.5), run_time=0.45)
        for o in ondas_k:
            o.clear_updaters()
        frente_y = -1.4 + 1.2
        yp = lambda x: S * np.sum([b(s) * DX * g_resp(x - s) for s in xs_k])
        grande = curva_onda(-1.4, frente_y, yp, AMBAR, ancho=7)
        self.play(integral.animate.move_to(np.array([-0.6, SUELO + 1.0, 0])).scale(0.6).set_opacity(0),
                  integral_h.animate.move_to(np.array([-0.6, SUELO + 1.0, 0])).scale(0.6).set_opacity(0),
                  ReplacementTransform(ondas_k, grande), FadeOut(fuente), FadeOut(fuente_h),
                  FadeOut(etq_b), run_time=0.65)
        self.limpiar(integral, integral_h)
        self.wait(0.9)

        # --- 6. δ se protege con la variación de las constantes ------------------------
        r6 = self.rotulo(r"Variación de constantes", r"W(x)\,\bm k'(x)=\bm b(x)", VIOLETA, size=56)
        escudo = VGroup(RoundedRectangle(corner_radius=0.12, width=1.05, height=2.6, stroke_color=VIOLETA,
                                         stroke_width=5, fill_color=CAJA, fill_opacity=0.97),
                        M(r"W^{-1}", size=64, color=BLANCO))
        escudo_h = RoundedRectangle(corner_radius=0.14, width=1.3, height=2.85, stroke_width=0,
                                    fill_color=VIOLETA, fill_opacity=0.2)
        escudo.move_to(np.array([1.25, SUELO + 1.4, 0]))
        escudo_h.move_to(escudo)
        escudo.set_z_index(6)
        escudo_h.set_z_index(6)
        borde_esc = escudo[0].get_left()[0]
        frente2 = ValueTracker(frente_y)
        self.remove(grande)
        ola = always_redraw(lambda: curva_onda(-1.4, frente2.get_value(), yp, AMBAR, ancho=7,
                                               x_tope=borde_esc))
        self.add(ola)
        self.play(PA(D, ESCUDO, SUELO, run_time=0.3), self.cambiar_rotulo(r6),
                  GrowFromCenter(escudo), FadeIn(escudo_h),
                  frente2.animate(rate_func=linear).set_value(borde_esc), run_time=1.1)
        # choque
        choque, gr_c = destello(np.array([borde_esc, SUELO + 1.2, 0]), BLANCO, radio=3.4,
                                n_rayos=14, run_time=0.6)
        gr_c.set_z_index(7)
        flash = Rectangle(width=12, height=20, stroke_width=0, fill_color=BLANCO, fill_opacity=0.0)
        flash.set_z_index(8)
        self.add(flash)
        self.play(choque, self.sacudir(0.22, 7),
                  flash.animate(rate_func=there_and_back, run_time=0.5).set_fill(opacity=0.6),
                  run_time=0.6)
        ola.clear_updaters()
        self.limpiar(gr_c, flash)

        # --- 7. Revelación: son el mismo método -------------------------------------------
        igual = VGroup(
            T(r"variación de constantes $\;\equiv\;$ método de Green", size=40, color=BLANCO),
            M(r"G(x,\tilde x)=\Theta(x-\tilde x)\,\hat{\bm y}^{\mathsf T}(x)\,W^{-1}(\tilde x)\,"
              r"\frac{\bm e_n}{a_n(\tilde x)}", size=44, color=BLANCO),
        ).arrange(DOWN, buff=0.3)
        ajustar(igual, 6.9)
        rfin = caja(igual, BLANCO, titulo=r"Son el mismo cálculo", buff=0.3).move_to(UP * 4.0 + LEFT * 0.35)
        self.play(FadeOut(ola), FadeOut(escudo), FadeOut(escudo_h),
                  PA(G, REPOSO, SUELO, run_time=0.5, lean=-0.12),
                  PA(D, REPOSO, SUELO, run_time=0.5, lean=-0.12),
                  self.cambiar_rotulo(rfin, t_in=0.5), run_time=0.65)
        self.wait(2.1)
        self.play(caminar(G, -1.5, SUELO, pasos=2, run_time=0.6),
                  caminar(D, 1.5, SUELO, pasos=2, run_time=0.6))
        self.play(PA(G, PUNETAZO, SUELO, run_time=0.25), PA(D, PUNETAZO, SUELO, run_time=0.25))
        puno = (G.punto("mano_d") + D.punto("mano_d")) / 2
        toque, gr_t = destello(puno, AMBAR, radio=1.0, n_rayos=8, run_time=0.45)
        toque2, gr_t2 = destello(puno, CIAN, radio=0.7, n_rayos=8, run_time=0.45)
        gr_t.set_z_index(6)
        gr_t2.set_z_index(6)
        self.play(toque, toque2, self.sacudir(0.06, 3))
        self.limpiar(gr_t, gr_t2)
        self.wait(1.0)

        # --- 8. Cierre ---------------------------------------------------------------------
        fin = VGroup(
            T(r"\bfseries Funciones de Green", size=60, color=BLANCO),
            T(r"la respuesta a un impulso, sumada sobre todos los impulsos", size=30, color=GRIS),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.15 + LEFT * 0.35)
        firma = VGroup(T(r"\textsc{Apuntes formalizados}", size=24, color=CIAN),
                       T(AUTOR, size=28, color=TEXTO)).arrange(DOWN, buff=0.1)
        firma.next_to(fin, DOWN, buff=0.45)
        self.play(FadeIn(fin, shift=UP * 0.2), PA(G, REPOSO, SUELO, run_time=0.4),
                  PA(D, REPOSO, SUELO, run_time=0.4), run_time=0.7)
        self.play(FadeIn(firma), run_time=0.5)
        self.wait(2.6)
