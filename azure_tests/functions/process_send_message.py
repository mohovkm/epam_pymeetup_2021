import json
import logging
from os import getenv

import azure.functions as func
from functions import setup_email


async def recieve_message_and_notify(queue: func.QueueMessage) -> None:
    queue = queue.get_body().decode("utf-8")
    queue = json.loads(queue)

    name = queue.get("name")
    email = queue.get("email")

    logging.info("Recieved message from queue: %s", json.dumps(queue))

    provider = getenv("EMAIL_PROVIDER")

    text = f"Hello, {name}, we recieved your order!"

    try:
        send_email = setup_email.send_email(provider)
    except KeyError as e:
        logging.error("Can't setup email provider: %s", e)
        return

    send_email(email, text)
