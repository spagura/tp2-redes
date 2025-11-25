#!/bin/bash

# Número de switches
N=2

echo ">>> Levantando Mininet con $N switches..."
sudo mn --custom topologia.py --topo customTopo,switches=$N --controller=remote --switch=ovsk << 'EOF'

h3 iperf -s -p 5002 >/tmp/h4_iperf_tcp_server.log 2>&1 &

h1 iperf -c 10.0.0.3 -p 5002 -t 5

h2 iperf -c 10.0.0.3 -p 5002 -t 5

h4 iperf -c 10.0.0.3 -p 5002 -t 5

exit
EOF
