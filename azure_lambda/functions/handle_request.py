import json
import logging
from collections import namedtuple
from typing import Dict, NamedTuple

from classes import CustomLogic, CustomLogicException


class ResponseBase(NamedTuple):
    text: str
    status_code: int


Response = namedtuple("ResponseBase", ["text", "status_code"])


async def handler(body: Dict) -> Response:
    url = body.get("url")
    if not url:
        return Response("You must provide url address in json body", 400)

    try:
        logic = CustomLogic(url)
    except CustomLogicException as e:
        logging.error("Can't initialise class")
        return Response(f"There is an error: {e}", 400)

    resp_from_logic = await logic.query_data()
    return Response(
        json.dumps(
            {
                "logic_result": resp_from_logic,
            }
        ),
        200,
    )
