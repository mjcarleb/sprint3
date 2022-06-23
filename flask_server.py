from flask import Flask, request
from celery_tasks import clear_c8_task

####################################################
#   SETUP TO USE WEB SERVER TO RECEIVE WEBHOOK
####################################################
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/CTL',methods=['POST'])
def recevieWebhook():
    """ Jira has return webhook_id for which a Zeebe task is waiting """

    webhook_uuid = request.form['webhook_uuid']
    clear_c8_task.delay(webhook_uuid=webhook_uuid)
    return {"status":  "ok"}

if __name__ == '__main__':

    #  Run the web server to accept webhooks
    app.run(debug=True)