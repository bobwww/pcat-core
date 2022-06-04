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
        if not sections:
            sections = []
        self.sections = sections
        self.proto = proto

    def __str__(self) -> str:
        return "{proto} {{\n\t{sections}\n}}".format(proto=self.proto,
                                                    sections="\n\t".join([str(s) for s in self.sections]))


class Chain:
    rules: Sequence[Rule]
    action: str

    def __init__(self, rules, action, alert=False) -> None:
        if not rules:
            rules = []
        self.rules = rules
        self.action = action
        self.alert = alert
        self.name = 'PlaceholderName'

    def __str__(self) -> str:
        return "{alert}{action} {{\n\t{rules}\n}}".format(
                                            action=self.action,
                                            rules="\n\t".join(['\t'.join(str(s).splitlines(True)) for s in self.rules]),
                                            alert=("alert " if self.alert else "")
                                                ) # How does that work ??


class Head:
    chains: Sequence[Chain]

    def __init__(self, chains) -> None:
        if not chains:
            chains = []
        self.chains = chains

    def __str__(self) -> str:
        return "{}".format("\n".join([str(s) for s in self.chains]))