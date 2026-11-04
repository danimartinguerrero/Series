"""Clip 2 — De la EDO a la recurrencia (método de la serie entera)."""
from utiles import *


class Clip2Recurrencia(Scene):
    def construct(self):
        cab = cabecera(2, 5, r"La EDO se convierte en una recurrencia")
        pie_ = pie()
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), FadeIn(cab[1]), run_time=0.6)
        self.play(Write(cab[2]), GrowFromEdge(cab[3], LEFT), run_time=1.1)
        self.add(pie_)
        X0 = LEFT * 0.35

        # --- 1. Punto ordinario y forma normal ------------------------------------------
        edo = M(r"P(x)\,y''+A(x)\,y'+B(x)\,y=0", size=54).move_to(UP * 4.35 + X0)
        ordin = M(r"x_0\ \text{ordinario}:\quad P(x_0)\neq 0", size=46, color=CIAN)
        ordin.move_to(UP * 3.05 + X0)
        normal = M(r"y''+p\,y'+q\,y=0", size=54).move_to(UP * 1.75 + X0)
        pq = M(r"p=\frac{A}{P}=\sum_{k}p_k z^{k},\qquad q=\frac{B}{P}=\sum_k q_k z^{k}",
               size=40, color=GRIS).move_to(UP * 0.45 + X0)
        zdef = M(r"z=x-x_0", size=38, color=GRIS).next_to(pq, DOWN, buff=0.35)
        self.play(Write(edo), run_time=1.0)
        self.play(FadeIn(ordin, shift=DOWN * 0.15), run_time=0.6)
        self.play(TransformFromCopy(edo, normal), run_time=0.9)
        self.play(FadeIn(pq, shift=UP * 0.15), FadeIn(zdef), run_time=0.8)
        self.wait(0.6)

        # --- 2. Ansatz y derivación término a término ----------------------------------
        self.play(FadeOut(edo, shift=UP * 0.3), FadeOut(ordin, shift=UP * 0.3),
                  FadeOut(pq), FadeOut(zdef),
                  normal.animate.move_to(UP * 4.35 + X0), run_time=0.9)
        filas = VGroup(
            M(r"y=\sum_{n\ge0}a_n\,z^{n}", size=50),
            M(r"y'=\sum_{n\ge1}n\,a_n\,z^{n-1}", size=50),
            M(r"y''=\sum_{n\ge2}n(n-1)\,a_n\,z^{n-2}", size=50),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.75 + X0)
        etq_ans = nota(r"\textsc{ansatz}", size=30, color=AMBAR).next_to(filas[0], UP, buff=0.4)\
            .align_to(filas, LEFT)
        self.play(FadeIn(etq_ans), Write(filas[0]), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in filas[1:]], lag_ratio=0.5),
                  run_time=1.2)

        # --- 3. Índice mudo: todo en potencias z^n ---------------------------------------
        nueva2 = M(r"y''=\sum_{n\ge0}(n+2)(n+1)\,a_{n+2}\,z^{n}", size=50).move_to(filas[2], LEFT)
        nueva1 = M(r"y'=\sum_{n\ge0}(n+1)\,a_{n+1}\,z^{n}", size=50).move_to(filas[1], LEFT)
        mudo = nota(r"índice mudo:\ $n\mapsto n+2$,\ \ $n\mapsto n+1$", size=34, color=CIAN)
        mudo.next_to(filas, DOWN, buff=0.55).align_to(filas, LEFT)
        self.play(FadeIn(mudo, shift=UP * 0.1), run_time=0.5)
        self.play(TransformMatchingTex(filas[2], nueva2), run_time=1.1)
        self.play(TransformMatchingTex(filas[1], nueva1), run_time=0.9)
        self.wait(0.4)

        # --- 4. Producto de Cauchy ----------------------------------------------------------
        bloque = VGroup(filas[0], nueva1, nueva2, etq_ans, mudo)
        self.play(FadeOut(bloque, shift=LEFT * 0.4), run_time=0.6)
        cauchy = M(r"\Bigl(\sum_k c_k z^{k}\Bigr)\Bigl(\sum_m b_m z^{m}\Bigr)"
                   r"=\sum_n\Bigl(\sum_{k=0}^{n}c_k\,b_{n-k}\Bigr)z^{n}", size=40)
        ajustar(cauchy, 7.3).move_to(UP * 2.75 + X0)
        tit_c = nota(r"\textsc{producto de Cauchy}", size=30, color=CIAN).next_to(cauchy, UP, buff=0.35)
        self.play(FadeIn(tit_c), Write(cauchy), run_time=1.0)
        red = VGroup()
        h = 0.78
        origen = LEFT * 2.3 + DOWN * 2.6
        puntos = {}
        for k in range(6):
            for mm in range(6):
                d = Dot(origen + RIGHT * k * h + UP * mm * h, radius=0.075, color=GRISMEDIO)
                puntos[(k, mm)] = d
                red.add(d)
        ek = M("k", size=36, color=GRIS).next_to(puntos[(5, 0)], RIGHT, buff=0.35)
        em = M("m", size=36, color=GRIS).next_to(puntos[(0, 5)], LEFT, buff=0.35)
        self.play(FadeIn(red, lag_ratio=0.02), FadeIn(ek), FadeIn(em), run_time=0.7)
        diag_lab = None
        for n in range(1, 6):
            diag = VGroup(*[puntos[(k, n - k)].copy().set_color(CIAN).scale(1.7) for k in range(n + 1)])
            lin = Line(puntos[(n, 0)].get_center(), puntos[(0, n)].get_center(), color=CIAN,
                       stroke_width=3)
            lab = M(r"z^{%d}" % n, size=40, color=CIAN).next_to(puntos[(n, 0)], DOWN, buff=0.35)
            anims = [FadeIn(diag), Create(lin), FadeIn(lab)]
            if diag_lab is not None:
                anims += [FadeOut(o) for o in diag_lab]
            self.play(*anims, run_time=0.38)
            diag_lab = (diag, lin, lab)
        self.wait(0.3)

        # --- 5. Identificar coeficientes: la recurrencia ---------------------------------
        self.play(FadeOut(red), FadeOut(ek), FadeOut(em), *[FadeOut(o) for o in diag_lab],
                  FadeOut(cauchy, shift=UP * 0.2), FadeOut(tit_c), run_time=0.6)
        rec = M(r"\begin{gathered}(n+2)(n+1)\,a_{n+2}\\[2pt]"
                r"=-\sum_{k=0}^{n}\Bigl[(n-k+1)\,p_k\,a_{n-k+1}+q_k\,a_{n-k}\Bigr]"
                r"\end{gathered}", size=42)
        ajustar(rec, 6.9)
        caja_r = caja(rec, AMBAR, titulo="Recurrencia")
        caja_r.move_to(UP * 2.2 + X0)
        coef0 = nota(r"coeficiente de $z^{n}$ $=0$ \ (unicidad del desarrollo)", size=32)
        coef0.next_to(caja_r, DOWN, buff=0.35)
        self.play(FadeIn(caja_r, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(coef0), run_time=0.5)

        # --- 6. Dependencias: a_0, a_1 libres ---------------------------------------------
        nodos = VGroup(*[nodo_coef(r"a_{%d}" % i, radio=0.42, size=36) for i in range(7)])
        nodos.arrange(RIGHT, buff=0.24).move_to(DOWN * 1.85 + X0)
        for i in (0, 1):
            nodos[i][0].set_stroke(AMBAR, width=4)
        libres = nota(r"libres: $a_0=y(x_0)$, \ $a_1=y'(x_0)$", size=32, color=AMBAR)
        libres.next_to(nodos, DOWN, buff=0.4).align_to(nodos, LEFT)
        self.play(LaggedStart(*[GrowFromCenter(nd) for nd in nodos], lag_ratio=0.08), run_time=0.9)
        self.play(FadeIn(libres), run_time=0.5)
        for j in range(2, 7):
            arcos = VGroup(*[CurvedArrow(nodos[i][0].get_top(), nodos[j][0].get_top(),
                                         angle=-TAU / 7, color=CIAN, stroke_width=2.5,
                                         tip_length=0.15)
                             for i in range(j)])
            self.play(Create(arcos), run_time=0.35)
            self.play(nodos[j][0].animate.set_stroke(CIAN, width=4), FadeOut(arcos), run_time=0.25)
        sol = M(r"y=a_0\,y_1+a_1\,y_2", size=54, color=BLANCO)
        caja_s = caja(sol, CIAN, titulo="Sistema fundamental")
        caja_s.move_to(DOWN * 3.85 + X0)
        self.play(FadeOut(libres), FadeIn(caja_s, shift=UP * 0.2), run_time=0.9)
        self.wait(2.2)
        firma = cierre(self, "")
        self.play(FadeIn(firma), run_time=0.6)
        self.wait(1.0)
