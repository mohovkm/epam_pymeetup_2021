import azure.functions as func

from functions import process_queue_in


async def main(
    request: func.HttpRequest, queue: func.Out[func.QueueMessage]
) -> func.HttpResponse:

    response, status_code = await process_queue_in.send_message_to_queue(request, queue)

    return func.HttpResponse(
        response,
        status_code=status_code,
    )
