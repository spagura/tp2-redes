#!/bin/bash

# Ruta al directorio pox
POX_DIR="/home/lied/Desktop/redes/tp2/firewall/pox"

cd "$POX_DIR" || exit 1

echo ">>> Levantando POX con firewall y learning switch..."
python3.8 pox.py  firewall forwarding.l2_learning