import asyncio

import numpy as np
import pandas as pd
from pyzeebe import ZeebeWorker, create_camunda_cloud_channel, create_insecure_channel
import pickle


####################################################
#      SETUP TO USE C8 ZEEBE
####################################################
# Create channel to Zeebe
#channel = create_camunda_cloud_channel(
#    client_id="u_eR8WbpVLktYegPjKTy_LwrwtKycxQD",
#    client_secret="gTvDm-l92oXaTbdcS.6IeypQxDQ8~hKhaUVV0C4Rq4MaSfMj4huEMiipAFxwdA2M",
#    cluster_id="b6f56d09-397c-4d96-838a-96df7f1665e4",
#)

channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

# Create single threaded worker
worker = ZeebeWorker(channel)

####################################################
#          DEFINE WORKERS
####################################################
# Define work this client should do when trade_match_worker job exists in Zeebe
@worker.task(task_type="trade_match_worker")
async def trade_match_work(trans_ref,
                           account,
                           security_id,
                           price,
                           price_currency,
                           sanctioned_security,
                           quantity,
                           trans_type,
                           amount,
                           amount_currency,
                           amount_USD,
                           market,
                           counter_party,
                           participant,
                           settle_date,
                           actual_settle_date,
                           source_system,
                           trade_status,
                           user_id,
                           ledger,
                           _merge
                           ):

    print(f"merge_results for {trans_ref} from {ledger} = {_merge}")

    if _merge == "both":
        return {"match_result": "matched"}
    else:
        return {"match_result":  "unmatched"}


# Main loop
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(worker.work())
finally:
    loop.stop()
    loop.close()