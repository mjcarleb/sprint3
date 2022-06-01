import pandas as pd
import dask.dataframe as dd
import asyncio
from pyzeebe import ZeebeClient, create_camunda_cloud_channel, create_insecure_channel

async def run_trade_match_batch(bpmn_process_id, merged_df):
    """Create C8 process to process all trades"""

    flag = False
    await client.deploy_process("process_models/sprint3-process_C8.bpmn")
    await client.deploy_process("process_models/decide-priority.dmn")

    for i, (idx, trade) in enumerate(merged_df.iterrows()):
        if i == 100:
            assert 100 == 101  # should never get here
        else:
            var_dict = dict()
            var_dict["_merge"] = trade["_merge"]

            # Send firm values to C8 process via variables
            if (trade["_merge"] == "both") or (trade["_merge"] == "left_only"):
                for c in merged_df.columns:
                    if c[-2:] == "_F":
                        new_c = c[:-2]
                        var_dict[new_c] = trade[c]

            # right only, send street values to C8 process via variables
            else:
                for c in merged_df.columns:
                    if c[-2:] == "_S":
                        new_c = c[:-2]
                        var_dict[new_c] = trade[c]
            await client.run_process(bpmn_process_id=bpmn_process_id,
                                     variables=var_dict)

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
client = ZeebeClient(channel)



# Perform batch pre-processing (match vs. unmatched trades)
data_dir = "../DataGeneration/data/"
file_name = "firm_trades"
df = pd.read_parquet(path=f"{data_dir}{file_name}")
firm_ddf = dd.from_pandas(df, npartitions=2)

file_name = "street_trades"
df = pd.read_parquet(path=f"{data_dir}{file_name}")
street_ddf = dd.from_pandas(df, npartitions=2)

firm_idx = firm_ddf.index
street_idx = street_ddf.index

merged_df = firm_ddf.merge(street_ddf, how="outer", left_index=True, right_index=True,
                           suffixes=["_F", "_S"], indicator=True)

# Now, send matched and unmatched trades through the process
bpmn_process_id = "Process_cdd8ac1b-a3e5-4467-8061-784691625fe2"
bpmn_process_id = "sid-1766A6F0-B9E4-41B6-8995-413493416BBB"

loop = asyncio.get_event_loop()
try:
    results = loop.run_until_complete(run_trade_match_batch(bpmn_process_id, merged_df))
finally:
    loop.stop()
    loop.close()