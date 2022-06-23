import asyncio
import threading

def clear_thread(webhook_id):
    from pyzeebe import ZeebeWorker, create_insecure_channel

    channel = create_insecure_channel(
        hostname='44.199.120.6',
        port=26500
    )

    #pid = self.pid
    worker = ZeebeWorker(grpc_channel=channel)

    @worker.task(task_type=f"{webhook_id}")
    def execute_webhook(url, method, webhook_uuid):
        # Now that Jira has returned the webhook_id, we just clear the task on Zeebe with return
        print('clearing awaiting task in C8')
        return {}

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(worker.work(one_shot=True))


if __name__ == "__main__":

    webhook_id = "webhook_6b1e1ba1-b276-4c5c-9b0d-d27442bb3a83"
    t = threading.Thread(clear_thread(webhook_id))
    t.start()