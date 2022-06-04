from scapy.all import Drain


class ConditionDrain(Drain):

    def __init__(self, f, name=None):
        Drain.__init__(self, name=name)
        self.f = f

    def push(self, msg):
        if self.f(msg):
            self._send(msg)

    def high_push(self, msg):
        if self.f(msg):
            self._high_send(msg)

def get_packet_layers(packet):
    '''
    Given a packet, generates its layers' names.
    '''
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer.name
        counter += 1


