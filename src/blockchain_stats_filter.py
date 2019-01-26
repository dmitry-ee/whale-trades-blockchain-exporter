import json
from datetime import datetime

import importdir
importdir.do("lib", globals())

class BlockchainStatsFilter(callback.Callback):
    def __init__(self, object_type="utx"):
        super().__init__("BlockchainStatsFilter")
        self.object_type = object_type

    def processCallback(self, stat):
        stat["pools"] = [{ "name": k, "value": v } for k,v in stat.items()]
        stat["type"] = self.object_type
        stat["time"] = stat["timestamp"]
        stat["timestamp"] = datetime.utcfromtimestamp(stat["timestamp"]/1000).isoformat()
        return stat
