import json
import logging
from os import getenv

import azure.functions as func
from functions import setup_email


async def recieve_message_and_notify(queue: func.QueueMessage) -> None:
    msg = queue.get("name")

    logging.info("Recieved message from queue: %s", msg)

    msg = json.decode(msg)
    reciever = msg.get("reciever")
    provider = getenv("PROVIDER")

    message = f"""\
        Subject: Sent from Azure Functions.

        We recieved your orderd. Details: {msg}"""

    try:
        send_email = setup_email.send_email(provider)
    except KeyError as e:
        logging.error("Can't setup email provider: %s", e)
        return

    send_email(reciever, message)
