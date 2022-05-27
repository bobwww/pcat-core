# Import components
from analyzer.analyzer import Analyzer
from enforcer.enforcer import Enforcer
from logger.logger import Logger

from analyzer.parsercat import parse

from gui.app import app

from scapy.all import *
from utils import ConditionDrain


def main():
    '''
    Initilizes main processes: sniffer, analyzer, enforcer and logger.
    
    '''

    # Retrieve ruleset from file
    with open('script.lcat', 'r') as fd:
        x = fd.read()
    try:
        ruleset = parse(x)
    except SyntaxError as e:
        print(f'An error occurred during parsing: {str(e)}')
        exit()
    # Main components: sniffer, analyezr, enforcer, and logger
    # Using scapy's PipeTools
    # Sniffer is a SniffSource object built in scapy
    sniffer = SniffSource()  # iface=conf.iface
    # Analyzer gets the ruleset, then can be used to analyze packets
    # with its analyze func
    analyzer = Analyzer(ruleset)
    analyzer_drain = TransformDrain(analyzer.analyze)
    # Enforcer can receive arguments such as prefrences
    enforcer = Enforcer()
    enforcer_drain = TransformDrain(enforcer.enforce)
    #
    log_cond = ConditionDrain(lambda x: x.log)  # lambda x:x.log
    send_cond = ConditionDrain(lambda x: x.send)
    sender = InjectSink()  # iface=conf.iface
    logger = Logger()
    logger_drain = TransformDrain(logger.log)
    sender = InjectSink()


    sniffer > analyzer_drain > enforcer_drain
    enforcer_drain > log_cond > logger_drain
    enforcer > send_cond > sender

    x = PipeEngine(sniffer)
    x.start()
    app.run()
    x.stop()
    exit()


if __name__ == '__main__':
    main()
