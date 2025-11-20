# TP2 – Redes

## Comandos útiles

### Crear el Mininet con N switches
```
sudo mn --custom topologia.py --topo customTopo,switches=N --controller=none --switch=ovsk
```

Si usás Ubuntu, dentro de Mininet ejecutar:
```
mininet> sh ovs-vsctl set-fail-mode s1 standalone
mininet> sh ovs-vsctl set-fail-mode s2 standalone
mininet> sh ovs-vsctl set-fail-mode s3 standalone
mininet> sh ovs-vsctl set-fail-mode s4 standalone
mininet> sh ovs-vsctl set-fail-mode s5 standalone
```

Después de esto, pingall funciona.

### Ver pings en Wireshark
Filtrar por:

--- icmp ---

------------------------------------------------------------

## POX

### Learning Switch
Para usar pox con la logica de learning switch:
```
python pox.py l2_learning.py
```

### Con nivel de logging específico:
Si queremos especificar el nivel de logging usar:

```
python pox.py log.level --DEBUG l2_learning.py (o INFO, WARNING, ERROR)
```

### Cambiar puerto o IP donde escucha POX:
Por defecto pox escucha a todas las ips en el puerto 6633.
Se puede especificar otra ip o puerto de la siguiente manera

```
python pox.py openflow.of_01 --port=<puerto> --address=<ip>  l2_learning.py
```

### Levantar Mininet con N switches y POX como controlador
```
sudo mn --custom topologia.py --topo customTopo,switches=N --controller=remote --switch=ovsk
```

### Firewall custom

Para usar POX con el firewall custom, usar el comando:

```
python pox.py  firewall l2_learning
```

En el firewall custom se puede indicar con el parametro --dpids los switches a los que se les aplica el firewall, por ejemplo:

```
python pox.py  firewall --dpids=1 l2_learning
```
Aplica el firewall solo al switch 1, si no se indica el parametro se aplica a todos los switches de la topologia.

Si no se especifica --dpids, se aplica a todos los switches.



