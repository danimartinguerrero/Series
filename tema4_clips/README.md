# Tema 4 (Parte I) — Clip «Duelo en 𝓛: δ contra G»

Clip vertical (1080 × 1920, 60 fps, ~29 s) animado con Manim: dos monigotes originales,
con cabezas δ (cian) y G (ámbar), combaten con las herramientas del tema.

1. δ lanza un **impulso unitario** δ(x − x̃); G lo atrapa y lo clava en x̃.
2. Surge la **respuesta causal** G(x, x̃) (nula antes del impulso), que derriba a δ.
3. δ responde con una **lluvia de impulsos** b(x) = ∫ b(x̃) δ(x − x̃) dx̃.
4. G suma las respuestas: **superposición** y_p = ∫ G b dx̃.
5. δ se cubre con la **variación de constantes** (W k′ = b, escudo W⁻¹) y, en el choque,
   descubren que es el mismo cálculo.

```bash
manim render -q h duelo_green.py DueloGreen            # calidad final
CLIP_PREVIA=1 manim render -q l duelo_green.py DueloGreen   # vista previa
```

`monigote.py` contiene el esqueleto articulado (cinemática directa, posturas interpolables)
y los efectos (destellos, partículas, impulsos).
