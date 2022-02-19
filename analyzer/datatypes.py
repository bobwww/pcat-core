from typing import Sequence


class Section:
    field: str
    expr: str

    def __init__(self, field, expr) -> None:
        self.field = field
        self.expr = expr

    def __str__(self) -> str:
        return "{field}: {expr};".format(field=self.field, expr=self.expr)


class Rule:
    sections: Sequence[Section]
    proto: str

    def __init__(self, sections, proto) -> None:
        self.sections = sections
        self.proto = proto

    def __str__(self) -> str:
        return "{proto} {{\n\t{sections}\n}}".format(proto=self.proto,
                                                    sections="\n\t".join([str(s) for s in self.sections]))


class Chain:
    rules: Sequence[Rule]
    action: str

    def __init__(self, rules, action) -> None:
        self.rules = rules
        self.action = action

    def __str__(self) -> str:
        return "{action} {{\n\t{rules}\n}}".format(
                                            action=self.action,
                                            rules="\n\t".join(['\t'.join(str(s).splitlines(True)) for s in self.rules])
                                                    ) # How does that work ??


class ExceptChain(Chain):
    pass


class Head:
    chains: Sequence[Chain]
    except_chains: Sequence[ExceptChain]

    def __init__(self, chains, except_chains) -> None:
        self.chains = chains
        self.except_chains = except_chains

    def __str__(self) -> str:
        return "{}".format("\n".join([str(s) for s in self.except_chains+self.chains]))