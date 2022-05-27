import json
import datetime as dt
from scapy.all import hexdump

def verdict_to_json(verdict):
    return json.dumps({
        'time': dt.datetime.strftime('%Y-%m-%d::%H:%M:%S'),
        'payload': hexdump(verdict.pkt),
        'alert': verdict.alert,
        'sent': verdict.send
    })


class Logger:

    def __init__(self, path):
        self.fd = open(path, 'a')

    def log(self, verdict):
        self.fd.write(verdict_to_json(verdict) + '\n')

    def __del__(self):
        self.fd.close()
