class Evaluator:

    def __init__(self, head) -> None:
        self.head = head  # Ruleset as a head object

    def evaluate_packet(self, pkt):
        """
        If packet is validated, returns None.
        If packet is caught in a chain, returns the chain action.
        The chains are checked in the same order they are written.
        """

        for chain in self.head.chains:
            if not self.__evaluate_chain(pkt, chain):
                return chain
        return None

    @classmethod
    def __evaluate_chain(cls, pkt, chain):
        # Returns true if chain upholds
        for rule in chain.rules:
            # To fix: make sure all protos are saved as capital letters
            if rule.proto not in pkt:
                continue  # If protocol is not present in packet,
                # we consider the rule irrelevent to that packet.

            elif not cls.__evaluate_rule(pkt, rule):
                # If a single rule is broken in a chain, the whole chain
                # is borken
                return False
        return True

    @classmethod
    def __evaluate_rule(cls, pkt, rule):
        # Returns true if rule upholds
        for section in rule.sections:
            if not section.expr.eval(getattr(pkt, section.field)):
                # If one of the sections' condition is not met, 
                # the entire rule is considered broken (false)
                return False
        return True
