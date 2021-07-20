import json

import azure.functions as func


async def main(
    request: func.HttpRequest, queue: func.Out[func.QueueMessage]
) -> func.HttpResponse:

    name = request.params.get("name")
    if not name:
        try:
            body = request.get_json()
        except ValueError:
            pass
        else:
            name = body.get("name")

    if name:
        data = {"recieved": name}
        queue.set(json.dumps(data))
        return func.HttpResponse(f"Value {name} was set to the queue")

    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
