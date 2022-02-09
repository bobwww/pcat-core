
class Ruleset:
    
    def __init__(self, chains=None) -> None:

        if not chains:      chains = ()

        self.chains = chains

class Chain:
    
    def __init__(self, rules=None, has=None, default_protocol=None, protocol=None) -> None:
        
        if not rules:               rules = ()
        if not has:                 has = ()
        if not default_protocol:    default_protocol = ''
        if not protocol:            protocol = ''

        self.rules = rules
        self.has = has
        self.default_proto = default_protocol
        self.proto = protocol

    # @staticmethod
    # def evaluate(func):
        
    #     def inside(chains):
    #         return any(func())

    #     return inside

class Rule:
    
    def __init__(self, field=None, values=None, protocol=None) -> None:

        if not field:       field = ''
        if not values:      values = ''
        if not protocol:    protocol = ''

        self.proto = protocol
        self.field = field
        self.value = values
        