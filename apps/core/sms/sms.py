import logging
import time

import requests

from django.conf import settings

logger = logging.getLogger(__name__)


def send_sms(message: str, to: str):
    recipient = '374{}'.format(to[1:])
    message_id = '{phone}-{time}'.format(phone=to, time=time.time())
    payload = {
        'messages': [
            {
                'recipient': recipient,
                'priority': settings.SMS_PRIORITY,
                'sms': {
                    'originator': settings.SMS_ORIGINATOR,
                    'content': {'text': message},
                },
                'message-id': message_id,
            }
        ]
    }

    response = requests.post(
        url=settings.SMS_API,
        headers={'Content-type': 'application/json; charset=utf-8'},
        auth=(settings.SMS_API_LOGIN, settings.SMS_API_PASSWORD),
        json=payload,
    )

    lfn = logger.info
    msg = 'SMS sent successfully: body={}'.format(payload)
    if response.status_code != 200:
        lfn = logger.error
        msg = 'Failed to send SMS: {info} \nStatus Code: {status}'.format(
            info=payload,
            status=response.status_code
        )

    lfn(msg)

    return response
