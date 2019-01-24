import json
from datetime import datetime

import importdir
importdir.do("lib", globals())

class BlockchainTxFilter(callback.Callback):
    def __init__(self, min_input_btc=0, min_input_total_btc=0, min_output_btc=0, min_output_total_btc=0, object_type="utx"):
        super().__init__("BlockchainTxFilter")
        self.min_input_btc = float(min_input_btc)
        self.min_input_total_btc = float(min_input_total_btc)
        self.min_output_btc = float(min_output_btc)
        self.min_output_total_btc = float(min_output_total_btc)

        self.object_type = object_type

        self.copy_from_tx = [
            "lock_time", "ver", "size", "tx_index", "vin_sz", "vout_sz", "hash", "relayed_by"
        ]

    def processCallback(self, obj):
        converted_tx = None

        if type(obj) is str: obj = json.loads(obj)

        if type(obj) is not dict:
            self.logger.warning("got wrong object type = %s! <- %s" % (type(obj), obj) )
        if obj["op"] != "utx":
            self.logger.warning("got wrong op type = %s! <- %s" % (obj["op"], obj) )

        return self.convert_tx(obj["x"])

        # if converted_tx != None:
        #     return converted_tx

    def convert_tx(self, tx):
        converted_tx = {}
        converted_tx["timestamp"] = datetime.utcfromtimestamp(tx["time"]).isoformat()
        converted_tx["type"] = self.object_type

        tx_output_values = [ o["value"] / 100000000.0 for o in tx["out"] ]
        converted_tx["total_output_btc"] = sum(tx_output_values)
        converted_tx["min_output_btc"]   = min(tx_output_values)
        converted_tx["max_output_btc"]   = max(tx_output_values)
        if converted_tx["max_output_btc"] < self.min_output_btc or converted_tx["total_output_btc"] < self.min_output_total_btc:
            return

        tx_input_values = [ i["prev_out"]["value"] / 100000000.0 for i in tx["inputs"] ]
        converted_tx["total_input_btc"] = sum(tx_input_values)
        converted_tx["min_input_btc"]   = min(tx_input_values)
        converted_tx["max_input_btc"]   = max(tx_input_values)
        if converted_tx["max_input_btc"] < self.min_input_btc or converted_tx["total_input_btc"] < self.min_input_total_btc:
            return

        for k in self.copy_from_tx:
            converted_tx[k] = tx[k]

        #converted_tx["in"]  = { seq["prev_out"]["addr"] : seq["prev_out"]["value"] for seq in tx["inputs"] }
        converted_tx["in"] = [ { "addr": seq["prev_out"]["addr"], "value": seq["prev_out"]["value"] } for seq in tx["inputs"] ]
        #converted_tx["out"] = { seq["addr"] : seq["value"] for seq in tx["out"] }
        converted_tx["out"] = [ { "addr": seq["addr"], "value": seq["value"] } for seq in tx["out"] ]

        converted_tx["fee_sat"] = int((converted_tx["total_input_btc"] - converted_tx["total_output_btc"]) * 100000000)
        converted_tx["fee_byte_sat"] = int(converted_tx["fee_sat"] / converted_tx["size"])
        return converted_tx
