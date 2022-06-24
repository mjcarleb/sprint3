from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import sys
import asyncio

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def exit(x, y):
    sys.exit(0)

@app.task(soft_time_limit=15, time_limit=30)
def clear_c8_task(webhook_uuid):
    from pyzeebe import ZeebeWorker, create_insecure_channel

    channel = create_insecure_channel(
        hostname='44.199.120.6',
        port=26500
    )

    #pid = self.pid
    worker = ZeebeWorker(grpc_channel=channel)

    @worker.task(task_type=f"{webhook_uuid}")
    def execute_webhook(url, method, webhook_uuid):
        # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
        print('clearing awaiting task in C8')
        return {}

    try:
        loop = asyncio.get_event_loop()
        #loop.set_debug(True)
        loop.run_until_complete(worker.work()) #one_shot=True))
    except SoftTimeLimitExceeded:
        #loop.close()
        return f"Closed Zeebe loop for webhook={webhook_uuid}"