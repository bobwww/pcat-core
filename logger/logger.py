from pymongo import MongoClient

    
class Logger:

    def __init__(self, uri: str) -> None:
        # Establishes connection to database
        self.client = MongoClient(uri)
        self.coll = self.client.pcat.data

    def log(self, results) -> None:
        """
        Logs the packet and its metadata.
        """

        self.coll.insert_one(results)
