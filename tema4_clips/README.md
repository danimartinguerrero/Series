# Tema 4 (Parte I) — Clip «Duelo en 𝓛: δ contra G»

Clip vertical (1080 × 1920, 60 fps, ~29 s) animado con Manim. Dos monigotes pequeños y
originales, con cabezas **δ** (cian) y **G** (ámbar), se baten **a distancia** con armas
matemáticas; cada ataque deja como consecuencia el resultado del tema al que alude, que se
anota en el «Registro del duelo»:

1. **Ráfaga de impulsos** δ(x − x̃) → G los para con la espada **∫** y, al clavarla, nace la
   **función de Green causal** (onda que sólo avanza hacia delante; δ la esquiva con una voltereta).
2. **Serie Σ** de e^{λx} → escudo **∏** (factorización 𝓛 = aₙ∏(D − λ_k)^{m_k}) que la parte en
   las exponenciales e^{λ_k x}.
3. **Plano ℂ** con las raíces −γ ± iΩ → **rayo amortiguado** e^{−γx} cos Ωx.
4. **Choque de rayos** ∫G b dx̃ contra W k′ = b → explosión: variación de constantes ≡ método de Green.

```bash
manim render -q h duelo_green.py DueloGreen                 # calidad final
CLIP_PREVIA=1 manim render -q l duelo_green.py DueloGreen   # vista previa
```

`monigote.py`: esqueleto articulado escalable (cinemática directa, posturas interpolables,
cabeza con glifo) y efectos (destellos, partículas, impulsos).
