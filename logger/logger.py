from pymongo import MongoClient
from datetime import datetime
from scapy.all import raw
from utils import get_packet_layers

    
class Logger:

    def __init__(self, uri: str) -> None:
        # Establishes connection to database
        self.client = MongoClient(uri)
        self.coll = self.db.coll

    def log(self, verdict, utctime: datetime=None) -> None:
        """
        Logs the packet and its metadata.
        """
        self.coll.insert_one(
                {
                'raw': raw(verdict.pkt),
                'layers': [name for name in get_packet_layers(verdict.pkt)],
                'time': utctime if utctime else datetime.utcnow(),
                'flags': {'alert': verdict.alert, 'sent': verdict.send}
                }
        )
