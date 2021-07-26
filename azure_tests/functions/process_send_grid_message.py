import json
import logging

import azure.functions as func


async def recieve_message_and_notify(
    queue: func.QueueMessage, sendGridMessage: func.Out[str]
) -> None:
    queue = json.loads(queue)

    name = queue.get("name")
    email = queue.get("email")
    text = f"Hello, {name}, we recieved your order!"

    logging.info("Recieved message from queue: %s", json.dumps(queue))

    message = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": email,
                    },
                ]
            },
        ],
        "subject": "Azure Functions email with SendGrid",
        "content": [
            {
                "type": "text/plain",
                "value": text,
            }
        ],
    }

    sendGridMessage.set(json.dumps(message))
