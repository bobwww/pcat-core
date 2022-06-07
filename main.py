# Import components
from analyzer.analyzer import Analyzer
from enforcer.enforcer import Enforcer
from logger.logger import Logger

# Import parser
from analyzer.parsercat import parse

# Import GUI (Web application)
from gui import app

# Import Scapy for Pipetools
from scapy.all import SniffSource, TransformDrain, InjectSink, PipeEngine
from utils import ConditionDrain, ask_confirm

# Import config manager
import config

from threading import Thread,Condition, Event


def safe_exit() -> None:
    """Exits safely from program, with a nice message.
    """
    print('Exiting...')
    exit()


def main():

    # Paths setup
    ROOTDIR = '.'  # Root directory
    DATADIR = ROOTDIR + '/data' # Data directory
    CFG_PATH = DATADIR + '/config.json'


    # Loading configuration
    try:
        cfg = config.load_config(CFG_PATH)
        if config.validate_config(cfg):
            print('Config loaded successfully.')
        else:
            raise 
        #Config error
    except Exception as e:
        if ask_confirm(
'''It seems your config file is corrupted.
Do you wish to reset it to default?'''):
            config.reset_config(CFG_PATH)
            print('Config reset to default.')
        safe_exit()
    

    # Ruleset retrieval and parsing
    RULESET_PATH = cfg['analyzer']['rulesetPath']
    with open(RULESET_PATH, 'r') as fd:
        ruleset = fd.read()
    try:
        ruleset = parse(ruleset)
    #Parse error
    except SyntaxError as e: # Handle parser errors
                            # Add ability to show all errors before raising exception
        print(f'An error occurred during parsing: {str(e)}')
        safe_exit()
    
    # Parameters set up

    #Sniffer
    SNIFF_IFACE = cfg['sniffer']['iface']
    if not SNIFF_IFACE: SNIFF_IFACE = None

    #Sender
    SEND_IFACE = cfg['sender']['iface']
    if not SEND_IFACE: SEND_IFACE = None

    #Enforcer
    DEFAULT_GUIDE = cfg['enforcer']['default']

    #Logger
    MONGO_URI = cfg['logger']['uri']

    # Main components: sniffer, analyezr, enforcer, and logger
    # Using scapy's PipeTools
    # Sniffer is a SniffSource object built in scapy
    sniffer = SniffSource(iface=SNIFF_IFACE)  # iface=conf.iface
    # check which iface to use

    # Analyzer gets the ruleset, then can be used to analyze packets
    # with its analyze func
    analyzer = Analyzer(ruleset)
    analyzer_drain = TransformDrain(analyzer.analyze)

    # Enforcer can receive arguments such as prefrences
    enforcer = Enforcer(DEFAULT_GUIDE)
    enforcer_drain = TransformDrain(enforcer.enforce)
    #

    log_cond = ConditionDrain(lambda x: x['log'])  # lambda x:x.log
    send_cond = ConditionDrain(lambda x: x['send'])
    sender = InjectSink(iface=SEND_IFACE)  # iface=conf.iface

    #Logger
    logger = Logger(MONGO_URI)
    logger_drain = TransformDrain(logger.log)


    sniffer > analyzer_drain > enforcer_drain
    enforcer_drain > log_cond > logger_drain
    #enforcer_drain > send_cond > sender

    t1 = PipeEngine(sniffer)
    #start pipe engine, starting another thread


    #start the gui
    # to add: dedicated thread for gui
    # try:
    #     app.run()
    # except KeyboardInterrupt:
    #     pass



    # t1.start()


    #monitoring of program...
    #
    #
    ev_exit = Event()
    # t2 = Thread(target=wait_for_shutdown, args=(ev_exit,))
    # t2.start()
    # flask must run on main thread

    app.main(ev_exit)
    

    # stoping program (critical error or by admin command)
    # t1.stop()
    # t2.stop() threading doesnt have this option
    safe_exit()



def wait_for_shutdown(ev):
    ev.wait()
    print('Received signal tos shutdown')
    safe_exit()




if __name__ == '__main__':
    main()
