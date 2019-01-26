import logging, importdir, asyncio
from blockchain import statistics
importdir.do("lib", globals())

from blockchain_tx_filter import BlockchainTxFilter
from blockchain_etv_filter import BlockchainETVFilter
from blockchain_stats_filter import BlockchainStatsFilter
from blockchain_pools_filter import BlockchainPoolsFilter

logger = logging.getLogger()

async def run(config):

    # kafka initializer
    # kafka_type_mapping = {
    #     config.wtbe.message.utx.type: config.wtbe.message.utx.topic,
    #     config.wtbe.message.blockchain.type: config.wtbe.message.blockchain.topic,
    #     config.wtbe.message.pools.type: config.wtbe.message.pools.topic,
    # }
    # kafka = kafka_callback.KafkaCallback(config.wtbe.kafka.url, type_topic_mapping=kafka_type_mapping)
    #
    # # blockchain listener initializer
    # ws = ws_listener.WSListener("wss://ws.blockchain.info/inv",
    #     command_list=['{ "op": "unconfirmed_sub" }'],
    #     sleep_ms=config.wtbe.websocket.sleep.ms
    # )
    # tx_filter = BlockchainTxFilter(
    #     min_output_btc=config.wtbe.min.output.btc,
    #     object_type=config.wtbe.message.utx.type
    # )
    # etv_filter = BlockchainETVFilter()

    # for debug purposes
    pp = print_callback.PrintCallback()

    #ws.addCallback(tx_filter)
    #tx_filter.addCallback(etv_filter)
    #etv_filter.addCallback(pp)

    # blockchain stats initializer
    rep = basic_call_repeater.BasicCallRepeater(
        repeat_lambda=lambda self: statistics.get().__dict__,
        sleep_ms=config.wtbe.repeater.sleep.ms
    )
    stats_filter = BlockchainStatsFilter(config.wtbe.message.blockchain.type)

    # pools scruber initializer
    pools = basic_call_repeater.BasicCallRepeater(
        repeat_lambda=lambda self: statistics.get_pools(),
        sleep_ms=config.wtbe.pools.sleep.ms
    )
    pools_filter = BlockchainPoolsFilter(config.wtbe.message.pools.type)

    # if str(config.wtbe.etv.enabled).lower() == "false":
    #     logger.warning("TURNING OFF ETV_FILTER")
    #     ws_filters = tx_filter.addCallback(kafka)
    # else:
    #     logger.warning("ETV_FILTER IS ON! IT MAY IMPACT CPU")
    #     ws_filters = tx_filter.addCallback(etv_filter.addCallback(kafka))
    # #ws_filters = tx_filter.addCallback(kafka) if config.wtbe.etv.enabled == "false" else tx_filter.addCallback(etv_filter.addCallback(kafka))
    #
    # ws.addCallback(ws_filters)
    # rep.addCallback(stats_filter.addCallback(kafka))
    pools.addCallback(pools_filter.addCallback(pp))

    tasks = [pools.run()]
    await asyncio.wait(tasks)
