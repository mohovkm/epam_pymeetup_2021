import azure.functions as func


def main(
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
        queue.set(name)
        return func.HttpResponse("Value was set to the queue")

    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
