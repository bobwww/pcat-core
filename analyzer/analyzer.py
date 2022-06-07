from analyzer.evaluate import Evaluator
from scapy.all import raw
from typing import Any, Dict, List


class Analyzer:

    def __init__(self, ruleset: str) -> None:
        """Initiates an Analyzer instance.

        Args:
            ruleset (str): string representation of an LCAT file
        """
        # self.ruleset = ruleset
        self.evaluator = Evaluator(ruleset)

    def analyze(self, pkt) -> Dict[str, Any]:
        """Analyzes a given packet and returns the results.

        Args:
            pkt (ScapyPacket): The packet to be analyzed

        Returns:
            Dict[str, Any]: a dcitionary containing the following key-value pairs;
                'packet': (bytes) Raw packet in bytes
                'layers': (List[str]) Sequence of the packet layers' names,
                'src', 'dst': dict of the following structure;
                    {'addr': (str) src/dst address,
                    'port': (int) src/dst port}
                'legal' - (bool) Whether the packet has broken a chain or not,
                
                *If packet is illegal, in addition:
                'chain': (str) The name of the chain that was broken,
                'action': (str) The action that is defined by the chain,
                'alert': (bool) Whether to alert or not.

        """
        triggering_chain = self.evaluator.evaluate_packet(pkt)
        # triggering_chain -> name of the triggered/broken chain. 
        # In case no chain is triggered, returns None
        results = {
                'packet': raw(pkt), # Could be optional
                'layers': get_packet_layers(pkt),
                'src': get_packet_src(pkt),
                'dst': get_packet_dst(pkt),
            }

        if triggering_chain:
            results.update({
                'legal': False,
                'chain': triggering_chain.name,
                'action':triggering_chain.action,
                'alert': triggering_chain.alert
            })
        else:
            results.update({
                'legal': True,
            })

        return results


def get_packet_layers(packet) -> List[str]:
    """Returns a sequence of strings representing the layers in the packet,
    starting from the lowest layer.

    Args:
        packet (ScapyPacket): A Scapy packet.

    Returns:
        List[str]: Names of the layers in the given packet.
    """

    def recursive_inside():
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break

            yield layer.name
            counter += 1
    
    return [name for name in recursive_inside()]

def get_packet_src(pkt):
    """Given a packet, returns its source IP address and port (if applicable).

    Args:
        pkt (ScapyPacket): A Scapy packet

    Returns:
        Dict[str, Any[int, str]]: A dictionary of the following shape:
        {'addr': (str) address,
        'port': (int) port}
    """

    src = {} 

    if pkt.haslayer('IP'):
        src['addr'] = pkt.getlayer('IP').src
        
        if pkt.haslayer('TCP'):
            src['port'] = pkt.getlayer('TCP').sport

        elif pkt.haslayer('UDP'):
            src['port'] = pkt.getlayer('UDP').sport

    return src

def get_packet_dst(pkt):
    """Given a packet, returns its destination IP address and port (if applicable).

    Args:
        pkt (ScapyPacket): A Scapy packet

    Returns:
        Dict[str, Any[int, str]]: A dictionary of the following shape:
        {'addr': (str) address,
        'port': (int) port}
    """

    dst = {} 

    if pkt.haslayer('IP'):
        dst['addr'] = pkt.getlayer('IP').dst
        
        if pkt.haslayer('TCP'):
            dst['port'] = pkt.getlayer('TCP').dport

        elif pkt.haslayer('UDP'):
            dst['port'] = pkt.getlayer('UDP').dport

    return dst