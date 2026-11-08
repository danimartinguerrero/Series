# Tema 4 — publicaciones para Instagram

Resumen visual del Tema 4 (EDO lineales de orden superior) con el mismo estilo oscuro de los apuntes.

| Fichero | Formato | Contenido |
|---|---|---|
| `png/diapo-1.png` … `png/diapo-7.png` | Carrusel 4:5, 1080×1350 | Portada-collage, estructura, wronskiano y Abel–Liouville, coeficientes constantes, variación de las constantes, función de Green, resumen |
| `png/historia-1.png` | Historia 9:16, 1080×1920 | Título, cascada de respuestas a impulsos, cuatro ideas clave y la fórmula final (respeta las zonas seguras de arriba y abajo) |

## Regenerar

```bash
cd tema4_instagram
latexmk          # compila carrusel.tex e historia.tex (LuaLaTeX)
./exportar.sh    # exporta los PNG a png/
```

Reutiliza `../tema4_latex/figuras/estilos.tex`, `../tema4_latex/datos/superposicion.dat` y la imagen de portada. El preámbulo común está en `comun.tex`.
