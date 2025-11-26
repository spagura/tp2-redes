#!/bin/bash

source scripts.config

N=$SWITCHES
TOPO_PATH=$TOPO_PATH

sudo mn --custom $TOPO_PATH --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

h1 iperf -s -u -p 80 >/tmp/h1_udp80_server.log 2>&1 &

h2 iperf -c 10.0.0.1 -u -p 80 -t 2
h3 iperf -c 10.0.0.1 -u -p 80 -t 2

h1 kill %iperf 2>/dev/null

h2 iperf -s -u -p 80 >/tmp/h2_udp80_server.log 2>&1 &

h1 iperf -c 10.0.0.2 -u -p 80 -t 2
h3 iperf -c 10.0.0.2 -u -p 80 -t 2
h4 iperf -c 10.0.0.2 -u -p 80 -t 2

h2 kill %iperf 2>/dev/null

h3 iperf -s -u -p 80 >/tmp/h3_udp80_server.log 2>&1 &

h1 iperf -c 10.0.0.3 -u -p 80 -t 2
h2 iperf -c 10.0.0.3 -u -p 80 -t 2
h4 iperf -c 10.0.0.3 -u -p 80 -t 2

h3 kill %iperf 2>/dev/null

h4 iperf -s -u -p 80 >/tmp/h4_udp80_server.log 2>&1 &

h2 iperf -c 10.0.0.4 -u -p 80 -t 2
h3 iperf -c 10.0.0.4 -u -p 80 -t 2

h4 kill %iperf 2>/dev/null

h1 cat /tmp/h1_udp80_server.log

h2 cat /tmp/h2_udp80_server.log

h3 cat /tmp/h3_udp80_server.log

h4 cat /tmp/h4_udp80_server.log

exit
EOF
