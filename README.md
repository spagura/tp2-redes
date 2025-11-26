# tp2-redes

# INDICE

- [Como correr los scripts](#como-correr-los-scripts)
  - [Firewall](#firewall)
  - [Explicación de cada script](#explicación-de-cada-script)
    - [normal_case.sh](#normal_casesh)
    - [firewall.sh](#firewallsh)
    - [pingall.sh](#pingallsh)
    - [h1_to_h4.sh](#h1_to_h4sh)
    - [h4_to_h1.sh](#h4_to_h1sh)
    - [h1_to_port_5001.sh](#h1_to_port_5001sh)
    - [udp_to_80.sh](#udp_to_80sh)
  - [Como_ejecutarlo](#como-ejecutarlo)
  - [Objetivo de cada script](#objetivo-de-cada-script)
- [EN CASO DE QUE LOS SCRIPTS NO FUNCIONEN](#en-caso-de-que-los-scripts-no-funcionen)
  - [POX](#pox)
  - [Levantar POX con firewall custom](#levantar-pox-con-firewall-custom)
  - [Para crear el mininet con N switches (sin protocolo)](#para-crear-el-mininet-con-n-switches-sin-protocolo)
  - [Forma de correrlo](#forma-de-correrlo)
  - [IPERF](#iperf)

# Como correr los scripts

####  Abre el archivo de configuración y actualiza las variables para que coincidan con tu sistema

####  Todos los comandos de los scripts deben realizarse en la carpeta scripts

## Firewall

Antes de ejecutar cualquier script de Mininet, ejecutá el script del firewall. Debes

Abrí una terminal en la carpeta scripts y escribí:

```bash
bash firewall.sh
```

## Explicaicon de cada script:

### normal_case.sh

Inicia la topología de manera normal.

Corre conexiones TCP entre los hosts que **no serían bloqueadas** por las reglas de firewall.

Su objetivo es mostrar cómo funciona la red cuando todo está bien.

### firewall.sh

Inicia Mininet con el firewall de POX y carga tus reglas.

### pingall.sh

Ejecuta `pingall` dentro de la topología de Mininet.

Este script muestra rápidamente que el aprendizaje de nivel 2 está correctamente configurado y funcionando con POX.

### h1_to_h4.sh

Levanta un servidor TCP en h4.
Desde h1 corre un `iperf` TCP hacia h4.
Quedará intentando conectar, debés interrumpirlo con **Ctrl + C**.

También levanta un servidor UDP en h4 e intenta conectarse desde h1.

Luego muestra los logs de h4 para ambos servidores, donde **no debería aparecer ningún paquete recibido**, indicando que el firewall lo bloquea correctamente.

### h4_to_h1.sh

Lo mismo que el anterior, pero en dirección invertida.

### h1_to_port_5001.sh

Crea servidores UDP en H2 y H3.
Intenta alcanzarlos desde H1 y luego muestra los logs de ambos servidores.
Los logs deben estar vacíos, ya que los paquetes deben ser bloqueados por el firewall.

### udp_to_80.sh

Para probar la regla del firewall que bloquea **todo puerto 80**, levanta un servidor UDP en cada host y luego intenta alcanzarlos desde todos los demás hosts.
Muestra los logs de los 4 servidores: todos deben estar vacíos.

## Como ejecutarlo

Todos los scripts siguen el mismo patrón:

<u> Iniciar Mininet + Firewall POX: </u>
```bash
bash firewall.sh
```

<u> Ejecutar pruebas de conectividad: </u>

En otra terminal:
```bash
bash pingall.sh
```

<u> Ejecutar pruebas TCP/UDP: </u>

```bash
bash h1_to_h4.sh
```
```bash
bash h4_to_h1.sh
```
```bash
bash h1_to_port_5001.sh
```
```bash
bash udp_to_80.sh
```

<u> Caso normal sin bloqueo del firewall: </u>
```bash
bash normal_case.sh
```

## Objetivo de cada script

normal_case.sh: comportamiento base.

firewall.sh: carga las reglas del firewall.

pingall.sh: verifica conectividad.

hX_to_hY scripts: testean tráfico en una dirección.

port/udp scripts: validan reglas de puerto/protocolo.


<br>


# EN CASO DE QUE LOS SCRIPTS NO FUNCIONEN

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

<br>

### IPERF

Abrir terminales con xterm en el host que prefieran:

```bash
xterm h1
xterm h2
xterm h3
...
```

<u> Montar servidor TCP </u>

Dentro de xterm en el host donde desee levantar el servidor:

```bash
iperf -s -p "puerto a eleccion"
```

<u> Montar servidor UDP </u>

```bash
iperf -s -u -p "puerto a eleccion"
```

<u> Conectarse a servidor TCP </u>

Desde otro host, intente conectarse al servidor levantado con:

```bash
iperf -c "ip de host" -p "puerto"
```

<u> Conectarse a servidor UDP </u>


```bash
iperf -c "ip de host" -u -p "puerto"
```