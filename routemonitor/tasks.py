from celery import shared_task

from routes.services import route_update


@shared_task
def route_update_task():
    route_update()