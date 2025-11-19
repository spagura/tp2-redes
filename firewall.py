#mover el archivo a la carpeta pox/ext


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp
from pox.lib.packet.udp import udp
from pox.lib.packet.icmp import icmp
from pox.lib.util import dpid_to_str
import json
import os

log = core.getLogger()

# Ruta al archivo de reglas (en el mismo directorio que este archivo)
RULES_FILE = os.path.join(os.path.dirname(__file__), "reglas_fw.json")


class Firewall(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        switch_id = dpid_to_str(self.connection.dpid)
        try:
            file = open(RULES_FILE)
            self.rules = json.load(file)
            file.close()
            log.info(" se cargan %d reglas del archivo %s en el switch %s",
                     len(self.rules), RULES_FILE, switch_id)
        except Exception as e:
            log.error(" Error al cargar reglas para el firewall en el switch %s desde el archivo %s: %s ",
                      switch_id, RULES_FILE, e)
            self.rules = []

    def _match_rules(self, packet, in_port):

        ip = packet.payload
        packet_protocol = ip.payload

        if not isinstance(ip, ipv4):
            log.debug(" No es un paquete IPv4, no se aplican reglas")
            return None

        # Log detallado: IP origen:puerto -> IP destino:puerto y protocolo
        try:
            src_ip = getattr(ip, "srcip", None)
            dst_ip = getattr(ip, "dstip", None)
            src_port = getattr(packet_protocol, "srcport", None) if packet_protocol is not None else None
            dst_port = getattr(packet_protocol, "dstport", None) if packet_protocol is not None else None

            if isinstance(packet_protocol, tcp):
                proto = "TCP"
            elif isinstance(packet_protocol, udp):
                proto = "UDP"
            elif isinstance(packet_protocol, icmp):
                proto = "ICMP"
            else:
                proto = type(packet_protocol).__name__ if packet_protocol is not None else None

            log.info("PKT -- switch=%s src=%s:%s dst=%s:%s proto=%s",
                     dpid_to_str(self.connection.dpid),
                     src_ip, src_port,
                     dst_ip, dst_port,
                     proto)
        except Exception:
            log.error("Error al recuperar campos del paquete para el log", exc_info=True)

        for rule in self.rules:
            action = rule.get("action")
            dst_port = rule.get("dst_port")

            log.info(" Evaluando regla: action=%s dst_port=%s", action, dst_port)

            #protocol = rule.get("protocol")
            #src_port = rule.get("src_port")

            # si quiero filtrar por protocolo
            # if protocol is not None:
            #     protocol = protocol.lower()
            #     if protocol == "tcp" and not isinstance(packet_protocol, tcp):
            #         continue
            #     if protocol == "udp" and not isinstance(packet_protocol, udp):
            #         continue
            #     if protocol == "icmp" and not isinstance(packet_protocol, icmp):
            #        continue



            # filtro por puerto destino
            if dst_port is not None:
                if not hasattr(packet_protocol, "dstport"):
                    continue
                try:
                    if int(packet_protocol.dstport) != int(dst_port):
                        continue
                except Exception:
                    log.error(" Error al comparar puerto destino en la regla")
                    continue

            # para filtrar por puerto origen
            # if src_port is not None:
            #     if not hasattr(packet_protocol, "srcport"):
            #         continue
            #     try:
            #         if int(packet_protocol.srcport) != int(src_port):
            #             continue
            #     except Exception:
            #         continue

            return action
        log.info(" No se encontro ninguna regla que coincida en switch %s",self.connection.dpid)
        return None

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        action = self._match_rules(packet, in_port)
        #log.info(" Accion determinada por las reglas: %s", action)
        if action == "deny":
            # Descarta e instala flow de drop
            log.info(" DROP paquete con dst_port=80 en switch %s",
                      event.connection.dpid)

            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, in_port)
            msg.buffer_id = event.ofp.buffer_id
            # No se agregan acciones, por lo que el paquete se descarta
            self.connection.send(msg)
            return


def launch(dpids=""):
    # dpids: lista separada por comas de los dpids donde se activa el firewall
    # si no se indica nada se activa el firewall en todos  los switchs
    if dpids:
        log.info(" Iniciando firewall custom en switchs con dpids = %s", dpids)
        allowed = set(int(d) for d in dpids.split(","))
    else:
        log.info(" Iniciando firewall custom en todos los switchs")
        allowed = None

    def start_switch(event):
        dpid = event.connection.dpid
        if allowed is None or dpid in allowed:
            log.info("Firewall ACTIVADO en switch %s", dpid)
            Firewall(event.connection)
        else:
            log.info("Firewall DESACTIVADO en switch %s", dpid)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
