#!/bin/bash

source scripts.config

N=$SWITCHES
TOPO_PATH=$TOPO_PATH

sudo mn --custom $TOPO_PATH --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

h2 iperf -s -u -p 5001 >/tmp/h2_udp_server.log 2>&1 &
h3 iperf -s -u -p 5001 >/tmp/h3_udp_server.log 2>&1 &

h1 iperf -c 10.0.0.2 -u -p 5001 -t 3

h1 iperf -c 10.0.0.3 -u -p 5001 -t 3

h2 cat /tmp/h2_udp_server.log

h3 cat /tmp/h3_udp_server.log

exit
EOF
