import xml.etree.ElementTree as ET

from rules import Ruleset, Chain, Rule

def main(path):
    tree = ET.parse(path)
    root = tree.getroot()
    
    chains = []
    for chain in root:
        rules = []
        for rule in chain:
            rules.append(
                Rule(field=rule.get('field'), values=rule.text, protocol=rule.get('protocol'))
            )
        chains.append(
            Chain(rules=rules, has=chain.get('has'), default_protocol=chain.get('default_protocol'),
            protocol=chain.get('protocol'))
        )

    return Ruleset(chains=chains)

