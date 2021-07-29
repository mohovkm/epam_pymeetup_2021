import asyncio
import json
import logging
from json import JSONDecodeError
from typing import Dict

from functions import handle_request


async def main(event, context) -> Dict:
    try:
        req_body = json.loads(event.get("body"))
    except (JSONDecodeError, TypeError):
        logging.error("Missed request body")
        return {
            "body": "You must provide url with as a json parameter in request body",
            "statusCode": 400,
        }

    response = await handle_request.handler(req_body)

    return {"statusCode": response.status_code, "headers": {"Content-Type": "application/json"}, "body": response.text}


def handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main(event, context))
