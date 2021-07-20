import azure.functions as func
from functions import process_queue_in


async def main(
    request: func.HttpRequest, queue: func.Out[func.QueueMessage]
) -> func.HttpResponse:

    response, status_code = process_queue_in(request, queue)

    return func.HttpResponse(
        response,
        status_code=status_code,
    )
