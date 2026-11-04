"""Clip 5 — Legendre: cuando la serie se corta aparecen los polinomios."""
from utiles import *


class Clip5Legendre(Scene):
    def construct(self):
        cab = cabecera(5, 5, r"Legendre: cuando la serie se corta")
        pie_ = pie()
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), FadeIn(cab[1]), run_time=0.6)
        self.play(Write(cab[2]), GrowFromEdge(cab[3], LEFT), run_time=1.1)
        self.add(pie_)
        X0 = LEFT * 0.35

        # --- 1. Ecuación y radio garantizado ----------------------------------------------
        edo = ajustar(M(r"(1-x^{2})\,y''-2x\,y'+\ell(\ell+1)\,y=0", size=52), 7.4)
        edo.move_to(UP * 4.4 + X0)
        r = M(r"P=1-x^{2}=0\iff x=\pm1\ \Rightarrow\ R\ge1", size=38, color=GRIS)
        r.next_to(edo, DOWN, buff=0.3)
        self.play(Write(edo), run_time=1.3)
        self.play(FadeIn(r, shift=DOWN * 0.1), run_time=0.6)
        self.wait(0.8)

        # --- 2. Recurrencia y truncamiento ----------------------------------------------
        rec = M(r"a_{n+2}=\frac{(n-\ell)\,(n+\ell+1)}{(n+2)(n+1)}\,a_n", size=50)
        rec[0][5:10].set_color(AMBAR)   # glifos de (n - l)
        caja_r = caja(rec, AMBAR, titulo="Recurrencia").move_to(UP * 1.75 + X0)
        self.play(FadeIn(caja_r, shift=UP * 0.2), run_time=0.9)
        foco = SurroundingRectangle(rec[0][5:10], color=AMBAR, buff=0.06, corner_radius=0.05)
        corte = M(r"n=\ell\ \Longrightarrow\ a_{\ell+2}=a_{\ell+4}=\cdots=0", size=42, color=AMBAR)
        corte.next_to(caja_r, DOWN, buff=0.4)
        self.play(Create(foco), run_time=0.5)
        self.play(Write(corte), run_time=1.0)
        poli = nota(r"si $\ell\in\mathbb N$, la serie de su paridad es un \textbf{polinomio}",
                    size=34, color=TEXTO).next_to(corte, DOWN, buff=0.3)
        self.play(FadeIn(poli), run_time=0.6)
        self.wait(1.4)

        # --- 3. Polinomios de Legendre ------------------------------------------------------
        self.play(FadeOut(r), FadeOut(foco), FadeOut(corte), FadeOut(poli),
                  caja_r.animate.scale(0.8).move_to(UP * 3.0 + X0), run_time=0.7)
        ax = ejes([-1, 1, 0.5], [-1, 1, 0.5], x_length=6.6, y_length=4.4)
        ax.move_to(DOWN * 1.55 + X0)
        xt = VGroup(*[M(t, size=28, color=GRIS).next_to(ax.c2p(v, -1), DOWN, buff=0.15)
                      for t, v in (("-1", -1), ("0", 0), ("1", 1))])
        self.play(Create(ax), FadeIn(xt), run_time=0.6)
        P = [lambda x: 1 + 0 * x, lambda x: x, lambda x: 0.5 * (3 * x ** 2 - 1),
             lambda x: 0.5 * (5 * x ** 3 - 3 * x), lambda x: (35 * x ** 4 - 30 * x ** 2 + 3) / 8]
        texs = [r"P_0=1", r"P_1=x", r"P_2=\tfrac12(3x^{2}-1)", r"P_3=\tfrac12(5x^{3}-3x)",
                r"P_4=\tfrac18(35x^{4}-30x^{2}+3)"]
        cols = [GRIS, CIAN, MAGENTA, AMBAR, VERDE]
        curvas, lab = [], None
        for k in range(5):
            c = ax.plot(P[k], x_range=[-1, 1], color=cols[k], stroke_width=5)
            nl = M(texs[k], size=44, color=cols[k]).move_to(UP * 1.4 + X0)
            anims = [Create(c)]
            anims += [Transform(lab, nl)] if lab is not None else [FadeIn(nl)]
            if curvas:
                anims += [curvas[-1].animate.set_stroke(opacity=0.45, width=3)]
            self.play(*anims, run_time=1.0)
            self.wait(0.35)
            curvas.append(c)
            if lab is None:
                lab = nl
        self.wait(0.6)

        # --- 4. La otra serie no se corta: diverge en x = ±1 -------------------------------
        self.play(*[FadeOut(c) for c in curvas], FadeOut(ax), FadeOut(xt), FadeOut(lab), run_time=0.6)
        caso = M(r"\ell=1:\quad y_1=1-\sum_{k\ge1}\frac{x^{2k}}{2k-1}=1-x\artanh x", size=40)
        ajustar(caso, 7.3).move_to(UP * 1.05 + X0)
        ax2 = ejes([-1, 1, 0.5], [-2.5, 1.2, 1], x_length=6.6, y_length=4.2)
        ax2.move_to(DOWN * 1.95 + X0)
        asint = VGroup(*[DashedLine(ax2.c2p(s, -2.5), ax2.c2p(s, 1.2), color=ROJO, stroke_width=3,
                                    dash_length=0.1) for s in (-1, 1)])
        self.play(Write(caso), Create(ax2), run_time=1.0)
        exacta = curva_recortada(ax2, lambda x: 1 - x * np.arctanh(x), -0.9995, 0.9995, -2.5, 1.2,
                                 BLANCO, ancho=5, n=1500)
        mm = [1, 2, 4, 8, 32]
        parcial = lambda M_: (lambda x: 1 - sum(x ** (2 * k) / (2 * k - 1) for k in range(1, M_ + 1)))
        g = curva_recortada(ax2, parcial(mm[0]), -1, 1, -2.5, 1.2, CIAN, ancho=4)
        self.play(Create(asint), Create(exacta), run_time=1.0)
        self.play(Create(g), run_time=0.4)
        for M_ in mm[1:]:
            self.play(Transform(g, curva_recortada(ax2, parcial(M_), -1, 1, -2.5, 1.2, CIAN, ancho=4)),
                      run_time=0.75)
        div = etiqueta_fondo(T(r"diverge en $x=\pm1$: \ $R=1$ exacto", size=32, color=ROJO))
        div.move_to(ax2.c2p(0, -2.05))
        self.play(FadeIn(div), run_time=0.5)
        self.wait(1.6)

        # --- 5. Cuantización -----------------------------------------------------------------
        msg = VGroup(
            M(r"\text{regular en }x=\pm1\ \Longrightarrow\ \ell\in\mathbb N", size=40, color=BLANCO),
            T(r"($x=\cos\theta$: polos $\theta=0,\pi$ en la ecuación de Laplace)", size=26, color=GRIS),
        ).arrange(DOWN, buff=0.16)
        caja_m = caja(ajustar(msg, 6.9), CIAN, titulo="Cuantización", buff=0.26).move_to(UP * 1.1 + X0)
        self.play(FadeOut(caso, shift=UP * 0.2), FadeIn(caja_m, shift=UP * 0.2), run_time=0.8)
        self.wait(3.4)
