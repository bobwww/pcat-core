from multiprocessing import Process, Pipe

from sniffer import sniff
from analyzer import analyze
from enforcer import enforce
from logger import log


def main():
    #Pipe definitons
    sniff_pipe, analyzer_recv_pipe = Pipe()
    analyzer_send_pipe, enforcer_recv_pipe = Pipe()
    enforcer_send_pipe, logger_recv_pipe = Pipe()

    #Process definitions
    sniffer_proc = Process(target=sniff, args=(sniff_pipe,))
    analyzer_proc = Process(target=analyze, args=(analyzer_recv_pipe, analyzer_send_pipe))
    enforcer_proc = Process(target=enforce, args=(enforcer_recv_pipe, enforcer_send_pipe))
    logger_proc = Process(target=log, args=(logger_recv_pipe,))

    #start sniffer
    sniffer_proc.start()

    #start analyzer
    analyzer_proc.start()

    #start enforcer
    enforcer_proc.start()

    #start logger
    logger_proc.start()


if __name__ == '__main__':
    main()