from typing import NewType, Any
from datatypes import Head, Chain, Rule, Section

ScapyLikePacketObject = NewType('ScapyLikePacketObject', Any)


def evaluate_head(pkt: ScapyLikePacketObject, head: Head):
    pass


def evaluate_chain(pkt: ScapyLikePacketObject, chain: Chain) -> bool:
    pass


def evaluate_rule(pkt: ScapyLikePacketObject, rule: Rule) -> bool:
    pass


def evaluate_section(pkt: ScapyLikePacketObject, section: Section) -> bool:
    pass