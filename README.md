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

Para usar pox con la logica de learning switch usar el comando:

```
python pox.py l2_learning.py
```
Si queremos especificar el nivel de logging usar:

```
python pox.py log.level --DEBUG l2_learning.py (o INFO, WARNING, ERROR)
```

Por defecto pox escucha a todas las ips en el puerto 6633.
Se puede especificar otra ip o puerto de la siguiente manera

```
python pox.py openflow.of_01 --port=<puerto> --address=<ip>  l2_learning.py
```

Para levantar mininet con n switches y pox como controlador en una terminal 
```
sudo mn --custom topologia.py --topo customTopo,switches=N --controller=remote --switch=ovsk
```


Para usar POX con el firewall custom, usar el comando:

```
python pox.py  firewall l2_learning
```

En el firewall custom se puede indicar con el parametro --dpids los switches a los que se les aplica el firewall, por ejemplo:

```
python pox.py  firewall --dpids=1 l2_learning
```
Aplica el firewall solo al switch 1, si no se indica el parametro se aplica a todos los switches de la topologia.