import re

class Ruleset:
    
    def __init__(self, chains=None) -> None:

        if not chains:      chains = ()

        self.chains = chains

    def validate(self, validator):
        return any([chain.validate(validator) for chain in self.chains])

class Chain:
    
    def __init__(self, rules, has, default_protocol, protocol) -> None:

        self.rules = rules
        self.has = has
        self.default_proto = default_protocol
        self.proto = protocol

    # @staticmethod
    # def evaluate(func):
        
    #     def inside(chains):
    #         return any(func())

    #     return inside

    @classmethod
    def create(cls, rules=None, has=None, default_protocol=None, protocol=None):

        if not rules: rules = ()
        else:
            if not all(map(lambda x:type(x) is Rule, rules)): raise Exception

        allowed_chars = re.compile('[A-Za-z_0-9@;]*')
        if not has:
            has = ()
        else:
            if not re.matchall(allowed_chars, has): raise Exception

        allowed_chars = re.compile('[A-Za-z_]*')

        if not default_protocol:
            default_protocol = ''
        else:
            if not re.matchall(allowed_chars, default_protocol): raise Exception

        if not protocol:
            protocol = ''
        else:
            if not re.matchall(allowed_chars, protocol): raise Exception

        return cls(rules, has, default_protocol, protocol)

    def validate(self, rule_validator_func):
        return all(map(rule_validator_func, self.rules))

class Rule:
    
    def __init__(self, protocol, field, values) -> None:

        self.proto = protocol
        self.field = field
        self.value = values
    
    @classmethod
    def create(cls, protocol=None, field=None, values=None):

        allowed_chars = re.compile('[A-Za-z_]*')

        if not protocol:
            protocol = ''
        else:
            if not re.matchall(allowed_chars, protocol): raise Exception

        if not field:
            field = ''
        else:
            if not re.matchall(allowed_chars, field): raise Exception

        allowed_chars = re.compile('[A-Za-z_0-9.-;]*')
        if not values:
            values = ()
        else:
            if not re.matchall(allowed_chars, values): raise Exception
            values = tuple(values.split(';'))


        return cls(protocol, field, values)


