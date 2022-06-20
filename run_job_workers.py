import asyncio
from pyzeebe import ZeebeWorker, create_insecure_channel

channel = create_insecure_channel(
    hostname='44.199.120.6',
    port=26500
)

webhook_id = "webhook_b1124163-6f0f-48c9-bb22-030ed90a5155"

worker = ZeebeWorker(grpc_channel=channel)

@worker.task(task_type=f"{webhook_id}")
def execute_webhook(url, method, webhook_uuid):
    # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
    print('clearing awaiting task in C8')
    return {}

loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(worker.work(one_shot=True))
