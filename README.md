# tp2-redes

## Comandos

### POX 

Luego de clonar el repositorio de POX provisto por la cátedra (link incluido en el PDF del trabajo práctico), es importante ejecutar todos los comandos de POX dentro de la carpeta principal del proyecto, es decir, en el directorio donde se encuentra el archivo pox.py. Esto garantiza el correcto funcionamiento del controlador.

Para usar pox con la logica de learning switch usar el comando:

```bash
python pox.py forwarding.l2_learning
```

Si queremos especificar el nivel de logging usar:

```bash
python pox.py log.level --DEBUG forwarding.l2_learning (o INFO, WARNING, ERROR)
```

Por defecto pox escucha a todas las ips en el puerto 6633. Pero se puede especificar otra ip o puerto de la siguiente manera

```bash
python pox.py openflow.of_01 --port=<puerto> --address=<ip>  forwarding.l2_learning
```
<br>

### Levantar POX con firewall custom

Para usar POX con el firewall programado para este trabajo practico, usar el comando:

```bash
python pox.py  firewall forwarding.l2_learning
```

En el firewall custom se puede indicar con el parametro --dpids los switches a los que se les aplica el firewall, por ejemplo:

```bash
python pox.py  firewall --dpids=1 forwarding.l2_learning
```
Aplica el firewall solo al switch 1, si no se indica el parametro se aplica a todos los switches de la topologia.

<br>


### Para crear el mininet con N switches (sin protocolo)

Nos ubicamos en la carpeta del trabajo práctico, donde se encuentra el archivo `topologia.py`.

```bash
sudo mn --custom topologia.py --topo customTopo,switches=N --controller=none --switch=ovsk
```

Si estan usando UBUNTU, dentro de mininet hay que mandar

```bash
mininet> sh ovs-vsctl set-fail-mode s1 standalone
mininet> sh ovs-vsctl set-fail-mode s2 standalone
mininet> sh ovs-vsctl set-fail-mode s3 standalone
mininet> sh ovs-vsctl set-fail-mode s4 standalone
mininet> sh ovs-vsctl set-fail-mode s5 standalone
....
```

Esto hace que si al switch no se le indica un controlador, se comporta como un switch learning normal (l2_learning)

<br>

Para levantar minimet con n switches y pox como controlador

```bash
sudo mn --custom topologia.py --topo customTopo,switches=N --controller=remote --switch=ovsk
```
<br>

### Forma de correrlo

Para ejecutar el trabajo de la forma esperada, es necesario abrir dos terminales: una para levantar POX con el firewall personalizado junto con l2_learning, y otra para iniciar Mininet utilizando POX como controlador.