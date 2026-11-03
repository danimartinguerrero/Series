# Ecuaciones Diferenciales — Tema 4 (Parte I): EDO lineales de orden superior y funciones de Green

Apuntes formalizados en LaTeX con el mismo diseño oscuro que el Tema 5.

## Compilación

```bash
cd tema4_latex
latexmk main.tex          # LuaLaTeX + biber (menos de un minuto)
```

* La imagen de la portada (`figuras/portada_superficie.png`: respuestas a impulsos
  en cascada y su superposición) se regenera con `python3 scripts/generar_portada.py`
  (numpy, matplotlib y Pillow).
* `datos/superposicion.dat` (figura de superposición de impulsos) se regenera con
  `python3 scripts/generar_datos.py`.

## Estructura

| Fichero | Contenido |
|---|---|
| `main.tex`, `portada.tex`, `preambulo.tex` | Documento, portada y preámbulo |
| `secciones/01_estructura.tex` | Operador lineal, dimensión del núcleo (isomorfismo de datos iniciales), wronskiano, $y=y_h+y_p$ |
| `secciones/02_coef_constantes.tex` | Ansatz exponencial, factorización de $p(D)$, soluciones reales, oscilador amortiguado |
| `secciones/03_raices_multiples.tex` | Lema de la «derivada covariante», núcleo de $(D-\lambda)^m$, base general |
| `secciones/04_variacion.tex` | Variación de las constantes (forma matricial y caso $n=2$) |
| `secciones/05_green.tex` | Función de Green: definición, condiciones de salto, Green causal = variación de constantes, Poisson |
| `secciones/06_resumen.tex` | Resumen operativo, tabla de raíces y errores típicos |
| `figuras/`, `datos/`, `scripts/` | Figuras TikZ/pgfplots, datos numéricos y scripts |
| `referencias.bib` | Bibliografía |
