import logging

import azure.functions as func

from functions import handle_request


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
    except ValueError:
        logging.error("Missed request body")
        return func.HttpResponse(
            "You must provide url with as a json parameter in request body",
            status_code=400,
        )

    response = await handle_request.handler(req_body)

    return func.HttpResponse(
        response.text,
        status_code=response.status_code,
        mimetype="application/json",
    )
