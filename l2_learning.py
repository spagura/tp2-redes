from pox.core import core # Nucleo principal de POX
import pox.openflow.libopenflow_01 as of # clases Openflow(flow_mod, packet_in, etc)

log = core.getLogger() # Permite mostrar mensajes en la consola

class LearningSwitch(object):
    # Representa un switch de aprendizaje simple
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self) # POX va a llamarte cuando haya eventos (PacketIN)

    def _handle_PacketIn(self, event):
        # Este metodo se ejecuta cuando el switch no sabe a que puerto mandar un paquete
        # Se llama automaticamente gracias a connection.addListeners(self)
        # NO cambien el nombre del metodo.
        packet = event.parsed
        in_port = event.port
        src_mac = str(packet.src)
        dst_mac = str(packet.dst)

        # Aprende la direccion MAC de origen, "la MAC esta conectada al puerto Y"
        self.mac_to_port[src_mac] = in_port
        log.debug("Aprendio direccion MAC %s en puerto %s", src_mac, in_port)

        if dst_mac in self.mac_to_port:
            out_port = self.mac_to_port[dst_mac]
            log.debug("Forwardeando paquete to %s en puerto %s", dst_mac, out_port)

            # Todo el resto del if crea una regla de flujo para el destino conocido

            # Configura la coincidencia del flujo
            # Ejemplo (no literal): match: in_port = 1, dl_dst = 00:00:00:00:00:03
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, in_port) 

            # Cuando un paquete haga match, envialo por el puerto out_port
            msg.actions.append(of.ofp_action_output(port=out_port)) 

            # POX le dice al switch mediante OpenFlow: Usa el paquete que tengas guardado en ese buffer y procesalo usando la regla
            msg.buffer_id = event.ofp.buffer_id
            self.connection.send(msg)
        else:
            #Flood si no conocemos el destino
            log.debug(f"[Switch {event.connection.dpid}] Flooding destino desconocido MAC {dst_mac}")

            msg = of.ofp_packet_out()
            msg.buffer_id = event.ofp.buffer_id

            # Flooding por todos los puertos excepto el de entrada
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            self.connection.send(msg)
    
def launch():
    # Cuando un switch se conecta, crea una instancia de LearningSwitch
    # Hay 1 instancia LearningSwitch por switch
    log.info("Iniciando controlador l2_learning")
    core.openflow.addListenerByName("ConnectionUp", lambda event: LearningSwitch(event.connection))