#!/bin/sh
# Régénère public/ à partir de tools/maquette.html (source unique des contenus FR/EN).
set -e
cd "$(dirname "$0")/.."
rm -rf /tmp/r4i-build
python3 tools/build.py tools/maquette.html /tmp/r4i-build
cp tools/site.js /tmp/r4i-build/assets/
python3 tools/extras.py /tmp/r4i-build tools/logo-defs.txt
rm /tmp/r4i-build/netlify.toml
rm -rf public && mv /tmp/r4i-build public
echo "public/ régénéré"
