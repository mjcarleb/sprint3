from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import sys
from pyzeebe import ZeebeWorker, create_insecure_channel
import asyncio
import time

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task(soft_time_limit=10, time_limit=60)
def add(x, y):
    try:
        time.sleep(20)
    except SoftTimeLimitExceeded:
        return None

    return x + y

@app.task
def exit(x, y):
    sys.exit(0)

@app.task(soft_time_limit=30, time_limit=60)
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
    try:
        loop.set_debug(True)
        loop.run_until_complete(worker.work(one_shot=False))
    except SoftTimeLimitExceeded:
        loop.close()
        return f"closed Zeebe loop for one-shot task type = {webhook_id}"