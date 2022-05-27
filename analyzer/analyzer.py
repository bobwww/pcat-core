from analyzer.evaluate import Evaluator


class Results:

    def __init__(self, pkt, legal, trigger_chain=None) -> None:
        self.pkt = pkt
        self.legal = legal
        self.trigger_chain = trigger_chain


class Analyzer:

    def __init__(self, ruleset) -> None:
        self.ruleset = ruleset
        self.evaluator = Evaluator(ruleset)

    def analyze(self, pkt):

        res = self.evaluator.evaluate_packet(pkt)
        if res:
            return Results(pkt, legal=False, trigger_chain=res)
        else:
            return Results(pkt, legal=True)
