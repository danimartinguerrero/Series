"""Clip 3 — y'' + y = 0: la serie reconstruye el coseno término a término."""
from math import factorial
from utiles import *


class Clip3Coseno(Scene):
    def construct(self):
        cab = cabecera(3, 5, r"Una serie que reconstruye el coseno")
        pie_ = pie()
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), FadeIn(cab[1]), run_time=0.6)
        self.play(Write(cab[2]), GrowFromEdge(cab[3], LEFT), run_time=1.1)
        self.add(pie_)
        X0 = LEFT * 0.35

        # --- 1. Ecuación y recurrencia ----------------------------------------------------
        edo = M(r"y''+y=0", size=66).move_to(UP * 4.4 + X0)
        pq = M(r"p\equiv0,\qquad q\equiv1\ \ (q_0=1)", size=38, color=GRIS).next_to(edo, DOWN, buff=0.3)
        self.play(Write(edo), run_time=0.9)
        self.play(FadeIn(pq, shift=DOWN * 0.1), run_time=0.5)
        rec = M(r"a_{n+2}=-\frac{a_n}{(n+2)(n+1)}", size=50)
        caja_r = caja(rec, AMBAR, titulo="Recurrencia").move_to(UP * 2.05 + X0)
        self.play(FadeIn(caja_r, shift=UP * 0.2), run_time=0.9)
        self.wait(0.4)

        # --- 2. Coeficientes: cadena par con a_0 = 1, a_1 = 0 ---------------------------
        datos = M(r"a_0=1,\quad a_1=0", size=40, color=AMBAR).move_to(UP * 0.5 + X0)
        self.play(FadeIn(datos), run_time=0.5)
        lineas = VGroup(
            M(r"a_2=-\frac{a_0}{2\cdot1}=-\frac{1}{2!}", size=46),
            M(r"a_4=-\frac{a_2}{4\cdot3}=+\frac{1}{4!}", size=46),
            M(r"a_6=-\frac{a_4}{6\cdot5}=-\frac{1}{6!}", size=46),
        ).arrange(DOWN, buff=0.32)
        for l in lineas[1:]:
            l.align_to(lineas[0], LEFT)
        lineas.move_to(DOWN * 1.6 + X0)
        for l in lineas:
            self.play(Write(l), run_time=0.85)
        general = M(r"a_{2m}=\frac{(-1)^m}{(2m)!},\qquad a_{2m+1}=0", size=44, color=CIAN)
        general.next_to(lineas, DOWN, buff=0.45)
        self.play(FadeIn(general, shift=UP * 0.15), run_time=0.7)
        self.wait(0.9)

        # --- 3. Sumas parciales que abrazan el coseno -----------------------------------
        self.play(FadeOut(lineas), FadeOut(general), FadeOut(datos),
                  FadeOut(pq), caja_r.animate.scale(0.85).move_to(UP * 3.0 + X0),
                  edo.animate.move_to(UP * 4.55 + X0), run_time=0.8)
        ax = ejes([-7, 7, np.pi], [-2, 2, 1], x_length=7.4, y_length=4.4)
        ax.move_to(DOWN * 0.95 + X0)
        ticks = VGroup(*[M(t, size=28, color=GRIS).next_to(ax.c2p(v, 0), DOWN, buff=0.2)
                         for t, v in ((r"-2\pi", -2 * np.pi), (r"-\pi", -np.pi), (r"\pi", np.pi),
                                      (r"2\pi", 2 * np.pi))])
        cos_g = DashedVMobject(ax.plot(np.cos, x_range=[-7, 7], color=BLANCO, stroke_width=3),
                               num_dashes=70)
        self.play(Create(ax), FadeIn(ticks), run_time=0.7)
        self.play(Create(cos_g), run_time=0.8)

        def S(mm):
            return lambda x: sum((-1) ** k * x ** (2 * k) / factorial(2 * k) for k in range(mm + 1))

        curva = curva_recortada(ax, S(0), -7, 7, -2, 2, CIAN, ancho=5)
        etq = M(r"S_{0}", size=44, color=CIAN).move_to(ax.c2p(-5.3, 1.5))
        self.play(Create(curva), FadeIn(etq), run_time=0.6)
        for mm in range(1, 11):
            nueva = curva_recortada(ax, S(mm), -7, 7, -2, 2, CIAN, ancho=5)
            netq = M(r"S_{%d}" % (2 * mm), size=44, color=CIAN).move_to(etq)
            self.play(Transform(curva, nueva), Transform(etq, netq), run_time=0.62)
        self.wait(1.0)

        # --- 4. Identidad y radio infinito ------------------------------------------------
        iden = M(r"\sum_{m\ge0}\frac{(-1)^m x^{2m}}{(2m)!}=\cos x", size=50)
        caja_i = caja(iden, CIAN, titulo="Resultado").move_to(DOWN * 4.05 + X0)
        self.play(FadeIn(caja_i, shift=UP * 0.2), run_time=0.9)
        radio = M(r"R=\infty\quad(P\equiv1\ \text{no tiene ceros})", size=36, color=AMBAR)
        radio.next_to(ax, UP, buff=0.2).align_to(ax, RIGHT)
        self.play(FadeIn(radio), run_time=0.5)
        sen = ax.plot(np.sin, x_range=[-7, 7], color=MAGENTA, stroke_width=4)
        sen_lab = etiqueta_fondo(M(r"(0,1)\mapsto y_2=\sen x", size=36, color=MAGENTA))
        sen_lab.move_to(ax.c2p(-3.6, -1.65))
        self.play(Create(sen), FadeIn(sen_lab), run_time=1.2)
        self.wait(1.4)
        gen = M(r"y=a_0\cos x+a_1\sen x", size=54, color=BLANCO)
        caja_g = caja(gen, CIAN, titulo="Solución general").move_to(caja_i)
        self.play(FadeOut(caja_i, shift=DOWN * 0.2), FadeIn(caja_g, shift=UP * 0.2), run_time=0.9)
        self.wait(2.6)
