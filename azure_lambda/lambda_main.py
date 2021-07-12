import asyncio
from typing import Dict

from functions import handle_request


async def main(event, context) -> Dict:

    response = await handle_request.handler(event)

    return {"statusCode": response.status_code, "headers": {"Content-Type": "application/json"}, "body": response.text}


def handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main(event, context))
