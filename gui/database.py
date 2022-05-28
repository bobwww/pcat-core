from pymongo import MongoClient
from datetime import datetime, timedelta

class TimeRange:

    # time should be at this format: YYYYMMDDhh[mm][ss][ms]
    def __init__(self, start: datetime, end:datetime=None, span:timedelta=None) -> None:
        self.start = start
        if end:
            self.end = end
        elif span:
            self.end = start + span
        else:
            self.end = start
    
    def evaluate(self, dt: datetime):
        return self.start <= dt <= self.end



class LogReader:

    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.coll = self.db.coll

    def get_by_timerange(self, start, end=None, span=None):
        timerange = TimeRange(start, end, span)
        return self.simple_query(timerange=timerange)

    def simple_query(self, timerange: TimeRange=None, flags: dict=None, protos: list=None, one_result=False):
        """
        time: YYYYMMDDhh[mm][ss][ms]
        time_span: amount of time to capture from time
        if end_time is give, timespan is ignored
        start_time <= time <= end_time
        generator func.
        flags ex. 
        {'alert': False, 'sent':True}
        """
        qry = {}

        if timerange:
            qry['time'] = {
                        '$gte': timerange.start,
                        '$lte': timerange.end
                         }
        if flags:
            new_flags = {}
            for key in flags:
                new_flags[f'flags.{key}'] = flags[key]
            qry.update(new_flags)
        
        if protos:
            qry['layers'] = { '$all': protos}

        if one_result:
            return self.coll.find_one(qry)
        else:
            return self.coll.find(qry)

    def advanced_query(self):
        '''
        can query using packet's contents. uses scapy for analyzing.
        '''
        pass

    @staticmethod
    def get_timestamp(year, month, day, hour, minute, second, microsecond):
        return datetime(year, month, day, hour, minute, second, microsecond).strftime('%Y%m%d%H%M%S%f')

    @staticmethod
    def get_datetime_from_timestamp(timestamp):
        return datetime.strptime(timestamp, '%Y%m%d%H%M%S%f')



