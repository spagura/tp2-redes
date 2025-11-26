#!/bin/bash

source scripts.config

POX_DIR=$POX_PATH

cd "$POX_DIR" || exit 1

python3 pox.py  firewall forwarding.l2_learning