from celery import Celery
import sys

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

@app.task
def exit(x, y):
    sys.exit(0)

@app.task
def clear_c8_task(x, y):
    sys.exit(0)