import json
import logging
from collections import namedtuple
from typing import Dict, NamedTuple


class ResponseBase(NamedTuple):
    text: str
    status_code: int


Response = namedtuple("ResponseBase", ["text", "status_code"])


async def send_message_to_queue(request: Dict, queue):
    name, body = None, None

    try:
        body = request.get_json()
    except ValueError:
        pass
    else:
        name = body.get("name")
        email = body.get("email")

    if name and email:
        queue.set(json.dumps({"name": name, "email": email}))
        return Response(
            f"Value for {name} was set to the queue",
            200,
        )

    else:
        logging.error("Recieved empty or not valid body: %s", json.dumps(body))
        return Response(
            "You must provide name and email in json body",
            400,
        )
