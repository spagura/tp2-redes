
# How to Run the Scripts

####  Open the config file and update the variables to reflect your system

## Setup the Firewall

Before running any mininet script, run the firewall script.

Open the shell in this folder and type

``` bash
bash firewall.sh
```

## Explanation of each script:

### normal_case.sh

Starts the topology normally.

Runs tcp connections between the hosts that would not be blocked by the firewall rules.

Its objective is to show how would the network work when everything is okay.
 

### firewall.sh

Starts Mininet with POX firewall and loads your rules.


### pingall.sh

Runs pingall inside the Mininet topology.

This script shows quickly that the level 2 learning is correctly set and running with POX-


### h1_to_h4.sh

Host a tcp server in h4.
From h1 runs a TCP iperf to h4.
It will halt trying to connect, you should interrupt it with ctrl + C.

It will Host a UDP server as well in h4 and try to contact from h1.

It will show the logs of h4 logs of both servers and not show any package received, correctly blocked by the firewall

### h4_to_h1.sh

Same as above but reversed direction.


### h1_to_port_5001.sh

Creates UDP servers in H2 and H3,
Tries to reach them from H1, then shows the logs for both servers.
The logs should be empty, as the packets have to be blocked by the firewall.


### udp_to_80.sh

To prove the Firewall rule that every port 80 is blocked,
It Host a UDP server for each Host and tries to reach them with every other host on the network.
Shows the logs for the 4 servers, everyone should be empty.


## How to Execute

All scripts follow the same pattern:

Start Mininet + POX firewall
``` bash
bash firewall.sh
```
Run connectivity tests

In another terminal:
``` bash
bash pingall.sh
```
``` bash
Run TCP/UDP tests
``` 
``` bash
bash h1_to_h4.sh
```
``` bash
bash h4_to_h1.sh
```
``` bash
bash h1_to_port_5001.sh
```
``` bash
bash udp_to_80.sh
```
Normal case without firewall blocking packages

``` bash
bash normal_case.sh
```

## Objective of the Scripts 

normal_case.sh: baseline behavior.

firewall.sh: load firewall rules.

pingall.sh: verify connectivity.

hX_to_hY scripts: test traffic in one direction.

port/udp scripts: validate port/protocol rules.