#!/bin/bash

source scripts.config

N=$SWITCHES
TOPO_PATH=$TOPO_PATH

sudo mn --custom $TOPO_PATH --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

h3 iperf -s -p 5002 >/tmp/h3_iperf_tcp_server.log 2>&1 &

h1 iperf -c 10.0.0.3 -p 5002 -t 5

h2 iperf -c 10.0.0.3 -p 5002 -t 5

h4 iperf -c 10.0.0.3 -p 5002 -t 5

h3 cat /tmp/h3_iperf_tcp_server.log

exit
EOF
