from celery import Celery
import sys
from pyzeebe import ZeebeWorker, create_insecure_channel
import asyncio

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def exit(x, y):
    sys.exit(0)

@app.task
def clear_c8_task(webhook_id):
    channel = create_insecure_channel(
        hostname='44.199.120.6',
        port=26500
    )

    worker = ZeebeWorker(grpc_channel=channel)

    @worker.task(task_type=f"{webhook_id}")
    def execute_webhook(url, method, webhook_uuid):
        # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
        return {}

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(worker.work(one_shot=True))
