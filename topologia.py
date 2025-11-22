import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

NUM_HOST_SIDE = 4

from mininet.topo import Topo

NUM_HOST_SIDE = 4

class MyTopo(Topo):
    def __init__(self, switch_count):
        super().__init__()

        # Create hosts
        for i in range(1, NUM_HOST_SIDE + 1):
            if i == 1:
                self.addHost(f'h{i}', ip='10.0.0.1/24')
            else:
                self.addHost(f'h{i}')

        prev_switch = None

        # Create the chain of switches
        for i in range(1, switch_count + 1):
            sw = self.addSwitch(f's{i}')

            if prev_switch is not None:
                self.addLink(prev_switch, sw)

            prev_switch = sw

        # Link hosts to first and last switch
        last_switch = switch_count

        self.addLink("h1", "s1")
        self.addLink("h2", "s1")
        self.addLink("h3", f"s{last_switch}")
        self.addLink("h4", f"s{last_switch}")


# IMPORTANT: Mininet only reads parameters through this dict.
topos = {
    'customTopo': lambda switches=2: MyTopo(switches)
}


def main():
    parser = argparse.ArgumentParser(description="Topología lineal de switches")
    parser.add_argument("-s", "--switches", type=int, required=True,
                        help="Cantidad de switches a crear en línea")

    args = parser.parse_args()

    print(f"Creando topología con {args.switches} switches encadenados...")

    topo = MyTopo(args.switches)
    print("Topología creada correctamente.")

    # Si querés ejecutarla desde Python:
    # net = Mininet(topo=topo)
    # net.start()
    # CLI(net)
    # net.stop()


if __name__ == "__main__":
    main()
