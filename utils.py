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


def ask_confirm(msg: str) -> bool:
    """Asks user a yes/no questions, and returns answer as a bool.

    Args:
        msg (str): the question to be displayed

    Returns:
        bool: True if answered yes, False otherwise
    """
    ans = input(msg + '(y/n)')
    if ans in ['Y', 'y', 'yes']:
        return True
    else:
        return False