#!/bin/bash

source scripts.config

N=$SWITCHES
TOPO_PATH=$TOPO_PATH

sudo mn --custom $TOPO_PATH --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

h1 iperf -s -u -p 5001 >/tmp/h1_iperf_udp_server.log 2>&1 &

h4 iperf -c 10.0.0.4 -u -p 5001 -b 10M -t 5

h1 iperf -s -p 5002 >/tmp/h1_iperf_tcp_server.log 2>&1 &

h4 iperf -c 10.0.0.4 -p 5002 -t 5

h1 cat /tmp/h1_iperf_udp_server.log

h1 cat /tmp/h1_iperf_tcp_server.log

exit
EOF
