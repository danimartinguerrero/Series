#!/usr/bin/env bash
# Exporta el carrusel (1080x1350, 4:5) y la historia (1080x1920, 9:16) a PNG.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p png
rm -f png/*.png
pdftoppm -png -scale-to-x 1080 -scale-to-y 1350 carrusel.pdf png/diapo
pdftoppm -png -scale-to-x 1080 -scale-to-y 1920 historia.pdf png/historia
