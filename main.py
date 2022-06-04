# Import components
from analyzer.analyzer import Analyzer
from enforcer.enforcer import Enforcer
from logger.logger import Logger

#Import parser
from analyzer.parsercat import parse

#Import web app
from gui.app import app

from scapy.all import *
from utils import ConditionDrain

import yaml


    


def main():
    '''
    
    '''

    ROOTDIR = '.'  # Root directory
    DATADIR = ROOTDIR + '/data' # Data directory

    # Retrieve rule script from file and parse
    with open(DATADIR + '/script.lcat', 'r') as fd:
        script = fd.read()
    try:
        ruleset = parse(script)
    except SyntaxError as e: # Handle parser errors
                            # Add ability to show all errors before raising exception
        print(f'An error occurred during parsing: {str(e)}')
        print('Exiting...')
        exit()

    # Loading configuration
    cfg = {'send': False, 'log':True, 'alert':False}
    
    
    #mongo_uri = cfg...
    mongo_uri = 'mongodb://localhost:27017'

    # Main components: sniffer, analyezr, enforcer, and logger
    # Using scapy's PipeTools
    # Sniffer is a SniffSource object built in scapy
    sniffer = SniffSource()  # iface=conf.iface
    # check which iface to use

    # Analyzer gets the ruleset, then can be used to analyze packets
    # with its analyze func
    analyzer = Analyzer(ruleset)
    analyzer_drain = TransformDrain(analyzer.analyze)

    # Enforcer can receive arguments such as prefrences
    enforcer = Enforcer(cfg)
    enforcer_drain = TransformDrain(enforcer.enforce)
    #

    log_cond = ConditionDrain(lambda x: x['log'])  # lambda x:x.log
    send_cond = ConditionDrain(lambda x: x['send'])
    sender = InjectSink()  # iface=conf.iface
    logger = Logger(mongo_uri)
    logger_drain = TransformDrain(logger.log)


    sniffer > analyzer_drain > enforcer_drain
    enforcer_drain > log_cond > logger_drain
    #enforcer_drain > send_cond > sender

    x = PipeEngine(sniffer)
    #start pipe engine
    x.start()

    #start the gui
    # to add: dedicated thread for gui
    app.run()

    #monitoring of program...
    #
    #

    # stoping program (critical error or by admin command)
    x.stop()
    exit()


if __name__ == '__main__':
    main()
