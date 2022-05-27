from pymongo import MongoClient
from datetime import datetime
import time
from scapy.all import raw


class Logger:

    def __init__(self, uri):
        self.client = MongoClient(uri)

    def log(self, verdict, timestamp: float=None):
        # Create the document to be stored
        docm = {
            'layers': [name for name in self.get_packet_layers(verdict.pkt)],
            'raw': raw(verdict.pkt),
            'timestamp': time if time else time.time(),
            'alert': verdict.alert,
            'sent': verdict.send
        }
        # Get the collection for the current time (by hour)
        # Uses GMT+0 time for consistency
        now = datetime.utcnow().strftime('%Y%m%d%H')
        coll = self.client[now]
        # Insert document
        coll.insert_one(docm)

    @staticmethod
    def get_packet_layers(packet):
        '''
        Given a packet, generates its layers' names.
        '''
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break

            yield layer
            counter += 1
