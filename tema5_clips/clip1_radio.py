"""Clip 1 — El radio de convergencia lo deciden los polos complejos."""
from utiles import *


class Clip1Radio(Scene):
    def construct(self):
        cab = cabecera(1, 5, r"El radio lo deciden los polos complejos")
        pie_ = pie()
        self.play(FadeIn(cab[0], shift=DOWN * 0.2), FadeIn(cab[1]), run_time=0.6)
        self.play(Write(cab[2]), GrowFromEdge(cab[3], LEFT), run_time=1.2)
        self.add(pie_)

        # --- 1. Una función perfectamente suave en R -----------------------------------
        f_tex = M(r"f(x)=\frac{1}{1+x^{2}}", size=66)
        f_tex.move_to(UP * 4.35 + LEFT * 0.35)
        ax = ejes([-2.5, 2.5, 1], [-1, 2, 1], x_length=7.4, y_length=5.3)
        ax.move_to(UP * 0.55 + LEFT * 0.35)
        x_lab = M("x", size=30, color=GRIS).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        f = lambda x: 1 / (1 + x * x)
        graf = ax.plot(f, x_range=[-2.5, 2.5], color=BLANCO, stroke_width=5)
        self.play(Write(f_tex), run_time=1.0)
        self.play(Create(ax), FadeIn(x_lab), run_time=0.8)
        self.play(Create(graf), run_time=1.3)
        suave = nota(r"suave, acotada y sin singularidades en $\mathbb R$", size=38)
        suave.move_to(DOWN * 3.25 + LEFT * 0.35)
        self.play(FadeIn(suave, shift=UP * 0.15), run_time=0.6)
        self.wait(0.5)

        # --- 2. Su serie de Taylor ---------------------------------------------------------
        serie = M(r"\frac{1}{1+x^{2}}=1-x^{2}+x^{4}-x^{6}+\cdots", size=54)
        serie.move_to(suave)
        self.play(FadeOut(suave, shift=UP * 0.15), FadeIn(serie, shift=UP * 0.15), run_time=0.8)

        # zonas |x| > 1 y sumas parciales
        zona_i = Rectangle(width=ax.c2p(-1, 0)[0] - ax.c2p(-2.5, 0)[0],
                           height=ax.y_length, stroke_width=0,
                           fill_color=GRISOSCURO, fill_opacity=0.55)
        zona_i.move_to(ax.c2p(-1.75, 0.5))
        zona_d = zona_i.copy().move_to(ax.c2p(1.75, 0.5))
        guias = VGroup(*[DashedLine(ax.c2p(s, -1), ax.c2p(s, 2), dash_length=0.08,
                                    color=GRISMEDIO, stroke_width=2) for s in (-1, 1)])
        self.play(FadeIn(zona_i), FadeIn(zona_d), Create(guias), run_time=0.6)
        self.bring_to_front(graf)

        m = ValueTracker(1)

        def parcial():
            k = int(round(m.get_value()))
            return curva_recortada(ax, lambda x: sum((-x * x) ** j for j in range(k + 1)),
                                   -2.5, 2.5, -1, 2, CIAN, ancho=4)

        sumas = always_redraw(parcial)
        etq = always_redraw(lambda: etiqueta_fondo(
            M(r"S_{%d}" % (2 * int(round(m.get_value()))), size=46, color=CIAN))
            .move_to(ax.c2p(0, 1.72)))
        self.play(FadeIn(sumas), FadeIn(etq), run_time=0.5)
        for k in range(2, 13):
            self.play(m.animate.set_value(k), run_time=0.42, rate_func=linear)
        r_lab = etiqueta_fondo(M(r"R=1", size=48, color=AMBAR))
        r_lab.move_to(ax.c2p(1.75, 1.5))
        div = VGroup(*[etiqueta_fondo(T("diverge", size=32, color=GRIS)).move_to(ax.c2p(s, -0.65))
                       for s in (-1.75, 1.75)])
        self.play(FadeIn(r_lab, scale=1.2), FadeIn(div), run_time=0.7)

        pregunta = T(r"¿Por qué $R=1$ si $f$ es\\ suave en todo $\mathbb R$?", size=50, color=BLANCO)
        pregunta.move_to(serie)
        self.play(FadeOut(serie, shift=UP * 0.2), FadeIn(pregunta, shift=UP * 0.2), run_time=0.8)
        self.wait(1.2)

        # --- 3. La respuesta está en el plano complejo ------------------------------------
        sumas.clear_updaters()
        etq.clear_updaters()
        self.play(*[FadeOut(o) for o in (ax, x_lab, graf, sumas, etq, zona_i, zona_d,
                                         guias, r_lab, div, pregunta)],
                  f_tex.animate.become(M(r"f(z)=\frac{1}{1+z^{2}},\quad z\in\mathbb C", size=60)
                                       .move_to(UP * 4.55 + LEFT * 0.35)),
                  run_time=1.0)

        L = 2.4
        plano = NumberPlane(x_range=[-L, L, 1], y_range=[-L, L, 1], x_length=6.1, y_length=6.1,
                            background_line_style=dict(stroke_color=GRISOSCURO, stroke_width=1.2,
                                                       stroke_opacity=0.6),
                            axis_config=dict(stroke_color=GRIS, stroke_width=2))
        plano.move_to(UP * 0.55 + LEFT * 0.35)
        img = imagen_fase(lambda z: 1 / (1 + z * z), (-L, L), (-L, L), res=1000, brillo=0.78)
        img.set(width=plano.width, height=plano.height).move_to(plano)
        borde = Square(side_length=6.1, stroke_color=GRISMEDIO, stroke_width=2).move_to(plano)
        self.play(FadeIn(img), Create(plano), Create(borde), run_time=1.4)
        lab_re = etiqueta_fondo(M(r"\operatorname{Re} z", size=28, color=TEXTO)).next_to(
            plano.c2p(L, 0), UP, buff=0.1).shift(LEFT * 0.55)
        lab_im = etiqueta_fondo(M(r"\operatorname{Im} z", size=28, color=TEXTO)).next_to(
            plano.c2p(0, L), RIGHT, buff=0.1).shift(DOWN * 0.3)
        self.play(FadeIn(lab_re), FadeIn(lab_im), run_time=0.4)

        ceros = M(r"1+z^{2}=0\;\Longrightarrow\; z=\pm\, i", size=54)
        ceros.move_to(DOWN * 3.55 + LEFT * 0.35)
        polos = VGroup(cruz(plano.c2p(0, 1), BLANCO, tam=0.2, ancho=7),
                       cruz(plano.c2p(0, -1), BLANCO, tam=0.2, ancho=7))
        lab_p = VGroup(etiqueta_fondo(M(r"+i", size=38)).next_to(plano.c2p(0, 1), UL, buff=0.22),
                       etiqueta_fondo(M(r"-i", size=38)).next_to(plano.c2p(0, -1), DL, buff=0.22))
        self.play(Write(ceros), run_time=0.9)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in polos], lag_ratio=0.3),
                  FadeIn(lab_p), run_time=0.9)

        intervalo = Line(plano.c2p(-1, 0), plano.c2p(1, 0), stroke_width=10, color=AMBAR)
        circ = Circle(radius=plano.c2p(1, 0)[0] - plano.c2p(0, 0)[0], color=BLANCO, stroke_width=5)
        circ.move_to(plano.c2p(0, 0))
        radio = DashedLine(plano.c2p(0, 0), plano.c2p(np.cos(-0.6), np.sin(-0.6)),
                           color=BLANCO, stroke_width=3, dash_length=0.1)
        r_txt = etiqueta_fondo(M(r"R=1", size=42, color=BLANCO)).move_to(plano.c2p(1.6, -1.05))
        self.play(Create(intervalo), run_time=0.6)
        self.play(Create(circ), Create(radio), run_time=1.3)
        self.play(FadeIn(r_txt, scale=1.2), run_time=0.5)
        self.play(Indicate(polos, color=AMBAR, scale_factor=1.35), run_time=0.9)

        # --- 4. Conclusión ---------------------------------------------------------------
        concl = VGroup(
            M(r"R=\dist\bigl(x_0,\ \text{polo complejo más cercano}\bigr)", size=40),
            M(r"\text{Fuchs: }\;R\;\ge\;\dist\bigl(x_0,\ \{P=0\}\subset\mathbb C\bigr)",
              size=38, color=CIAN),
        ).arrange(DOWN, buff=0.32)
        caja_c = caja(concl, AMBAR, titulo="Resultado")
        caja_c.move_to(DOWN * 3.85 + LEFT * 0.35)
        self.play(FadeOut(ceros, shift=DOWN * 0.2), FadeIn(caja_c, shift=UP * 0.2), run_time=1.0)
        self.wait(2.6)
        # tarjeta final: el plano se encoge y queda el mensaje
        grupo_plano = Group(img, plano, borde, lab_re, lab_im, polos, lab_p, intervalo, circ,
                            radio, r_txt)
        self.play(FadeOut(caja_c, shift=DOWN * 0.2), FadeOut(f_tex, shift=UP * 0.2),
                  grupo_plano.animate.scale(0.72).move_to(UP * 2.3 + LEFT * 0.35), run_time=1.0)
        final = T(r"El disco de convergencia\\ no mira el eje real:\\ mira el plano complejo.",
                  size=54, color=BLANCO)
        final.move_to(DOWN * 2.6 + LEFT * 0.35)
        self.play(Write(final), run_time=1.4)
        self.wait(1.8)
