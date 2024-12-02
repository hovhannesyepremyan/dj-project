import celery

from .sms import send_sms

from project.celery import app

__all__ = (
    'send_async_sms',
)


@app.task(bind=True)
def send_async_sms(_: celery.Task, message: str, to: str):
    _ = send_sms(message=message, to=to)
