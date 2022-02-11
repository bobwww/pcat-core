from multiprocessing import Process, Pipe

from sniffer.sniffer import sniff
from analyzer.analyzer import analyze
from enforcer.enforcer import enforce
from logger.logger import log


def main():
    '''
    Initilizes main processes: sniffer, analyzer, enforcer and logger.
    
    '''

    #   Pipe definitons
    #   x_src - pipe starts at x
    #   x_dst - end of pipe that started at x
    sniffer_src, sniffer_dst = Pipe()
    analyzer_src, analyzer_dst = Pipe()
    enforcer_src, enforcer_dst = Pipe()

    #   Process definitions
    sniffer_proc = Process(target=sniff, args=(sniffer_src,))
    analyzer_proc = Process(target=analyze, args=(sniffer_dst, analyzer_src))
    enforcer_proc = Process(target=enforce, args=(analyzer_dst, enforcer_src))
    logger_proc = Process(target=log, args=(enforcer_dst,))

    #   Start sniffer
    sniffer_proc.start()

    #   Start analyzer
    analyzer_proc.start()

    #   Start enforcer
    enforcer_proc.start()

    #   Start logger
    logger_proc.start()


if __name__ == '__main__':
    main()