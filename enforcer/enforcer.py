# default = {
#     'alert': False,
#     'log': True,
#     'send': True
# }

# class Verdict:
#     GUIDE = {
#         'allow' : {'send': True, 'log': True},
#         'sallow': {'send': True, 'log': False},
#         'deny'  : {'send': False, 'log': True},
#         'sdeny' : {'send': False, 'log': False}
#     }

#     def __init__(self, pkt, alert=False, log=False, send=False, evoked=False) -> None:
#         self.pkt = pkt
#         self.alert = alert
#         self.log = log
#         self.send = send
#         self.evoked = evoked

#     @classmethod
#     def evaluate_verdict(cls, analysis, conf):
#         if analysis['legal']:
#             return cls(
#                 analysis.pkt, alert=conf['default']['alert'], log=conf['default']['log'], send=conf['default']['send'],
#                 evoked=False
#             )
#         else:
#             return cls(
#                 analysis.pkt,
#                 alert=analysis.trigger_chain.alert,
#                 log=cls.GUIDE[analysis.trigger_chain.action]['log'],
#                 send=cls.GUIDE[analysis.trigger_chain.action]['send'],
#                 evoked=True
#             )

from datetime import datetime

class Enforcer:

    GUIDE = {
        'allow' : {'send': True, 'log': True},
        'sallow': {'send': True, 'log': False},
        'deny'  : {'send': False, 'log': True},
        'sdeny' : {'send': False, 'log': False}
    }

    def __init__(self, conf):
        self.conf = conf

    def enforce(self, results):

        if results['legal']:
            send = self.conf['send']
            alert = self.conf['alert']
            log = self.conf['log']
        else:
            send = self.GUIDE[results['action']]['send']
            log = self.GUIDE[results['action']]['log']
            alert = results['alert']

        #results.pop('action') ##Optional
        results.update(
            {
                'time': datetime.utcnow(),
                'send': send,
                'log': log,
                'alert': alert   
            } 
        )

        return results
