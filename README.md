# tp2-redes

Comandos

Para crear el mininet con N switches

sudo mn --custom topologia.py --topo customTopo,switches=N --controller=none --switch=ovsk

Si estan usando UBUNTU, dentro de mininet hay que mandar

mininet> sh ovs-vsctl set-fail-mode s1 standalone
mininet> sh ovs-vsctl set-fail-mode s2 standalone
mininet> sh ovs-vsctl set-fail-mode s3 standalone
mininet> sh ovs-vsctl set-fail-mode s4 standalone
mininet> sh ovs-vsctl set-fail-mode s5 standalone

pingall en este momento funciona

para ver en wireshark los pings, se filtra con
 --- icmp ---

no hay firewall
no hay controlador