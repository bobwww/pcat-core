# default = {
#     'alert': False,
#     'log': True,
#     'send': True
# }

class Verdict:
    guide = {
        # action: (send_pkt, log_pkt)
        'allow': {'send': True, 'log': True},
        'sallow': {'send': True, 'log': False},
        'deny': {'send': False, 'log': True},
        'sdeny': {'send': False, 'log': False}
    }

    def __init__(self, pkt, alert=False, log=False, send=False) -> None:
        self.pkt = pkt
        self.alert = alert
        self.log = log
        self.send = send

    @classmethod
    def evaluate_verdict(cls, analysis, default):
        if analysis.legal:
            return cls(
                analysis.pkt, alert=default['alert'], log=default['log'], send=default['send']
            )
        else:
            return cls(
                analysis.pkt,
                alert=analysis.trigger_chain.alert,
                log=cls.guide[analysis.trigger_chain.action]['log'],
                send=cls.guide[analysis.trigger_chain.action]['send']
            )


class Enforcer:

    def __init__(self, conf):
        self.conf = conf

    def enforce(self, results):
        return Verdict.evaluate_verdict(results, self.conf)
