"""Clip 4 — La ecuación de Airy: la recurrencia salta de tres en tres."""
from utiles import *


def airy_base(x, N=120):
    """Sistema fundamental y1, y2 de y'' = x y sumando sus series."""
    a1 = np.zeros(N); a2 = np.zeros(N)
    a1[0], a2[1] = 1.0, 1.0
    for n in range(1, N - 2):
        a1[n + 2] = a1[n - 1] / ((n + 2) * (n + 1))
        a2[n + 2] = a2[n - 1] / ((n + 2) * (n + 1))
    pot = x ** np.arange(N)
    return float(a1 @ pot), float(a2 @ pot)


C1, C2 = 0.355028053887817, 0.258819403792807


def Ai(x):
    y1, y2 = airy_base(x)
    return C1 * y1 - C2 * y2


def Bi(x):
    y1, y2 = airy_base(x)
    return np.sqrt(3) * (C1 * y1 + C2 * y2)


class Clip4Airy(Scene):
    def construct(self):
        cab = cabecera(4, 5, r"Airy: funciones que no existían")
        pie_ = pie()
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), FadeIn(cab[1]), run_time=0.6)
        self.play(Write(cab[2]), GrowFromEdge(cab[3], LEFT), run_time=1.1)
        self.add(pie_)
        X0 = LEFT * 0.35

        # --- 1. Ecuación y recurrencia ----------------------------------------------------
        edo = M(r"y''-x\,y=0", size=66).move_to(UP * 4.4 + X0)
        q = M(r"q=-x\ \Rightarrow\ q_1=-1", size=38, color=GRIS).next_to(edo, DOWN, buff=0.3)
        self.play(Write(edo), run_time=0.9)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        rec = M(r"(n+2)(n+1)\,a_{n+2}=a_{n-1},\qquad a_2=0", size=44)
        caja_r = caja(ajustar(rec, 7.0), AMBAR, titulo="Recurrencia").move_to(UP * 1.95 + X0)
        self.play(FadeIn(caja_r, shift=UP * 0.2), run_time=0.9)

        # --- 2. Tres cadenas independientes -------------------------------------------
        colores = [CIAN, MAGENTA, GRISMEDIO]
        filas = VGroup()
        for r in range(3):
            fila = VGroup(*[nodo_coef(r"a_{%d}" % (r + 3 * c), color=colores[r], radio=0.42, size=34)
                            for c in range(4)])
            fila.arrange(RIGHT, buff=0.55)
            filas.add(fila)
        filas.arrange(DOWN, buff=0.38).move_to(DOWN * 1.15 + X0 + LEFT * 0.45)
        for nd in filas[2]:
            nd[1].set_color(GRISMEDIO)
        sufijos = VGroup(
            M(r"\propto a_0", size=36, color=CIAN).next_to(filas[0], RIGHT, buff=0.35),
            M(r"\propto a_1", size=36, color=MAGENTA).next_to(filas[1], RIGHT, buff=0.35),
            M(r"=0", size=36, color=GRIS).next_to(filas[2], RIGHT, buff=0.35),
        )
        self.play(LaggedStart(*[FadeIn(f[0], scale=0.8) for f in filas], lag_ratio=0.2), run_time=0.8)
        flechas = VGroup()
        for c in range(1, 4):
            anims = []
            for r in range(3):
                fl = Arrow(filas[r][c - 1].get_right(), filas[r][c].get_left(), buff=0.06,
                           stroke_width=3, color=colores[r], max_tip_length_to_length_ratio=0.35)
                flechas.add(fl)
                anims += [GrowArrow(fl), FadeIn(filas[r][c], shift=RIGHT * 0.15)]
            self.play(*anims, run_time=0.75)
        self.play(FadeIn(sufijos), run_time=0.6)
        self.wait(1.4)

        # --- 3. Las dos series -----------------------------------------------------------------
        self.play(FadeOut(filas), FadeOut(flechas), FadeOut(sufijos), FadeOut(q), run_time=0.6)
        series = VGroup(
            M(r"y_1=1+\frac{x^{3}}{6}+\frac{x^{6}}{180}+\cdots", size=46, color=CIAN),
            M(r"y_2=x+\frac{x^{4}}{12}+\frac{x^{7}}{504}+\cdots", size=46, color=MAGENTA),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.0 + X0)
        self.play(caja_r.animate.scale(0.85).move_to(UP * 3.0 + X0), run_time=0.5)
        self.play(LaggedStart(*[Write(s) for s in series], lag_ratio=0.4), run_time=1.8)
        rinf = nota(r"$R=\infty$: convergen en todo $\mathbb R$", size=32).next_to(series, DOWN, buff=0.3)
        self.play(FadeIn(rinf), run_time=0.5)
        self.wait(1.2)

        # --- 4. Ai y Bi --------------------------------------------------------------------
        self.play(FadeOut(rinf), series.animate.scale(0.78).move_to(UP * 1.15 + X0), run_time=0.6)
        ax = ejes([-9, 2.5, 3], [-0.6, 1.5, 0.5], x_length=7.4, y_length=4.0)
        ax.move_to(DOWN * 2.05 + X0)
        sombra = Rectangle(width=ax.c2p(2.5, 0)[0] - ax.c2p(0, 0)[0], height=ax.y_length,
                           stroke_width=0, fill_color=GRISOSCURO, fill_opacity=0.55)
        sombra.move_to(ax.c2p(1.25, 0.45))
        xt = VGroup(*[M(str(v), size=26, color=GRIS).next_to(ax.c2p(v, -0.6), DOWN, buff=0.15)
                      for v in (-9, -6, -3, 0)])
        self.play(Create(ax), FadeIn(sombra), FadeIn(xt), run_time=0.7)
        g_ai = curva_recortada(ax, Ai, -9, 2.5, -0.6, 1.5, AMBAR, ancho=5, n=700)
        g_bi = curva_recortada(ax, Bi, -9, 2.5, -0.6, 1.5, VERDE, ancho=5, n=700)
        self.play(Create(g_ai), run_time=2.2, rate_func=linear)
        self.play(Create(g_bi), run_time=2.2, rate_func=linear)
        ley = VGroup(M(r"\Ai", size=38, color=AMBAR), M(r"\Bi", size=38, color=VERDE))\
            .arrange(RIGHT, buff=0.5).move_to(ax.c2p(-7.4, 1.3))
        osc = etiqueta_fondo(T("oscila", size=30, color=GRIS)).move_to(ax.c2p(-4.5, 1.3))
        exp_ = etiqueta_fondo(T("crece / decae", size=26, color=GRIS)).move_to(ax.c2p(1.25, -0.42))
        self.play(FadeIn(ley), FadeIn(osc), FadeIn(exp_), run_time=0.6)
        comb = M(r"\Ai=c_1y_1-c_2y_2,\qquad \Bi=\sqrt3\,(c_1y_1+c_2y_2)", size=34, color=GRIS)
        ajustar(comb, 7.2).next_to(ax, DOWN, buff=0.75)
        self.play(FadeIn(comb), run_time=0.6)
        self.wait(2.0)
        msg = T(r"La serie \emph{define} funciones nuevas", size=44, color=BLANCO)
        msg.move_to(series)
        self.play(FadeOut(series, shift=UP * 0.2), FadeIn(msg, shift=UP * 0.2), run_time=0.8)
        self.wait(3.6)
