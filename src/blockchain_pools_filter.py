import json
from datetime import datetime

import importdir
importdir.do("lib", globals())

class BlockchainPoolsFilter(callback.Callback):
    def __init__(self, object_type="pools"):
        super().__init__("BlockchainPoolsFilter")
        self.object_type = object_type

    def processCallback(self, pools_info):
        stat = {}
        stat["pools"] = [{ "name": k, "value": v } for k,v in pools_info.items()]
        stat["type"] = self.object_type
        stat["timestamp"] = datetime.utcnow().isoformat()
        return stat
