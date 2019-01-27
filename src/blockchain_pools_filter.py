import json
from datetime import datetime

import importdir
importdir.do("lib", globals())

class BlockchainPoolsFilter(callback.Callback):
    def __init__(self, object_type="pools"):
        super().__init__("BlockchainPoolsFilter")
        self.object_type = object_type

    def processCallback(self, pools_info):
        stat = [
            {
                "pool_name": k,
                "pool_value": v,
                "type": self.object_type,
                "timestamp": datetime.utcnow().isoformat()
            } for k,v in pools_info.items()
        ]
        return stat
