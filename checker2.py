'''
Print tx_hash thats swapped and not ICCS
'''

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import os

# Create engines
engine_bridge = create_engine(os.getenv("DB_CONNECTION_STRING"))
engine_logger = create_engine(os.getenv("EVENT_LOGGER_DB_CONNECTION_STRING"))

# Reflect tables from each database
## ybridge_v3
base_ybridge = automap_base()
base_ybridge.prepare(engine_bridge, reflect=True)
tx_map = base_ybridge.classes.ybridge_request_tx_map  # table

## event_logger
base_logger = automap_base()
base_logger.prepare(engine_logger, reflect=True)
swap_requested = base_logger.classes.event_swap_requested  # table

# Queries
## Query ybridge_v3 for requested but not ICCS-ed tx
session_bridge = Session(engine_bridge)
query_bridge = session_bridge.query(tx_map.src_tx).filter(tx_map.process_status == 'REQUESTED') # (tx_map.process_status == 'REQUESTED')
results_bridge = query_bridge.all()
print(len(results_bridge))
session_bridge.close()

## Query event_logger for not designated dst daa
session_logger = Session(engine_logger)
query_logger = session_logger.query(swap_requested.tx_hash).filter(swap_requested.dst_aggregator_adaptor.is_(None))
results_logger = query_logger.all()
print(len(results_logger))
session_logger.close()

print([a for a in results_bridge for b in results_logger if a == b])
