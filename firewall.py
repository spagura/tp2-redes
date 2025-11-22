# mover el archivo a la carpeta pox/ext


from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.tcp import tcp
from pox.lib.packet.udp import udp
from pox.lib.packet.icmp import icmp
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr
import json
import os

log = core.getLogger()

# Ruta al archivo de reglas (en el mismo directorio que este archivo)
RULES_FILE = os.path.join(os.path.dirname(__file__), "reglas_fw.json")


def format_rule(action, rule_dst_ip, rule_dst_port, rule_protocol,
                rule_src_ip, rule_src_port, rule_priority):
    rule_msg = " regla: "
    if action is not None:
        rule_msg += f"action={action} "
    if rule_src_ip is not None:
        rule_msg += f"src_ip={rule_src_ip} "
    if rule_src_port is not None:
        rule_msg += f"src_port={rule_src_port} "
    if rule_dst_ip is not None:
        rule_msg += f"dst_ip={rule_dst_ip} "
    if rule_dst_port is not None:
        rule_msg += f"dst_port={rule_dst_port} "
    if rule_protocol is not None:
        rule_msg += f"protocol={rule_protocol} "
    if rule_priority is not None:
        rule_msg += f"priority={rule_priority} "
    return rule_msg

# Cargar reglas desde archivo (una sola vez al iniciar el controlador)
def load_rules_from_file():
    try:
        with open(RULES_FILE) as f:
            rules = json.load(f)
        log.info("Se cargaron %d reglas desde %s", len(rules), RULES_FILE)
        return rules
    except Exception as e:
        log.error("Error al cargar reglas desde %s: %s", RULES_FILE, e)
        return []


# Construye y instala en el switch flows de drop a partir de cada regla
def install_rules_on_connection(connection, rules):
    for rule in rules:
        action = rule.get("action")
        rule_src_ip = rule.get("src_ip")
        rule_src_port = rule.get("src_port")
        rule_dst_ip = rule.get("dst_ip")
        rule_dst_port = rule.get("dst_port")
        rule_protocol = rule.get("protocol").lower() if rule.get("protocol") is not None else None
        rule_priority = rule.get("priority")

        if rule_priority is None:
            log.error("La regla no tiene prioridad definida: %s", rule)
            continue

        rule_msg = format_rule(action, rule_dst_ip, rule_dst_port, rule_protocol, rule_src_ip,
                                     rule_src_port, rule_priority)
        log.info("Configurando %s", rule_msg)
        if action != 'deny':
            log.info("Action no soportada: %s", action)
            continue

        # Construye un objeto match para definir la regla
        match = of.ofp_match()
        # Forzamos IPv4 si hay campos IP/puerto
        match.dl_type = 0x0800

        if rule_protocol is not None:
            rp = rule_protocol.lower()
            if rp == 'tcp':
                match.nw_proto = 6
            elif rp == 'udp':
                match.nw_proto = 17
            elif rp == 'icmp':
                match.nw_proto = 1
            else:
                log.warning("Protocolo no soportado %s", rule_protocol)
                continue

        #agrego a la regla el puerto destino si esta definio
        if rule_dst_port is not None:
            try:
                match.tp_dst = int(rule_dst_port)
            except Exception:
                log.warning('dst_port invalido en regla: %s', rule)

        #agrego a la regla el puerto origen si esta definido
        if rule_src_port is not None:
            try:
                match.tp_src = int(rule_src_port)
            except Exception:
                log.warning('src_port invalido en regla: %s', rule)

        #agrego a la regla la ip origen si esta definida
        if rule_src_ip is not None:
            try:
                match.nw_src = IPAddr(rule_src_ip)
            except Exception:
                log.warning('src_ip invalida en regla: %s', rule)

        #agrego a la regla la ip destino si esta definida
        if rule_dst_ip is not None:
            try:
                match.nw_dst = IPAddr(rule_dst_ip)
            except Exception:
                log.warning('dst_ip invalida en regla: %s', rule)

        msg = of.ofp_flow_mod()
        msg.match = match
        # Prioridad razonable para reglas de firewall
        msg.priority = int(rule_priority)
        connection.send(msg)
        log.info('Instalada %s  en switch: %s', rule_msg, dpid_to_str(connection.dpid))


class Firewall(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        # Usar las reglas cargadas globalmente (core.firewall_rules) si existen
        self.rules = getattr(core, 'firewall_rules', [])



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

    # def _handle_PacketIn(self, event):
    #     packet = event.parsed
    #     in_port = event.port
    #     #Si el mensaje no es bloqueado por el firewall se envia a destino
    #     try:
    #         eth = packet
    #         ip = eth.payload if isinstance(eth.payload, ipv4) else None
    #         l4 = ip.payload if ip is not None else None
    #
    #         src_ip = str(getattr(ip, 'srcip', None)) if ip is not None else None
    #         dst_ip = str(getattr(ip, 'dstip', None)) if ip is not None else None
    #         src_port = getattr(l4, 'srcport', None) if l4 is not None else None
    #         dst_port = getattr(l4, 'dstport', None) if l4 is not None else None
    #
    #         if isinstance(l4, tcp):
    #             proto_name = 'TCP'
    #         elif isinstance(l4, udp):
    #             proto_name = 'UDP'
    #         elif isinstance(l4, icmp):
    #
    #             proto_name = type(l4).__name__ if l4 is not None else None
    #     except Exception:
    #         src_ip = dst_ip = src_port = dst_port = proto_name = None
    #
    #     log.debug("NO se bloquea el paquete en switch=%s src=%s:%s dst=%s:%s proto=%s",
    #              dpid_to_str(event.connection.dpid), src_ip, src_port, dst_ip, dst_port, proto_name)
    #
    #     # Reenviar el paquete sin instalar flows; usar OFPP_NORMAL para que el switch realice el forwarding unicast
    #     pkt_out = of.ofp_packet_out()
    #     buffer_id = getattr(event.ofp, 'buffer_id', None)
    #     if buffer_id is not None and buffer_id != -1:
    #         pkt_out.buffer_id = buffer_id
    #     else:
    #         pkt_out.data = event.ofp.data
    #
    #     pkt_out.in_port = in_port
    #     # Salida por OFPP_NORMAL permite al switch decidir el puerto de salida (procesamiento normal)
    #     pkt_out.actions.append(of.ofp_action_output(port=of.OFPP_NORMAL))
    #     self.connection.send(pkt_out)
    #     return

def launch(dpids=""):
    # dpids: lista separada por comas de los dpids donde se activa el firewall
    # si no se indica nada se activa el firewall en todos  los switchs
    if dpids:
        log.info(" Iniciando firewall custom en switchs con dpids = %s", dpids)
        allowed = set(int(d) for d in dpids.split(","))
    else:
        log.info(" Iniciando firewall custom en TODOS los switchs")
        allowed = None

    # Cargar reglas UNA VEZ y almacenarlas en core.firewall_rules
    core.firewall_rules = load_rules_from_file()

    def start_switch(event):
        dpid = event.connection.dpid
        if allowed is None or dpid in allowed:
            log.info("Firewall ACTIVADO en switch %s", dpid)
            Firewall(event.connection)
            # Instalar reglas proactivas en el switch en cuanto se conecte
            if hasattr(core, 'firewall_rules'):
                install_rules_on_connection(event.connection, core.firewall_rules)
        else:
            log.info("Firewall DESACTIVADO en switch %s", dpid)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
