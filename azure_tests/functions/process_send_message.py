import json
import logging

import azure.functions as func


async def recieve_message_and_notify(
    queue: func.QueueMessage, sendGridMessage: func.Out[str]
) -> None:
    msg = queue.get("name")

    logging.info("recieved message from queue: %s", msg)

    value = f"Sent from Azure Functions. Value from the queue: {msg}"

    message = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": "konstantin_mokhov@epam.com",
                    },
                ],
            },
        ],
        "subject": "Azure Functions email with SendGrid",
        "content": [
            {
                "type": "text/plain",
                "value": value,
            },
        ],
    }

    sendGridMessage.set(json.dumps(message))
