# Tema 5 (Parte I) — Clips verticales

Cinco clips de unos 30 s en formato vertical (1080 × 1920, 60 fps), animados con
[Manim Community](https://www.manim.community/) en estilo 3Blue1Brown y con la estética
oscura de los apuntes (fondo negro, Computer Modern, acentos cian / violeta / ámbar).
Sin voz: la explicación avanza con fórmulas y gráficas.

| Vídeo | Contenido |
|---|---|
| `videos/01_radio_polos_complejos.mp4` | $1/(1+x^2)$ es suave en $\mathbb R$ pero su serie sólo converge en $\lvert x\rvert<1$: los polos $\pm i$ fijan el radio (Fuchs). |
| `videos/02_edo_a_recurrencia.mp4` | Punto ordinario, ansatz, índices mudos, producto de Cauchy, recurrencia y cadena de dependencias ($a_0$, $a_1$ libres). |
| `videos/03_serie_coseno.mp4` | $y''+y=0$: coeficientes paso a paso y sumas parciales que reconstruyen $\cos x$; $R=\infty$. |
| `videos/04_airy.mp4` | $y''=xy$: recurrencia de salto tres, tres cadenas, series $y_1,y_2$ y funciones $\mathrm{Ai}$, $\mathrm{Bi}$. |
| `videos/05_legendre.mp4` | Recurrencia de Legendre, truncamiento en polinomios $P_\ell$, divergencia en $x=\pm1$ y cuantización de $\ell$. |

## Renderizado

```bash
pip install manim            # requiere LaTeX, ffmpeg, cairo y pango
./render_todos.sh            # calidad final -> videos/
CLIP_PREVIA=1 manim render -q l clip1_radio.py Clip1Radio   # vista previa rápida (540x960, 15 fps)
```

`estilo.py` fija el formato, la paleta, la plantilla LaTeX y los elementos comunes
(cabecera, cajas con pestaña, ejes); `utiles.py` reúne utilidades gráficas. El contenido
importante se mantiene dentro de la zona segura de la interfaz de TikTok.
