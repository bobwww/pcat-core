# default = {
#     'alert': False,
#     'log': True,
#     'send': True
# }

class Verdict:
    GUIDE = {
        'allow' : {'send': True, 'log': True},
        'sallow': {'send': True, 'log': False},
        'deny'  : {'send': False, 'log': True},
        'sdeny' : {'send': False, 'log': False}
    }

    def __init__(self, pkt, alert=False, log=False, send=False) -> None:
        self.pkt = pkt
        self.alert = alert
        self.log = log
        self.send = send

    @classmethod
    def evaluate_verdict(cls, analysis, conf):
        if analysis.legal:
            return cls(
                analysis.pkt, alert=conf['default']['alert'], log=conf['default']['log'], send=conf['default']['send']
            )
        else:
            return cls(
                analysis.pkt,
                alert=analysis.trigger_chain.alert,
                log=cls.GUIDE[analysis.trigger_chain.action]['log'],
                send=cls.GUIDE[analysis.trigger_chain.action]['send']
            )


class Enforcer:

    def __init__(self, conf):
        self.conf = conf

    def enforce(self, results):
        return Verdict.evaluate_verdict(results, self.conf)
