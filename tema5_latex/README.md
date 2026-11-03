# Ecuaciones Diferenciales — Tema 5 (Parte I): puntos ordinarios y series enteras

Apuntes formalizados en LaTeX, con diseño oscuro (fondo negro, texto claro en
Computer/Latin Modern) y figuras TikZ/pgfplots.

## Compilación

```bash
cd tema5_latex
latexmk main.tex          # LuaLaTeX + biber (varias pasadas, unos 10 min)
```

* Se compila con **LuaLaTeX**: la superficie 3D de la portada y los retratos de
  fase superan la memoria de pdfLaTeX.
* Para iterar deprisa, crea un fichero vacío `rapido.flag`: las superficies y
  retratos de fase se generan a baja resolución y cada pasada tarda unos
  20 s. Bórralo antes de la compilación final.
* Las tablas de `datos/` (Airy, ejemplo gaussiano, sumas parciales de
  Legendre) se regeneran con `python3 scripts/generar_datos.py`, que suma las
  propias series del texto en aritmética decimal de 60 cifras.

## Estructura

| Fichero | Contenido |
|---|---|
| `main.tex`, `portada.tex`, `preambulo.tex` | Documento, portada y preámbulo (paleta oscura, entornos con pestaña) |
| `secciones/01_motivacion.tex` | Ecuaciones en diferencias; analogía discreto ↔ continuo |
| `secciones/02_analiticidad.tex` | Planteamiento, funciones analíticas, $e^{-1/x^2}$, regularidad de las soluciones |
| `secciones/03_polos.tex` | Polos, Laurent, clasificación de singularidades, radio y polos complejos |
| `secciones/04_puntos_ordinarios.tex` | Teorema de Fuchs, recurrencia, producto de Cauchy, sistema fundamental, demostración por mayorantes |
| `secciones/05_ejemplos.tex` | Oscilador armónico, Airy, $y''+xy'+y=0$, Legendre |
| `secciones/06_resumen.tex` | Receta, tabla resumen, diagrama de flujo y perspectivas (Parte II) |
| `figuras/` | Figuras TikZ/pgfplots (`estilos.tex` reúne los estilos comunes) |
| `datos/`, `scripts/` | Tablas numéricas y el script que las genera |
| `referencias.bib` | Bibliografía |
