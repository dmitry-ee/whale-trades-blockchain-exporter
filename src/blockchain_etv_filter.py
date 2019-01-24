import json
from datetime import datetime
from blockchain import blockexplorer

import importdir
importdir.do("lib", globals())

class BlockchainETVFilter(callback.Callback):
    def __init__(self):
        super().__init__("BlockchainETVFilter")
        #self.bitcoin_api = cryptos.Bitcoin()

    def processCallback(self, tx):
        self._mark_output_as_input(tx)
        self._mark_blank_out_by_history(tx)
        return tx

    def _mark_output_as_input(self, tx):
        # not necessary if there's exactly one out
        if len(tx["out"]) == 1:
            return

        for o in tx["out"]:
            if o["addr"] in [ o["addr"] for o in tx["in"] ]:
                #tx["out"][o_addr]["is_input"] = True
                o["is_input"] = True

    def _mark_blank_out_by_history(self, tx):
        for o in tx["out"]:
            if not o.get("is_input", False):
                # get history for output address
                try:
                    #api_history = self.bitcoin_api.history(o["addr"])
                    account_info = blockexplorer.get_address(o["addr"])
                    #print(account_info.transactions)
                    # if it's an new address (with one record in history) we assume that's a "change" address
                    #if api_history["n_tx"] == 1: o["new_addr"] = True
                    if len(account_info.transactions) == 0: o["new_addr"] = True
                except Exception as e:
                    self.logger.info("error during perform blockchain HISTORY request for address = %s" % o["addr"])
                    o["invalid_addr"] = True
