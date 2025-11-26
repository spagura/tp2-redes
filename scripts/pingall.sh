#!/bin/bash

source scripts.config

N=$SWITCHES
TOPO_PATH=$TOPO_PATH

sudo mn --custom $TOPO_PATH --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

pingall

exit
EOF