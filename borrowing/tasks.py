from celery import shared_task
from time import sleep

@shared_task
def my_task():
    print("Start my_task")
    sleep(3)
    print("End my_task")
    return "my_task completed"


@shared_task
def another_task():
    print("Start another_task")
    sleep(5)
    print("End another_task")
    return "another_task completed"
