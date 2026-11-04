#!/bin/bash
# Renderiza los cinco clips en calidad final (1080x1920, 60 fps) y los copia a videos/.
# Uso: ./render_todos.sh   (requiere manim; aquí: /root/venv-manim/bin/manim)
MANIM=${MANIM:-manim}
MEDIA=${MEDIA:-./media}
mkdir -p videos
render() {  # $1 = fichero, $2 = escena, $3 = nombre final
  $MANIM render -q h --disable_caching --media_dir "$MEDIA/$2" "$1" "$2" > "logs_$2.txt" 2>&1 \
    && cp "$(find "$MEDIA/$2/videos/${1%.py}" -name "$2.mp4" | head -1)" "videos/$3" \
    && echo "OK $3" || echo "FALLO $2"
}
render clip1_radio.py       Clip1Radio       01_radio_polos_complejos.mp4 &
render clip2_recurrencia.py Clip2Recurrencia 02_edo_a_recurrencia.mp4 &
wait
render clip3_coseno.py      Clip3Coseno      03_serie_coseno.mp4 &
render clip4_airy.py        Clip4Airy        04_airy.mp4 &
wait
render clip5_legendre.py    Clip5Legendre    05_legendre.mp4
